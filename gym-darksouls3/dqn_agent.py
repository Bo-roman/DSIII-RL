import tensorflow as tf
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import config
from tensorflow import keras
from tensorflow.keras import layers
from interfaces.agent import Agent

class DqnAgent(Agent):
    """
    DQN Agent

    The agent that explores the game and learn how to play the game by
    learning how to predict the expected long-term return, the Q value given
    a state-action pair.
    """

    def __init__(self,state_shape,number_of_actions,gamma,epsilon,epsilon_min,decay_rate,learning_rate,save_location):
        super().__init__(state_shape,number_of_actions,gamma,epsilon,epsilon_min,decay_rate,learning_rate,save_location)

    def _build_model(self):
        inputs = layers.Input(shape=self.state_shape)
        # Convolutions on the frames on the screen
        layer1 = layers.Conv2D(32, (8, 8), strides=(4, 4), activation="relu")(inputs)
        layer2 = layers.Conv2D(64, (4, 4), strides=(2, 2), activation="relu")(layer1)
        layer3 = layers.Conv2D(64, (3, 3), strides=(1, 1), activation="relu")(layer2)

        layer4 = layers.Flatten()(layer3)

        layer5 = layers.Dense(128,activation="relu")(layer4)
        layer6 = layers.Dense(64,activation="relu")(layer5)
        layer7 = layers.Dense(32, activation="relu")(layer6)
        actions = layers.Dense(self.number_of_actions, activation="relu")(layer7)
        keras.Model(inputs=inputs, outputs=actions).summary()
        return keras.Model(inputs=inputs, outputs=actions)
        
