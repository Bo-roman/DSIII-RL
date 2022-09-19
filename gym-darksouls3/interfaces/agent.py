import tensorflow as tf
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import config
from tensorflow import keras
from tensorflow.keras import layers


class Agent:
    """
    DQN Agent

    The agent that explores the game and learn how to play the game by
    learning how to predict the expected long-term return, the Q value given
    a state-action pair.
    """

    def __init__(self,state_shape,number_of_actions,gamma,epsilon,epsilon_min,decay_rate,learning_rate,save_location):
        #configs
        self.q_net_location = save_location + 'q_net_checkpoint'
        self.q_net_target_location = save_location + 'q_net_target_checkpoint'
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.number_of_actions = number_of_actions
        self.state_shape = state_shape
        
        
        #neural networks
        self.q_net = self._build_model()
        self.q_net_target = self._build_model()
        opt = keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.q_net.compile(loss='mean_squared_error',optimizer=opt)
        self.q_net_target.compile(loss='mean_squared_error',optimizer=opt)
        #more configs
        self.q_net_checkpoint = tf.train.Checkpoint(step=tf.Variable(0), net=self.q_net)
        self.q_net_checkpoint_manager = tf.train.CheckpointManager(self.q_net_checkpoint, self.q_net_location, max_to_keep=10)
        
        self.q_net_target_checkpoint = tf.train.Checkpoint(step=tf.Variable(0), net=self.q_net_target)
        self.q_net_target_checkpoint_manager = tf.train.CheckpointManager(self.q_net_target_checkpoint, self.q_net_target_location, max_to_keep=10)
        
        self.load_q_net_checkpoint()
        self.load_q_net_target_checkpoint()

    def _build_model(self):
        raise Exception('to be implemented')

    def random_policy(self):
        """
        Outputs a random actio
        """
        return np.random.randint(0, self.number_of_actions)

    def collect_policy(self, state):
        """
        Similar to policy but with some randomness to encourage exploration.
        """
        self.epsilon = max(self.epsilon - self.decay_rate, self.epsilon_min)
        if self.epsilon > np.random.rand(1)[0]:
            return self.random_policy()

        return self.policy(state)

    def policy(self, state):
        """
        Takes a state from the game environment and returns an action that
        has the highest Q value and should be taken as the next step.
        """
        #state_tensor = tf.convert_to_tensor(state)
        #state_tensor = tf.expand_dims(state_tensor, 0)
        action_probs = self.q_net.predict(np.expand_dims(state,axis=0))
        # Take best action
        action = tf.argmax(action_probs[0]).numpy()
        return action

    def update_model(self,state_sample,state_next_sample,rewards_sample,action_sample,done_sample,batches=32):
        # Build the updated Q-values for the sampled future states
        # Use the target model for stability
        future_rewards = self.q_net_target.predict(state_next_sample)
        # Q value = reward + discount factor * expected future reward
        updated_q_values = rewards_sample + (self.gamma * tf.reduce_max(
                future_rewards, axis=1)) * (1 - done_sample)

        return self.q_net.fit(state_sample,updated_q_values,epochs=1,batch_size=batches)

    def update_target_model(self):
        self.q_net_target.set_weights(self.q_net.get_weights())

    def save_q_net_checkpoint(self):
        self.q_net_checkpoint_manager.save()

    def load_q_net_checkpoint(self):
        self.q_net_checkpoint.restore(self.q_net_checkpoint_manager.latest_checkpoint)

    def save_q_net_target_checkpoint(self):
        self.q_net_target_checkpoint_manager.save()

    def load_q_net_target_checkpoint(self):
        self.q_net_target_checkpoint.restore(self.q_net_target_checkpoint_manager.latest_checkpoint)
        
