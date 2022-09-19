package.path = package.path..';lua\\?.lua'
package.cpath = package.cpath..';clibs64\\mime\\?.dll'

local Socket = {}

function Socket.connectToServer(ip,port)
         local socket = require('socket')
         local tcp = assert(socket.tcp())
         tcp:connect(ip,port)
         return tcp
end

function Socket.createServer(port,callback)
         local socket = require('socket')
         local server = assert(socket.bind('*',port))
         local client
	       local clientThread
	       server:settimeout(nil)
         while 1 do
               client = server:accept()
               if client ~= nil then
                  createThread(function()
                    callback(client)
                  end)
               end
         end

end

--[[
We define a function that sends messages to an endpoint

It first sends the message length followed by an end-mark '@' symbol
then it sends the message
--]]
function sendMessageToClient(client,message)
         local messageLength = string.len(message)
         client:send(tostring(messageLength)..'@')
         client:send(message)
end

--[[
  msgObject = {
            dataType;
            message;
  }
--]]

function sendObjectToClient(client,dataType,name,message)
         sendMessageToClient(client,dataType)
         sendMessageToClient(client,name)
         sendMessageToClient(client,message)
end

function tableLength(T)
  local count = 0
  for _ in pairs(T) do
      count = count + 1
  end
  return count
end

function Socket.sendDSRLObject(client,tableObject)
         --[[sending the table length --]]
         local tableObjectLength = tableLength(tableObject)

         if tableObjectLength == 0 then return -1 end

         sendObjectToClient(client,'integer','_length',tableObjectLength)


         --[[for every entry in the table we send it to the other endpoint
             if we enounter another table in it we will send again another table
         --]]

         local currentDataType = ''

         for _ in pairs(tableObject) do

             if type(tableObject[_]) == 'number' then
                currentDataType = math.type(tableObject[_])
             else
                 currentDataType = type(tableObject[_])
             end

             sendObjectToClient(client,currentDataType,_,tostring(tableObject[_]))

         end

end

function recvMessage(client)
        local sReceivedMessageLength = ''
        local msg,err,part

        while sReceivedMessageLength:sub(-1) ~= '@' do
               msg,err,part = client:receive(1)
               if msg ~= nil then
                  sReceivedMessageLength = sReceivedMessageLength..msg
               elseif part ~= nil then
                  sReceivedMessageLength = sReceivedMessageLength..part
               elseif err == 'closed' then
                  return ''
               end
        end
        
        sReceivedMessageLength = sReceivedMessageLength:sub(1,-2)
        msg,err,part = client:receive(tonumber(sReceivedMessageLength))

        if msg ~= nil then
              return msg
        elseif part ~= nil then
              return part
          end

        return ''
end

function recvObjectFromClient(client)
        dataType = recvMessage(client)
        name = recvMessage(client)
        rawMessage = recvMessage(client)
        message = ''
        Object = {}

        if(dataType == '' or name == '' or rawMessage == '') then
          return {}
        end

        if dataType == 'integer' or dataType == 'float' then
            message = tonumber(rawMessage)
        else
            message = rawMessage
        end

        Object['dataType'] = dataType
        Object['name'] = name
        Object['message'] = message


        return Object
end

function placeholder() 
    return 0
end

function Socket.recvDSRLObject(client)
    DSRLObject = {}
    currentObject = {}
    DSRLObjectLength = tonumber(recvObjectFromClient(client)['message'])
    if DSRLObjectLength == nil or DSRLObjectLength == 0 then
      return {}
    end

    for i=0,DSRLObjectLength - 1,1 do
        currentObject = recvObjectFromClient(client)
        if currentObject['message'] ~= nil then
          DSRLObject[currentObject['name']] = currentObject['message']
        end
    end       

    return DSRLObject
    
end

return Socket

