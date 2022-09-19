gameState = {}

function readGameStateAddresses()

    gameStateAddresses = {}

    gameStateAddresses['playerHP']         = readPointer(readPointer(readPointer(readPointer('BaseB') + 0x80)+ 0x1F90) + 0x18)+0xD8
    gameStateAddresses['playerMaxHP']      = readPointer(readPointer(readPointer(readPointer('BaseB') + 0x80)+ 0x1F90) + 0x18)+0xDC
    gameStateAddresses['playerStamina']    = readPointer(readPointer(readPointer(readPointer('BaseB') + 0x80)+ 0x1F90) + 0x18)+0xF0
    gameStateAddresses['playerMaxStamina'] = readPointer(readPointer(readPointer(readPointer('BaseB') + 0x80)+ 0x1F90) + 0x18)+0xF4
    gameStateAddresses['playerAnimation']  = readPointer(readPointer(readPointer(readPointer('BaseB') + 0x80)+ 0x1F90) + 0x28)+0x898
    gameStateAddresses['playerXaxis']      = readPointer(readPointer(readPointer('BaseB') + 0x40)+ 0x28) + 0x80
    gameStateAddresses['playerZaxis']      = readPointer(readPointer(readPointer('BaseB') + 0x40)+ 0x28) + 0x84
    gameStateAddresses['playerYaxis']      = readPointer(readPointer(readPointer('BaseB') + 0x40)+ 0x28) + 0x88
    gameStateAddresses['GundyrFlags'] = readPointer('[GameFlagData]') + 0x5A67
    gameStateAddresses['speedHack']        = speedhack_setSpeed 
   
    --[[
    if readPointer('target_ptr') ~= nil then
        gameStateAddresses['targetedEntityHP'] = readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x18) + 0xD8
        gameStateAddresses['targetedEntityMaxHP'] = readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x18) + 0xDC
        gameStateAddresses['targetedEntityStamina'] = readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x18) + 0xF0
        gameStateAddresses['targetedEntityMaxStamina'] = readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x18) + 0xF4
        gameStateAddresses['targetedEntityAnimation'] = readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x28) + 0x898
        gameStateAddresses['targetedEntityXaxis'] =  readPointer(readPointer(readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x68) + 0xA8) + 0x40) + 0x70
        gameStateAddresses['targetedEntityZaxis'] = readPointer(readPointer(readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x68) + 0xA8) + 0x40) + 0x74
        gameStateAddresses['targetedEntityYaxis'] = readPointer(readPointer(readPointer(readPointer(readPointer('target_ptr') + 0x1F90)+ 0x68) + 0xA8) + 0x40) + 0x78
    end
    00]]

    return gameStateAddresses

end

function gameState.getCurrentGameState()

    gameStateValues = {}

    if readPointer('BaseB') ~= nill then
        gameStateValues['playerHP']         = readInteger('[[[[BaseB]+0x80]+XA]+0x18]+0xD8')
        gameStateValues['playerMaxHP']      = readInteger('[[[[BaseB]+0x80]+XA]+0x18]+0xDC')
        gameStateValues['playerStamina']    = readInteger('[[[[BaseB]+0x80]+XA]+0x18]+0xF0')
        gameStateValues['playerMaxStamina'] = readInteger('[[[[BaseB]+0x80]+XA]+0x18]+0xF4')
        gameStateValues['playerAnimation']  = readString('[[[[BaseB]+0x80]+XA]+0x28]+0x898',20,true)
        gameStateValues['playerXaxis']      = readFloat('[[[BaseB]+0x40]+0x28]+0x80')
        gameStateValues['playerZaxis']      = readFloat('[[[BaseB]+0x40]+0x28]+0x84')
        gameStateValues['playerYaxis']      = readFloat('[[[BaseB]+0x40]+0x28]+0x88')
    
    else
        gameStateValues['playerHP']         = -1
        gameStateValues['playerMaxHP']      = -1
        gameStateValues['playerStamina']    = -1
        gameStateValues['playerMaxStamina'] = -1
        gameStateValues['playerAnimation']  = -1
        gameStateValues['playerXaxis']      = -1
        gameStateValues['playerZaxis']      = -1
        gameStateValues['playerYaxis']      = -1
    end

    if readPointer('target_ptr') ~= nill then
        entityHP = readInteger('[[[target_ptr] + 0x1F90] + 0x18] + 0xD8')
        if entityHP ~= nill then 
            gameStateValues['targetedEntityHP'] = entityHP

        else
            gameStateValues['targetedEntityHP'] = -1
        end

        entityMaxHP = readInteger('[[[target_ptr] + 0x1F90] + 0x18] + 0xE0')
        if entityMaxHP ~= nill then 
            gameStateValues['targetedEntityMaxHP'] = entityMaxHP

        else
            gameStateValues['targetedEntityMaxHP'] = -1
        end
    end
    --[[
    if readPointer('target_ptr') ~= nil then
        gameStateValues['targetedEntityHP'] = readInteger('[[[target_ptr]+0x1F90]+0x18]+0xD8')
        gameStateValues['targetedEntityMaxHP'] = readInteger('[[[target_ptr]+0x1F90]+0x18]+0xDC')
        gameStateValues['targetedEntityStamina'] = readInteger('[[[target_ptr]+0x1F90]+0x18]+0xF0')
        gameStateValues['targetedEntityMaxStamina'] = readInteger('[[[target_ptr]+0x1F90]+0x18]+0xF4')
        gameStateValues['targetedEntityAnimation']  = readInteger('[[[target_ptr]+0x1F90]+0x28]+0x898')
        gameStateValues['targetedEntityXaxis'] = readInteger('[[[[[target_ptr]+0x1F90]+0x68]+0xA8]+0x40]+0x70')
        gameStateValues['targetedEntityZaxis'] =  readInteger('[[[[[target_ptr]+0x1F90]+0x68]+0xA8]+0x40]+0x74')
        gameStateValues['targetedEntityYaxis'] =  readInteger('[[[[[target_ptr]+0x1F90]+0x68]+0xA8]+0x40]+0x78')

    else
        gameStateValues['targetedEntityHP'] = -1
        gameStateValues['targetedEntityMaxHP'] = -1
        gameStateValues['targetedEntityStamina'] = -1
        gameStateValues['targetedEntityMaxStamina'] = -1
        gameStateValues['targetedEntityAnimation']  = -1
        gameStateValues['targetedEntityXaxis'] = -1
        gameStateValues['targetedEntityZaxis'] = -1
        gameStateValues['targetedEntityYaxis'] = -1
    end
    -]]

    return gameStateValues

end

--[[ Table datatype is reserved for cheat engine internal functions like speedhack--]]
function gameState.setCurrentGameState(listOfStates) 
    gameStateAddresses = readGameStateAddresses()
    
    for _ in pairs(listOfStates) do

        if math.type(listOfStates[_]) == 'integer' then
            writeInteger(gameStateAddresses[_],listOfStates[_])

        elseif math.type(listOfStates[_]) == 'float' then
            writeFloat(gameStateAddresses[_],listOfStates[_])
        
        elseif type(listOfStates[_]) == 'string' then
            writeString(gameStateAddresses[_],listOfStates[_],true)

        end        
    end
end

return gameState

