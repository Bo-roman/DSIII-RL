import dsSocket
import characterActions
import time
import logging

class PlayerStateController:
    '''
    config = {
        'bossFogDoor' : {
            'x' : float
            'y' : float
            'z' : float
        },

        'inFrontOfBoss' : {
            'x' : float
            'y' : float,
            'z' : float
        },

        'loadingScreenTime' : float | int ,

        'ports' : {
            'get' : int,
            'set' : int
        },
        
        'ip' : string

   
    },

  

    '''

    def __init__(self, config):
        self.game_variables = [
            'playerHP',
            'playerMaxHP',
            'playerMaxStamina',
            'playerAnimation',
            'playerXaxis',
            'playerZaxis',
            'playerYaxis',
            'GundyrFlags'
        ]
        '''
        Gundyr world flag is stored in a byte,
        MSB is defeated
        2nd MSB is encountered
        3rd MSB is pulled sword
        so 01100000  = 96 means undefeated, enountered, pulled sword
        '''
        self.gundyrFlags = {'Default': 96,
                            'Dead': 224,
                            'Alive': 127}
        self.config = config

    # returns object received from get server
    def getPlayerState(self):
        client = dsSocket.connectToServer(self.config['ip'], self.config['ports']['get'])
        Object = dsSocket.recvDSRLObject(client)
        client.close()

        return Object

    # x, y, z = float, float, float
    def setPlayerPosition(self, x, y, z):
        client = dsSocket.connectToServer(self.config['ip'], self.config['ports']['set'])
        posObject = {self.game_variables[4]: x, self.game_variables[5]: z, self.game_variables[6]: y}
        dsSocket.sendDSRLObject(client, posObject)
        client.close()

    def lockCameraOnBoss(self):
        characterActions.lockCameraOnMonster()

    # health = int
    def setPlayerHealth(self, health):
        client = dsSocket.connectToServer(self.config['ip'], self.config['ports']['set'])
        dsSocket.sendDSRLObject(client, {'playerHP': health})
        client.close()

    def teleportToBoss(self):
        # teleport infront of the door
        # its a little unstable please update x,y,z as pleased
        # might die on teleport if there are mobs infront of the door
        # the game engine kind of gets retarded when you teleport to
        # an unrendered area
        self.setPlayerPosition(self.config['bossFogDoor']['x'], self.config['bossFogDoor']['y'],
                               self.config['bossFogDoor']['z'])
        time.sleep(0.5)
        # press E to enter fog wall
        characterActions.interact()
        time.sleep(2.5)
        self.setPlayerPosition(self.config['inFrontOfBoss']['x'], self.config['inFrontOfBoss']['y'],
                               self.config['inFrontOfBoss']['z'])

    def resetPositionToBoss(self):
        self.teleportToBoss()
        time.sleep(2.5)
        self.lockCameraOnBoss()
        time.sleep(1)

    def resetGundyrWorldFlags(self):
        client = dsSocket.connectToServer(self.config['ip'], self.config['ports']['set'])
        posObject = {self.game_variables[7]: self.gundyrFlags['Alive']}
        dsSocket.sendDSRLObject(client, posObject)
        client.close()

    def resetWorldState(self):
        try:
            while self.getPlayerState()['playerHP'] != 0:
                self.setPlayerHealth(0)
        except KeyError as ke:
            logging.warning('Environment tried to reset prematurely')
            time.sleep(5)

        self.resetGundyrWorldFlags()
        characterActions._stopMoving()
        time.sleep(self.config['loadingScreenTime'])
        #characterActions._stopMoving()
        time.sleep(0.5)
        self.resetPositionToBoss()
