import gym
import sys
import numpy as np
import cv2 as cv
import logging
sys.path.insert(1, '..//PythonLibs')
sys.path.insert(1, '..//PythonLibs//SQLite3')
from darksouls3playerState import PlayerStateController
import characterActions
from windowcapture import WindowCapture

windowCaptureConfig = {
    'WINDOW_WIDTH': 1280,
    'WINDOW_HEIGHT': 740,
    'WIDNOW_NAME': 'DARK SOULS III'
}

playerControllerConfig = {
    'bossName': 'Iudex Gundy',
    'bossFogDoor': {
        'x': 125.6999969,
        'y': 558.2000122,
        'z': -64.05046844
    },
    'inFrontOfBoss': {
        'x': 133.6301727,
        'y': 579.1668701,
        'z': -68.48419952
    },

    'ports': {
        'get': 64501,
        'set': 64502
    },

    'penalties': {
        'movement': 15
    },

    'ip': 'localhost',

    'loadingScreenTime': 20,

    'lockCameraAfterAnimations': ['ThrowDef'],

    'attackAnimations': ['AttackRightLight1', 'AttackRightLight2', 'AttackRightLight3']

}


class DarkSouls3Env(gym.Env):

    def __init__(self):
        super(DarkSouls3Env, self).__init__()
        self.action_space = gym.spaces.Discrete(len(characterActions.action_list))
        self.observation_space = gym.spaces.Box(0, 255, [windowCaptureConfig['WINDOW_WIDTH'],
                                                         windowCaptureConfig['WINDOW_HEIGHT'], 3], dtype=np.uint8)

        self.playerStateController = PlayerStateController(playerControllerConfig)
        self.playerState = {}
        self.previousState = self.playerStateController.getPlayerState()
        self.currentState = {}

        self.penaltiesCounter = {'movement': 0}

        try:
            self.gameWindow = WindowCapture(windowCaptureConfig)
        except Exception as exeption:
            print(exeption)

    def just_step(self, action):
        characterActions.action_list[action]()  # executing action

    def step(self, action):
        characterActions.action_list[action]()  # executing action
        self.currentState = self.playerStateController.getPlayerState()

        if self.currentState['targetedEntityHP'] == -1:
            raise Exception('Error has occured when teleporting to {}'.format(playerControllerConfig['bossName']))

        done = False

        reward = self.getReward()

        if self.checkEndOfEpisode():
            done = True

        if self.currentState['playerAnimation'] in playerControllerConfig['lockCameraAfterAnimations']:
            self.playerStateController.lockCameraOnBoss()

        self.previousState = self.currentState

        return self.gameWindow.get_screenshot(), reward, done, 0

    def reset(self):
        self.playerStateController.resetWorldState()
        return self.gameWindow.get_screenshot()

    def render(self, mode="human"):
        raise NotImplementedError

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass

    def seed(self, seed=None):
        return

    def checkEndOfEpisode(self):
        return self.currentState['playerHP'] <= 0 or \
               self.currentState['playerAnimation'] == 'DeathStart' or \
               self.currentState['targetedEntityHP'] == 0

    def getReward(self):
        reward = 0

        if self.currentState['playerHP'] < self.previousState['playerHP']:
            reward -= 50

        if self.currentState['playerHP'] == 0:
            reward -= 500

        if self.currentState['targetedEntityHP'] < self.previousState['targetedEntityHP']:
            reward += 60

        if self.currentState['targetedEntityHP'] == 0:
            reward += 500

        # increment penalties
        if self.currentState['playerAnimation'] == 'Move':
            self.penaltiesCounter['movement'] += 1

        if self.penaltiesCounter['movement'] > playerControllerConfig['penalties']['movement']:
            self.penaltiesCounter['movement'] = 0
            reward -= 10

        return reward

    def _StateHasErrors(self, currentState):
        if 'playerHP' not in currentState or \
                'playerStamina' not in currentState or \
                'playerAnimation' not in currentState or \
                'targetedEntityHP' not in currentState:
            return True

        return False


#import matplotlib.pyplot as plt
#cap = WindowCapture(windowCaptureConfig)
#image = cap.get_screenshot()
#image = image[0:590,350:800]
#image = cv.resize(image, (93,150))
#print(np.array(image).shape)
#plt.imshow(image)
#plt.show()
