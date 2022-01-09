-------------------------------------------------------------------------------
local component = require("component")
local event = require("event")
local term = require("term")
local say = component.chat_box.say
local name = component.chat_box.setName
local delay = os.sleep
local no = "false"
local owner = "utevaugu36"
local blacklist = {}
local err = false
local err2 = false
local err3 = false
local gpu = component.gpu
local w, h = gpu.getResolution()
local length = 0
-------------------------------------------------------------------------------
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
gpu.fill(1, 1, w, h, " ")
name("§6Bot§7")
say("§4+----§rutevaugu36§4---+")
say("§4|    §6Прослушка чата    §4|")
say("§4+-----§rMcskill.ru§4----+")
term.setCursor(1, 1)
-------------------------------------------------------------------------------
while true do
err = false
err2 = false
local _,_,plr,msg = event.pull("chat_message")

if msg == "-blacklist add" or msg == "-bl add" and plr == owner then
  say("§rВведите ник игрока, которого вы хотите добавить в черный список")
  local _,_,plar,msg = event.pull("chat_message")
  if plar == plr then
  if blacklist ~= nil then
      for i = 1, #blacklist do
        if blacklist[i] == msg then
          say("§rЭтот игрок уже присутствует в черном списке!")
          err = true
  end
end
end
if err == false then
if blacklist == nil then length = 0 end
if blacklist == nil then blacklist = {"nil"} end
blacklist[length + 1] = msg
say("§4"..msg.."§r успешно добавлен в черный список!")
  end
end
else
	local _,_,plar,msg = event.pull("chat_message")
end

if msg == "-blacklist list" or msg == "-bl list" and plr == owner then
if blacklist == nil or #blacklist == 0 then
say("§rВ черном списке нет §4ни одного игрока§r!")
else
say("§4+--------------------------+")
for i = 1, #blacklist do
say("§r          [§4"..i.."§r] - §"..math.random(0,9)..blacklist[i])
end
say("§4+--------------------------+")
  end
end

if msg == "-blacklist clear" or msg == "-bl clear" and plr == owner then
say("§rВы уверены что хотите удалить §4всех игроков§r из черного списка?")
local _,_,player,message = event.pull("chat_message")
if message == "yes" or message == "y" or message == "-yes" or message == "Да" or message == "да" then
blacklist = nil
local blacklist = {"nil"}
say("§2Черный список очищен!")
end 
if message == "n" or message == "no" or message == "not" or message == "No" or message == "Not" or message == "Нет" or message == "нет" then
say("§4Отменено!")
  end 
end

if msg == "-bl help" or message == "'=blacklist help" and plr == owner then
say("§4+--------------------------+")
say("§1  Список доступных команд:")
say("§4-bl list")
say("§6-bl clear")
say("§2-bl add")
say("§9-bl remove")
say("§4+--------------------------+")
end

if msg == "-debug mode" and plr == owner then
if #blacklist == 0 or blacklist == nil then
say("§rВ черном списке нет §4ни одного игрока§r")
else
say("§4+-------blacklist----------+")
for i = 1, #blacklist do
say("§r          [§4"..i.."§r] - §"..math.random(0,9)..blacklist[i])
end
say("§4+--------------------------+")
  end
say("§4"..plr)
say("§9----------------------------")
say("§2"..msg)
end

if msg == "-blacklist remove" or msg == "-bl remove" and plr == owner then
if blacklist ~= nil then
  err2 = false
  say("§rВведите ник игрока, которого вы хотите удалить из черного списка")
  local _,_,plr,msg = event.pull("chat_message")
    for i = 1, #blacklist do
      if blacklist[i] == msg then
        blacklist[i] = nil
        say("§4"..msg.."§r успешно удален из черного списка!")
        err2 = true
  end
end
if err2 == false then
say("§rДанного игрока нету в черном списке!")
err2 = true
  		end
  		else
	say("§rВ черном списке нету §4ни одного игрока§r!")
	end
end
--------------------------------------------------------------------------
no = "false"
if blacklist ~= nil  then
for i = 1, #blacklist do
if blacklist[i] == plr then no = "true" end
end
end
err3 = false
local blacklist = {"nil"}
if err3 == false then
	if msg == "-bl add" then
		elseif msg == "-bl remove" then
			elseif msg == "-bl help" then
				elseif msg == "-bl list" then
					elseif msg == "-bl clear" then
						elseif msg == "-blacklist add" then
							elseif msg == "-blacklist remove" then
								elseif msg == "-blacklist help" then
									elseif msg == "-blacklist list" then
										elseif msg == "-blacklist clear" then
											print("Команда: "..plr..": "..msg)
										else
if no == "false" then
		print("Прослушка: "..plr..": "..msg)
		end
	end
end
if blacklist == nil then
local blacklist = {"nil"}
	end
end
