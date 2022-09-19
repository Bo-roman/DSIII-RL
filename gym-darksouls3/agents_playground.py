"""
Training loop

This module trains the DQN agent by trial and error. In this module the DQN
agent will play the game episode by episode, store the gameplay experiences
and then use the saved gameplay experiences to train the underlying model.
"""
from sqlite_training_data_logger import TrainigDataLogger
from frame_stack_wrapper import FrameStack, LazyFrames2D
from darksouls3_env import DarkSouls3Env
from replay_buffer import ReplayBuffer
from dqn_agent import DqnAgent
from drqn_agent import DrqnAgent
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import logging
import config
import signal
import errno
import time
import csv
import sys
import os

def save_state_csv(csv_name, row):
    with open(csv_name, 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(row)

def load_state_csv(csv_name):
    try:
        with open(csv_name, newline='') as csvfile:
            lines = list(csv.reader(csvfile))
            return float(lines[0][0]), int(lines[0][1]), int(lines[0][2])

    except FileNotFoundError as e:
        print(e)
        return config.EPSILON_MAX, 0, 0

#//// Preset variables
try:
    os.makedirs(config.VERSION_FOLDER)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

LOGGING_LEVEL = logging.INFO
EPISODE_NAME = 'Experiences_'
TRAINING_BATCHES = 32 # how many batches to train per epoch
NUMBER_OF_EXPERIENCES = config.BATCH_SIZE * TRAINING_BATCHES # how many experiences to collect before training
CURRENT_EPSILON,EPOCH_NUMBER,EPISODE_NUMBER = load_state_csv(config.CSV_NAME)
CURRENT_EPSILON = 0.45
#//// playground variables
WANT_TO_TRAIN = False
WANT_TO_COLLECT_EXPERIENCES = True
SAVE_EXPERIENCES = False
SAVE_DISK_SPACE = True
training_data_logger = TrainigDataLogger(config.TRAINING_DATA_DATABASE_NAME,NUMBER_OF_EXPERIENCES)
agent = DqnAgent(config.STACKED_IMAGE_SHAPE, config.NUMBER_OF_ACTIONS,config.GAMMA,CURRENT_EPSILON,config.EPSILON_MIN, config.EPSILON_DECAY_RATE, config.LEARNING_RATE,config.VERSION_FOLDER)
buffer = ReplayBuffer(config.DATABASE_NAME, config.STACKED_IMAGE_SHAPE,batch_size = config.BATCH_SIZE)
env = FrameStack(DarkSouls3Env(),config.FRAME_STACK,LazyFrames2D)



logging.basicConfig(
    level=LOGGING_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(config.VERSION_FOLDER + 'log_' + config.VERSION + '.log'),
        logging.StreamHandler(sys.stdout)
    ])


def preprocess_state(state):

    #return np.reshape(cv.resize(np.array(state)[100:690,550:900], (config.IMAGE_SHAPE[1],config.IMAGE_SHAPE[0])),(1,150,93,12))
    return np.reshape(cv.resize(np.array(state)[100:690,550:900], (config.IMAGE_SHAPE[1],config.IMAGE_SHAPE[0])),config.STACKED_IMAGE_SHAPE)


def collect_gameplay_experiences(env, agent, buffer, storing_table):
    """
    Collects gameplay experiences by playing env with the instructions
    produced by agent and stores the gameplay experiences in buffer.

    :param env: the game environment
    :param agent: the DQN agent
    :param buffer: the replay buffer
    :return: None
    """
    logging.info('Resetting the enviroment')
    state = preprocess_state(env.reset())
    number_of_steps_taken = 1
    cumulated_reward = 0
    done = False
    preProcessedNextState = []
    action = agent.collect_policy(state)  # init action variable
    try:
        start_episode_time = time.perf_counter()
        time_of_execution = time.time()
        while done == False and number_of_steps_taken  <= config.MAX_STEPS_PER_EPISODE:
            if time.time() - time_of_execution >= config.OBSCURING_FACTOR:
                action = agent.collect_policy(state)
                next_state, reward, done, _ = env.step(action)
                preProcessedNextState = preprocess_state(next_state)
                buffer.store_gameplay_experience(state, preProcessedNextState, reward, action, done)
                training_data_logger.enqueue_experience_data(EPOCH_NUMBER,EPISODE_NUMBER,reward,action,agent.epsilon)
                logging.debug('Saving the experiences\n {0} | {1} | {2} | {3} | {4} | {5}'.format(state.shape,preProcessedNextState.shape,reward,action,done,agent.epsilon))
                state = preProcessedNextState
                cumulated_reward += reward
                number_of_steps_taken += 1

            else:
                logging.debug('Executing the same action')
                env.just_step(action)
        end_episode_time = time.perf_counter()
        logging.info('Reward for this episode : {0} | Experiences collected : {1} | Episode took : {2:.3g} seconds to finish'.format(cumulated_reward,number_of_steps_taken,end_episode_time-start_episode_time))

        if buffer.getExperiencesCount() > config.MIN_ACTIONS and number_of_steps_taken <= config.MAX_STEPS_PER_EPISODE and SAVE_EXPERIENCES:
            logging.info('Storing experiences...')
            buffer.store_in_database(storing_table)
            training_data_logger.log_experience_data(config.TRAINING_EXPERIENCES_DATA_TABLE)
            return True
        else:
            raise Exception('')


    except Exception as e:
        buffer.cleanMemoryBuffer()
        logging.error(e)
        logging.info('Memory Replay Buffer has been cleared of this atrocity...')
        return False


def train_model(agent, buffer, env, current_epoch):
    """

    :return: None
    """
    global EPISODE_NUMBER
    global EPOCH_NUMBER
    training_batch_count = 0
    sql_experiences_table = EPISODE_NAME + str(current_epoch)
    db_experiences_count = buffer.getDBExperiencesCount(sql_experiences_table)
    fit_history = []

    if WANT_TO_COLLECT_EXPERIENCES:
        logging.info('Episode {0} starting'.format(EPISODE_NUMBER))
        while db_experiences_count < NUMBER_OF_EXPERIENCES:
            while(collect_gameplay_experiences(env,agent,buffer,sql_experiences_table) == False):
                logging.warning('Failed to start episode...Retrying...')
            db_experiences_count = buffer.getDBExperiencesCount(sql_experiences_table)
            logging.info('Collected {0} / {1} Experiences'.format(db_experiences_count,NUMBER_OF_EXPERIENCES))
            EPISODE_NUMBER +=1
            save_state_csv(config.CSV_NAME,[agent.epsilon,EPOCH_NUMBER,EPISODE_NUMBER])


    if WANT_TO_TRAIN:
        logging.info('Begining Training...')
        while not buffer.hasSamplingFinished() and training_batch_count < TRAINING_BATCHES:
            logging.info('Epoch {0} | Training batch {1} / {2}'.format(EPOCH_NUMBER,training_batch_count + 1,TRAINING_BATCHES))
            s, n, r, a, d = buffer.sample_gameplay_batch(sql_experiences_table,TRAINING_BATCHES)
            #agent.zeroLSTM()
            fit_history = agent.update_model(s, n, r, a, d, config.BATCH_SIZE)
            logging.info('Storing training data...')
            training_data_logger.log_training_data(config.TRAINING_DATA_TABLE,EPOCH_NUMBER,training_batch_count,fit_history.history['loss'][0])
            training_batch_count += 1

        agent.save_q_net_checkpoint()

        if EPOCH_NUMBER != 0 and EPOCH_NUMBER % config.Q_NET_TARGET_UPDATE_INTERVAL == 0:
            logging.info('Updating target network...')
            agent.update_target_model()
            agent.save_q_net_target_checkpoint()

        EPOCH_NUMBER += 1

        logging.info('Finished Training : {0}'.format(not buffer.hasSamplingFinished()))


def signint_handler(signum,frame):
    logging.warning('Guess someone wants to kill my lovely program...shame\nBut fine im saving the state')
    save_state_csv(config.CSV_NAME,[agent.epsilon,EPOCH_NUMBER,EPISODE_NUMBER])
    exit(1)
signal.signal(signal.SIGINT, signint_handler)

try:
    for _ in range(EPOCH_NUMBER,99999):
        logging.info('Starting Training Epoch {}'.format(_))
        train_model(agent, buffer, env, _)
        if SAVE_DISK_SPACE:
            os.remove(config.DATABASE_NAME) # to save memory...one batch of 128 takes 40GB
except Exception as e:
    save_state_csv(config.CSV_NAME,[agent.epsilon,EPOCH_NUMBER,EPISODE_NUMBER])
    logging.error(e)
    raise e

