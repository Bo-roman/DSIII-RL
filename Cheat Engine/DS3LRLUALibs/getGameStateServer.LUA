local myModuleFolder = ';'..lfs.currentdir()..'\\DS3LRLUALibs\\?.lua'
package.path = package.path..myModuleFolder

local PORT = 64501
local gameState = require('currentGameState')
local dsSocket = require('dsSockets')

function sendCurrentGameState(client)
    if client == nil then
        return
    end

    dsSocket.sendDSRLObject(client,gameState.getCurrentGameState())
    client:close()

end

serverThread = CreateThread(function()
    dsSocket.createServer(PORT,sendCurrentGameState)
end)

