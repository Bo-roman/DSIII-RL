local myModuleFolder = ';'..lfs.currentdir()..'\\DS3LRLUALibs\\?.lua'
package.path = package.path..myModuleFolder

local PORT = 64502
local gameState = require('currentGameState')
local dsSocket = require('dsSockets')

function setCurrentGameState(client)
    if client == nil then
        return
    end

    Object = dsSocket.recvDSRLObject(client)
    if tableLength == 0 then
        print("Error receiving")
        client:close()
        return nil
    end
    print(object)
    gameState.setCurrentGameState(Object)
    client:close()

end

serverThread = CreateThread(function()
    dsSocket.createServer(PORT,setCurrentGameState)
end)

