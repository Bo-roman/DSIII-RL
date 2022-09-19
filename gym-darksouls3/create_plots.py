import sys
sys.path.insert(1, '..//PythonLibs//SQLite3')
import matplotlib.pyplot as plt
from datetime import datetime
from sqlite_3 import SQLite_3
import numpy as np
import config
import errno
import os

PLOTS_PATH = config.VERSION_FOLDER + 'plots'
LOSS_CAP = 50000
try:
    os.makedirs(PLOTS_PATH)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

def plot_loss(losses):
    losses_capped =  np.minimum(losses,LOSS_CAP)
    plt.ylabel('loss')
    plt.xlabel('{} trained batches'.format(len(losses_capped)))
    plt.title('Loss plot')
    plt.plot(losses_capped)
    plt.savefig(PLOTS_PATH + '/' + str(datetime.now()).replace(':','-') + '_loss.jpg',dpi=1000)
    plt.clf()
    

def plot_reward(rewards):
    plt.ylabel('reward')
    plt.xlabel('{} episodes'.format(len(rewards)))
    plt.title('Reward plot')
    plt.plot(np.arange(len(rewards)),rewards)
    plt.savefig(PLOTS_PATH + '/' + str(datetime.now()).replace(':','-') + '_reward.jpg',dpi=1000)
    plt.clf()

def plot_reward_epsilon(rewards,epsilons):
    plt.ylabel('reward')
    plt.xlabel('epsilon'.format(len(rewards)))
    plt.title('Reward plot')
    plt.plot(epsilons,rewards)
    plt.savefig(PLOTS_PATH + '/' + str(datetime.now()).replace(':','-') + '_reward_epsilon.jpg',dpi=1000)
    plt.clf()

    
try:
    sqlite = SQLite_3(config.TRAINING_DATA_DATABASE_NAME)
    sqlite.connect()
    training_data = sqlite.select(config.TRAINING_DATA_TABLE)
    training_experiences_data = sqlite.select(config.TRAINING_EXPERIENCES_DATA_TABLE)
    sqlite.close()
except Exception as e:
    print(e)
experiences_epochs = [data[1] for data in training_experiences_data]
experiences_episodes = [data[2] for data in training_experiences_data]
rewards = [data[3] for data in training_experiences_data]
actions = [data[4] for data in training_experiences_data]
epsilons = [data[5] for data in training_experiences_data]
training_epochs = [data[1] for data in training_data]
training_episodes = [data[2] for data in training_data]
losses  = [data[3] for data in training_data]

def averageReward(rewards):
    idx = 0
    a = [[]*200] * len(experiences_episodes)
    for i in experiences_episodes:
        a[i] = a[i] + [rewards[idx]]
        idx += 1

    reward_averages = []
    idx = 0
    for i in a:
        if len(i) != 0:
            reward_averages.append(sum(i) / len(i))
    return reward_averages


def averageRewardEpisodes(rewards,number):
    idx = 0
    averaged = 0
    a = []
    for i in range((len(rewards))):
        if i % number == 0:
            a.append(averaged/number)
            averaged = 0
        else:
            averaged += rewards[i]

    print(a)
    return a
    
plot_loss(losses)
#plot_reward(averageRewardEpisodes(averageReward(rewards),3))
plot_reward(averageReward(rewards))
plot_reward_epsilon(rewards,epsilons)
