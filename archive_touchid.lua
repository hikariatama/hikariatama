local component = require("component")
local sides = require("sides")
local term = require("term")
local event = require("event")
local chat = component.chat_box
local say = chat.say
local name = chat.setName
local gpu = component.gpu
local owner = "utevaugu36" 
local w, h = gpu.getResolution()
local red = component.redstone.setOutput
function clearScreen()
w, h = gpu.getResolution()
gpu.fill(1, 1, w, h, " ")
term.setCursor(1, 1)
end
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
clearScreen()
function loading()
print("Загрузка")
for i = 1, 3 do
os.sleep(0.5)
print(".")
os.sleep(0.5)
print(".")
os.sleep(0.5)
print(".")
os.sleep(0.5)
local X, Y = term.getCursor()
gpu.fill(9, Y, w, h, " ")
os.sleep(0.3)
term.setCursor(9, Y)
end
print(" завершена!")
end
-- loading()
gpu.fill(1, 1, w, h, " ")
gpu.setBackground(0x000000)
clearScreen()
gpu.setResolution(14, 9)
function printPassword(color)
gpu.setForeground(color)
term.setCursor(1, 2)
print("    ######")
print("  ##      ##")
print("##    ###   ##")
print("##    ###   ##")
print("##    ###   ##")
print("  ##      ##")
print("    ######")
end
printPassword(0xFFFFFF)
while true do
local eventType,MonitorAdress,x,y,_,plr = event.pull(0)
while eventType == "touch" do
printPassword(0xFFFFFF)
if plr == owner then
	say("§2Доступ разрешен!")
	clearScreen()
	printPassword(0x119911)
	os.sleep(1)
	printPassword(0xFFFFFF)
	eventType = nil
	break
end
if plr ~= owner then
	say("§4Доступ запрещен!")
	clearScreen()
	printPassword(0x991111)
		os.sleep(1)
	printPassword(0xFFFFFF)
	eventType = nil
end
os.sleep(1)
clearScreen()
end
if eventType == "touch" then
gpu.setBackground(0x333333)
gpu.setForeground(0xFFFFFF)
clearScreen()
break
end
end
gpu.setResolution(150, 51)
gpu.setForeground(0xFFFFFF)


