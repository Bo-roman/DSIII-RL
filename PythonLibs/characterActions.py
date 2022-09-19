import directInput  # PressKey(scanCode) & ReleaseKey(scanCode)
import time
from threading import Thread

# the time needed by the game to register a keystroke
TIMEWAIT_BETWEEN_PRESS_RELEASE = 0.03
TIMEWAIT_BETWEEN_ACTION_CHAIN = 0

# scancodes of the keys used in darksouls3
ds3_keys = {
    'W': 0x11,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'E': 0x12,
    'ROLL': 0x08,
    'attack': 0x9,
    'sAttack': 0x0A,
    'lock_on': 0x10,
    'use_item': 0x13,
    'switch_item': 0x0b,
    'two_hand_weapon': 0x21
}


# Move Forward ----------------------------
def moveForward():
    directInput.PressKey(ds3_keys['W'])


# to unlock the camera call this function again
# def moveForward():
#     moveForwardThread = Thread(target = _moveForward, args = [])
#     moveForwardThread.start()
#     return moveForwardThread
# -------------------------------------------


# Move Backwards ----------------------------
def moveBackwards():
    directInput.PressKey(ds3_keys['S'])


# def moveBackwards():
#     moveBackwardsThread = Thread(target = _moveBackwards, args = [])
#     moveBackwardsThread.start()
#     return moveBackwardsThread
# -------------------------------------------


# Move Left ----------------------------
def moveLeft():
    directInput.PressKey(ds3_keys['A'])


# def moveLeft():
#     moveLeftThread = Thread(target = _moveLeft, args = [])
#     moveLeftThread.start()
#     return moveLeftThread
# -------------------------------------------


# Move Right ----------------------------
def moveRight():
    directInput.PressKey(ds3_keys['D'])


# def moveRight():
#     moveRightThread = Thread(target = _moveRight, args = [])
#     moveRightThread.start()
#     return moveRightThread
# -------------------------------------------

# Stop Moving ----------------------------
def _stopMoving():
   
    directInput.PressKey(ds3_keys['A'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['A'])

    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)

    
    directInput.PressKey(ds3_keys['D'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['D'])

    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)


    directInput.PressKey(ds3_keys['S'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['S'])

    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)

    
    directInput.PressKey(ds3_keys['W'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['W'])


def stopMoving():
    stopMovingThread = Thread(target=_stopMoving, args=[])
    stopMovingThread.start()
    return stopMovingThread


# -------------------------------------------


# Lock Camera  -------------------------------
def lockCameraOnMonster():
    directInput.PressKey(ds3_keys['lock_on'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['lock_on'])


# to unlock the camera call this function again
# def lockCameraOnMonster():
#    lockCameraOnMonster = Thread(target = _lockCameraOnMonster, args = [])
#    lockCameraOnMonster.start()
#    return lockCameraOnMonster
# -------------------------------------------


# Attack --------------------------------------
def attack():
    _stopMoving()
    directInput.PressKey(ds3_keys['attack'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['attack'])
    # time.sleep(0.9)


# def attack():
#    attackThread = Thread(target = _attack, args = [])
#    attackThread.start()
#    return attackThread
# --------------------------------------------


# Strong Attack -------------------------------
def strongAttack():
    directInput.PressKey(ds3_keys['sAttack'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['sAttack'])
    # time.sleep(2)


# def strongAttack():
#    strongAttackThread = Thread(target = _strongAttack, args = [])
#    strongAttackThread.start()
#    return strongAttackThread
# ---------------------------------------------

# Roll Forward ---------------------------------
def rollForward():
    _stopMoving()
    directInput.PressKey(ds3_keys['W'])
    directInput.PressKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['W'])
    # time.sleep(1.3)


# def rollForward():
#    rollForwardThread = Thread(target = _rollForward, args = [])
#    rollForwardThread.start()
#    return rollForwardThread
#  --------------------------------------------


# Roll Backwards -------------------------------
def rollBackwards():
    _stopMoving()
    directInput.PressKey(ds3_keys['S'])
    directInput.PressKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['S'])
    # time.sleep(1.3)


# def rollBackwards():
#    rollBackwardsThread = Thread(target = _rollBackwards, args = [])
#    rollBackwardsThread.start()
#    return rollBackwardsThread
#  --------------------------------------------


# Roll Left -------------------------------------
def rollLeft():
    _stopMoving()
    directInput.PressKey(ds3_keys['A'])
    directInput.PressKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['A'])
    # time.sleep(1.3)


# def rollLeft():
#    rollLeftThread = Thread(target = _rollLeft, args = [])
#    rollLeftThread.start()
#    return rollLeftThread
#  ------------------------------------------


# Roll Right ---------------------------------
def rollRight():
    _stopMoving()
    directInput.PressKey(ds3_keys['D'])
    directInput.PressKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['ROLL'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['D'])
    # time.sleep(1.3)


# def rollRight():
#    rollRightThread = Thread(target = _rollRight, args = [])
#    rollRightThread.start()
#    return rollRightThread
#  ------------------------------------------


# Two Hand Weapon ----------------------------
def twoHandWeapon():
    directInput.PressKey(ds3_keys['two_hand_weapon'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['two_hand_weapon'])
    # time.sleep(0.7)


# to use again one handed weapon call this function again
# def twoHandWeapon():
#    twoHandWeaponThread = Thread(target = _twoHandWeapon, args = [])
#    twoHandWeaponThread.start()
#    return twoHandWeaponThread
# -------------------------------------------


# Use Item -----------------------------------
def useItem():
    directInput.PressKey(ds3_keys['use_item'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['use_item'])
    # time.sleep(2)


# def useItem():
#    useItemThread = Thread(target = _useItem, args = [])
#    useItemThread.start()
#    return useItemThread
# -------------------------------------------

# Switch consumable item ---------------------
def switchItem():
    directInput.PressKey(ds3_keys['switch_item'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['switch_item'])


# def switchItem():
#    switchItemThread = Thread(target = _switchItem, args = [])
#    switchItemThread.start()
#    return switchItemThread
# -------------------------------------------


# Interact -----------------------------------
def interact():
    directInput.PressKey(ds3_keys['E'])
    time.sleep(TIMEWAIT_BETWEEN_PRESS_RELEASE)
    directInput.ReleaseKey(ds3_keys['E'])


# def interact():
#    interactThread = Thread(target = _interact, args = [])
#    interactThread.start()
#    return interactThread
# -------------------------------------------


# Cancel Every Action ------------------------
def _cancelActions():
    for key in ds3_keys:
        directInput.ReleaseKey(ds3_keys[key])



def cancelActions():
    cancelActionsThread = Thread(target=_cancelActions, args=[])
    cancelActionsThread.start()
    return cancelActionsThread


# -------------------------------------------


# Action List
# action_dictionary = {  'moveForward' : moveForward,
#                       'moveBackwards' : moveBackwards,
#                       'moveLeft' : moveLeft,
#                       'moveRight' : moveRight,
#                       'stopMoving' : stopMoving,
#                       'attack' : attack,
#                       'strongAttack' : strongAttack,
#                       'rollForward' : rollForward,
#                       'rollBackwards' : rollBackwards,
#                       'rollLeft' : rollLeft,
#                       'rollRight' : rollRight,
#                       'twoHandWeapon' : twoHandWeapon,
#                       'useItem' : useItem,
#                       'cancelActions' : cancelActions
#                    }

action_dictionary = {
                     'attack': attack,
                     'rollForward': rollForward,
                     'rollBackwards': rollBackwards,
                     'rollLeft': rollLeft,
                     'rollRight': rollRight
                     }

action_list = list(action_dictionary.values())
