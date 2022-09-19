from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, TimeDistributed
from interfaces.agent import Agent
from keras.layers.convolutional import Conv2D
from keras.backend import variable
import numpy

class DrqnAgent(Agent):
    """
    DQN Agent

    The agent that explores the game and learn how to play the game by
    learning how to predict the expected long-term return, the Q value given
    a state-action pair.
    """

    def __init__(self, state_shape, number_of_actions, gamma, epsilon, epsilon_min, decay_rate, learning_rate,
                 save_location):
        super().__init__(state_shape, number_of_actions, gamma, epsilon, epsilon_min, decay_rate, learning_rate,
                         save_location)

    def a_build(self):
        inputs = layers.Input(shape= self.state_shape)
        # Convolutions on the frames on the screen
        layer1 = layers.Conv2D(32, (5, 5), activation="relu")(inputs)
        layer2 = layers.Conv2D(64, (3, 3), activation="relu")(layer1)
        layer3 = layers.Conv2D(128, (3, 3), activation="relu")(layer2)

        layer4 = layers.Flatten()(layer3)
        print(layer3.shape)
        layer5 = layers.LSTM(512,input_shape=(10,) + layer3.shape)(layer4)
        layer5 = layers.Dense(128, activation="relu")(layer4)
        layer6 = layers.Dense(64, activation="relu")(layer5)
        layer7 = layers.Dense(32, activation="relu")(layer6)
        actions = layers.Dense(self.number_of_actions, activation="relu")(layer7)

        return keras.Model(inputs=inputs, outputs=actions)

    def _build_model(self):
        self.model = Sequential()

        self.model.add(TimeDistributed(Conv2D(32, (8, 8), strides=(4, 4), activation='relu'),

                                  input_shape= self.state_shape))

                                  #input_shape=(time_step, row, col, channels)
                                  
        self.model.add(TimeDistributed(Conv2D(64, (4, 4), strides=(2, 2), activation='relu')))
       
        self.model.add(TimeDistributed(Conv2D(64, (3, 3), strides=(1, 1), activation='relu')))
       
        self.model.add(TimeDistributed(Flatten()))

        self.model.add(LSTM(512))

        #self.model.add(Dense(128, activation='relu'))

        self.model.add(Dense(self.number_of_actions))
        self.model.summary()
        self.zeroLSTM()
        
        return self.model

    def zeroLSTM(self):
        self.model.layers[4].states[0] = variable(numpy.zeros(self.state_shape))
        self.model.layers[4].states[1] = variable(numpy.zeros(self.state_shape))
