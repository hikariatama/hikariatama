local str = 0
local i = 0
local err = false
local strNumber = 7
local component = require("component")
local event = require("event")
local term = require("term")
local gpu = component.gpu
local say = component.chat_box.say
local name = component.chat_box.setName
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
local Width, Height = gpu.getResolution()
gpu.setResolution(150, 51)
name("§6Bot§7")
function printMenu()
gpu.setResolution(30, 16)
gpu.setForeground(0x9999999)
term.setCursor(1, 2)
print("+----------------------------+")
print("|     Информационный стенд   |")
print("|                            |")
print("|  + Добавить строку         |")
print("|  - Удалить строку          |")
print("|  •Просмотр.                |")
print("|============================|")
print("|                            |")
print("|                            |")
print("|                            |")
print("|                            |")
print("|                            |")
print("|                            |")
print("|                            |")
print("+----------------------------+")
end

function menu()
local eventType,MonitorAdress,x,y,_,plr = event.pull(0)
if eventType == "touch" then
if x >= 4 and x <= 20 and y == 4 then
	if not err then
say("§3Введите текст строки")
end
str = str + 1
strNumber = strNumber + 1
term.setCursor(2, strNumber)
if str1 == nil then
	str1 = io.read()
	elseif str2 == nil then
		str2 = io.read()
		elseif str3 == nil then
			str3 = io.read()
			elseif str4 == nil then
				str4 = io.read()
				elseif str5 == nil then
					str5 = io.read()
end
if str > 5 then
say("§4Достигнуто макс. кол-во строк")
err = true
end
if #str1 > 30 then
say("§rВведено слишком много символов! (макс.30)")
gpu.setResolution(150, 51)
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
gpu.fill(1, 1, 150, 51, " ")
os.exit()
end
if err == false then
say("§2Строка добавлена!")
end
end
if x >= 4 and x <= 19 and y == 5 then
str = str - 1
strNumber = strNumber - 1
if strNumber == 6 then strNumber = 7 end
if str5 ~= nil then
str5 = nil
	elseif str4 ~= nil then
		str4 = nil
		elseif str3 ~= nil then
			str3 = nil
			elseif str2 ~= nil then
				str2 = nil
				elseif str1 ~= nil then
					str1 = nil
gpu.fill(1, 1, 30, 16, " ") end
printMenu()
print("+----------------------------+")
print("|     Информационный стенд   |")
print("|                            |")
print("|  + Добавить строку         |")
print("|  - Удалить строку          |")
print("|  •Просмотр.                |")
print("|============================|")
if str1 ~= nil then print("|"..str1) else print("|                            |") end
if str2 ~= nil then print("|"..str2) else print("|                            |") end
if str3 ~= nil then print("|"..str3) else print("|                            |") end
if str4 ~= nil then print("|"..str4) else print("|                            |") end
if str5 ~= nil then print("|"..str5) else print("|                            |") end
print("|                            |")
print("|                            |")
print("+----------------------------+")
if str1 ~= nil and str2 ~= nil and str3 ~= nil and str4 ~= nil and str5 ~= nil then
say("§4Строка удалена")
else end end
if x >= 4 and x <= 12 and y == 6 then
if str1 ~= nil then
say("§2Показ вкл.")
gpu.setForeground(0xFFFFFF)
gpu.setBackground(0x000000)
local w, h = gpu.getResolution()
gpu.fill(1, 1, w, h, " ")
gpu.setResolution(#str1, 1)
os.sleep(0.1)
function touch()
local eventType,_,_,_,_,_ = event.pull(0)
if eventType == "touch" then
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
w, h = gpu.getResolution()
gpu.fill(1, 1, w, h, " ")
gpu.setResolution(150, 51)
term.setCursor(1, 1)
os.exit()
end
end
if str5 ~= nil then
while true do
touch()
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str1, 1)
term.setCursor(1, 1)
io.write(str1)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str2, 1)
term.setCursor(1, 1)
io.write(str2)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str3, 1)
term.setCursor(1, 1)
io.write(str3)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str4, 1)
term.setCursor(1, 1)
io.write(str4)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str5, 1)
term.setCursor(1, 1)
io.write(str5)
touch()
os.sleep(2)
end
elseif str4 ~= nil then
while true do
touch()
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str1, 1)
term.setCursor(1, 1)
io.write(str1)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str2, 1)
term.setCursor(1, 1)
io.write(str2)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str3, 1)
term.setCursor(1, 1)
io.write(str3)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str4, 1)
term.setCursor(1, 1)
io.write(str4)
touch()
os.sleep(2)
end
elseif str3 ~= nil then
while true do
touch()
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str1, 1)
term.setCursor(1, 1)
io.write(str1)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str2, 1)
term.setCursor(1, 1)
io.write(str2)
touch()
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str3, 1)
term.setCursor(1, 1)
io.write(str3)
touch()
os.sleep(2)
end

elseif str2 ~= nil then
while true do
gpu.fill(1, 1, i, 1, " ")
os.sleep(2)
gpu.setResolution(#str1, 1)
term.setCursor(1, 1)
io.write(str1)
os.sleep(2)
gpu.fill(1, 1, i, 1, " ")
gpu.setResolution(#str2, 1)
term.setCursor(1, 1)
io.write(str2)
os.sleep(2)
end

elseif str1 ~= nil then
io.write(str1)
while true do
touch()
end
end

else say("§4Вы не добавили не одну строку!") end end end end
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
gpu.fill(1, 1, Width, Height, " ")
gpu.setResolution(150, 51)
printMenu()
while true do
menu() 
end




