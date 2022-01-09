--=======================================--
--     Smart House или Control Panel     --
--   Copyright (c) utevaugu36 2017 год   --
--=======================================--
-----Librares-----
local component = require("component")
local event = require("event")
local term = require("term")
local buffer = require("doubleBuffering")
local GUI = require("GUI")
local api = require("api")
local warp = "paradise"
local msgs = {}
-----Constants-----
local ports = {{6667, false}, {35565, false}, {12345, false}}
local allowed = {"e51", "83f7"}
local say = component.chat_box.say
local send = component.modem.broadcast
local modem = component.modem
local bridge = component.openperipheral_bridge
for i = 1, #ports, 1 do modem.open(ports[i][1]) end
color = math.random(0x000000, 0xFFFFFF)
for i = 1, 10, 1 do
  msgs[i] = bridge.addText(5, 20 + i*10, "", color)
  msgs[i].setScale(1)
end
msgs[1].setText("Приятного пользования!")
bridge.sync()
os.sleep(3)
bridge.clear()
bridge.sync()
-----Variables-----
function glMsg(msg, number)
	temp = bridge.addText(5, 20 + number*10, "", color)
  	temp.setScale(1)
	temp.setText(msg)
	bridge.sync()
end
function separator() say("§4=§6=§e=§2=§9=§1=§5=§4=§6=§e=§2=§9=§1=§5=§4=§6=§e=§2=§9=§1=§5=§4=§4=§6=§e=§2=§9=§1=§5=§4=§6=§e=§2=§9=§1=§5=§4=§6=§e=§2=§9=§1=§5=§4=") end
local suggestions = {}
local secretSuggestions = {}
local orders = {}
local players = {}
local admins = {"utevaugu36"}

local powers = {tree = false, farm = false, reactor = false}
local statuses = {farm = "выкл.", tree = "выкл.", reactor = "Готовы к работе"}
local colors = {farm = 0xFF0000, tree = 0xFF0000, reactor = 0x00FF00}
-----Initialisation-----
api.license()
component.chat_box.setName("§5Discord§7")
component.modem.open(620)
local mainContainer = GUI.fullScreenContainer()
-----Code-----
mainContainer:addChild(GUI.panel(1, 1, mainContainer.width, mainContainer.height, 0x2D2D2D))
local menu = mainContainer:addChild(GUI.menu(1, 1, mainContainer.width, 0xEEEEEE, 0x666666, 0x3366CC, 0xFFFFFF, nil))
menu:addItem("Smart House", 0x000000)
mainContainer:addChild(GUI.framedButton(10, 4, 8, 3, 0xFFFFFF, 0x555555, 0x880000, 0xFFFFFF, "On\\off"))
mainContainer:addChild(GUI.framedButton(10, 8, 8, 3, 0xFFFFFF, 0x555555, 0x880000, 0xFFFFFF, "On\\off"))
mainContainer:addChild(GUI.framedButton(10, 12, 8, 3, 0xFFFFFF, 0x555555, 0x880000, 0xFFFFFF, "On\\off"))
mainContainer:addChild(GUI.roundedButton(3, 46, 15, 3, 0xFFFFFF, 0x555555, 0x880000, 0xFFFFFF, "Принудительно"))
mainContainer:draw()
buffer.draw(true)
term.setCursor(2, 5) component.gpu.setForeground(0xFF9900) io.write("Лесоруб")
term.setCursor(2, 9) component.gpu.setForeground(0x990099) io.write("Фермер")
term.setCursor(2, 13) component.gpu.setForeground(0xFFFF00) io.write("Р") component.gpu.setForeground(0x000000) io.write("e") component.gpu.setForeground(0xFFFF00) io.write("а") component.gpu.setForeground(0x000000) io.write("к") component.gpu.setForeground(0xFFFF00) io.write("т") component.gpu.setForeground(0x000000) io.write("о") component.gpu.setForeground(0xFFFF00) io.write("р") component.gpu.setForeground(0x000000) io.write("ы")
while true do
	local eventType,_,x,y,_,message = event.pull(1)
	if eventType == "touch" then
		if api.clickedAtArea(x, y, 10, 4, 18, 7) then --Лесоруб вкл\выкл
			if powers["tree"] == true then
				powers["tree"] = false
				for i = 1, 20 do
					send(111, "treeOFF")
					local eventType,_,_,_,_,message = event.pull(1) if eventType == "modem_message" and message == "treeOFF" then break end
				end
				say("§8[§7Smart house§8] §6Лесоруб §cвыключен")
			elseif powers["tree"] == false then powers["tree"] = true send(111, "treeON") say("§8[§7Smart house§8] §6Лесоруб §aвключен")
			end
		end
		if api.clickedAtArea(x, y, 10, 8, 18, 11) then --Фермер вкл\выкл
			if powers["farm"] == true then
				powers["farm"] = false
				say("§8[§7Smart house§8] §5Фермер §cвыключен")
				for i = 1, 20 do
					send(222, "farmOFF")
					local eventType,_,_,_,_,message = event.pull(1) if eventType == "modem_message" and message == "farmOFF" then break end
				end
			elseif powers["farm"] == false then powers["farm"] = true send(222, "treeON")
			local eventType,_,_,_,_,message = event.pull(3) if eventType == "modem_message" and message == "treeON" then say("§8[§7Smart house§8] §6Лесоруб (экспонат) §aвключен") else say("§8[§7Smart house§8] §4Невозможно установить связь с §6Лесоруб (экспонат)!") end
			end
		end
		if api.clickedAtArea(x, y, 10, 12, 18, 15) then --Реакторы вкл\выкл
			if powers["reactor"] == true then powers["reactor"] = false say("§8[§7Smart house§8] §6Реакторы §cвыключены") component.redstone.setOutput(require("sides").up, 0)
			elseif powers["reactor"] == false then powers["reactor"] = true say("§8[§7Smart house§8] §6Реакторы §aвключены") component.redstone.setOutput(require("sides").up, 15)
			end
		end
		if api.clickedAtArea(x, y, 3, 46, 18, 49) then --Аварийная остановка
			send(111, "treeOFF")
			send(222, "treeOFF")
			powers["tree"] = false
			powers["farm"] = false
			colors["tree"] = 0xFF0000
			colors["farm"] = 0xFF0000
			statuses["tree"] = "выкл."
			statuses["farm"] = "выкл."
			say("§8[§7Smart house§8] §4Все системы успешно отключены!")
			for i = 1, 20 do
				local eventType,_,_,_,_,message = event.pull(1) if eventType == "modem_message" and message == "treeOFF" then break elseif eventType == "modem_message" and message == "burOFF" then break end
			end
		end
	end
	if eventType == "modem_message" then --Если получено сообщение
		if message == "treeON" then powers["tree"] = true statuses["tree"] = "вкл." colors["tree"] = 0x00FF00
		elseif message == "treeONn" then powers["tree"] = false statuses["tree"] = "Готов к работе" colors["tree"] = 0x00FF00
		elseif message == "treeOFF" then powers["tree"] = false statuses["tree"] = "выкл." colors["tree"] = 0xFF0000
		elseif message == "charging" then statuses["tree"] = "Зарядка мотыги..." powers["tree"] = true colors["tree"] = 0x00FF00
		elseif message == "sapling" then statuses["tree"] = "Ожидание саженцов..." powers["tree"] = true colors["tree"] = 0x9900FF
		elseif message == "droppingtreeloot" then statuses["tree"] = "Выгрузка..." powers["tree"] = true colors["tree"] = 0x9900FF
			elseif message == "farmON" then powers["farm"] = true statuses["farm"] = "вкл." colors["farm"] = 0x00FF00
		elseif message == "farnONn" then powers["farm"] = false statuses["farm"] = "Готов к работе" colors["farm"] = 0x00FF00
		elseif message == "farmOFF" then powers["farm"] = false statuses["farm"] = "выкл." colors["farm"] = 0xFF0000
		elseif message == "droppingfarmloot" then statuses["farm"] = "Выгрузка..." powers["farm"] = true colors["farm"] = 0x9900FF
		elseif message:find("tree") == 1 then tmp = api.breakText(message) for i = 1, 4 do table.remove(tmp, 1) end result = tonumber(table.concat(tmp)) statuses["tree"] = "Рубка... Цикл номер "..result powers["tree"] = true colors["tree"] = 0xFF9900
		elseif message:find("2tree") == 1 then tmp = api.breakText(message) for i = 1, 5 do table.remove(tmp, 1) end result = tonumber(table.concat(tmp)) statuses["farm"] = "Рубка... Цикл номер "..result powers["farm"] = true colors["farm"] = 0xFF9900
		end
	end
	plr = x
	msg = y
	if eventType == "chat_message" then
		for i = 1, #admins do
			if plr == admins[i] then
				player_type = "admin"
			end
		end
		if msg == "-order list" and player_type == "admin" then
			for i = 1, #orders do
				say("§8[§3/warp §5"..warp.."§8] "..orders[i])
			end
		elseif msg == "-suggestion list" and player_type == "admin" then
			for i = 1, #secretSuggestions do
				say("§8[§3/warp §5"..warp.."§8] "..secretSuggestions[i])
			end
		elseif msg == "-отзывы" then
			separator()
			for i = 1, #suggestions do
				say(suggestions[i])
			end
			separator()
		elseif msg == "-update glasses" then
			bridge.clear()
			for i = 1, #orders do
				glMsg(orders[i], i)
				os.sleep(1)
			end
		elseif msg:find("-show") == 1 and player_type == "admin" then
			tmp = api.breakText(msg)
			for i = 1, 6 do
				table.remove(tmp, 1)
			end
			suggestion = table.concat(tmp)
			table.insert(suggestions, secretSuggestions[tonumber(suggestion)])
			say("§8[§3/warp §5"..warp.."§8] §aОтзыв §8[§c"..secretSuggestions[tonumber(suggestion)].."§8] §aуспешно опубликован.")
			table.remove(secretSuggestions, tonumber(suggestion))
		elseif y:find("-заказ") == 1 then
			tmp = api.breakText(msg)
			for i = 1, 12 do
				table.remove(tmp, 1)
			end
			order = table.concat(tmp)
			result = plr..": §9"..order
			if #orders < 10 then
				say("§8[§3/warp §5"..warp.."§8] §aВаш заказ принят и скоро будет §aрассмотрен §cадминистраторами §aварпа")
				orders[#orders+1] = result
				bridge.clear()
				for i = 1, #orders do glMsg(orders[i], i) end
			else
				say("§8[§3/warp §5"..warp.."§8] §cВ связи с загруженностью §aадминистраторов §cварпа, ваш заказ отклонен!")
			end
		elseif y:find("-complete") == 1 and player_type == "admin" then
			tmp = api.breakText(msg)
			for i = 1, 10 do
				table.remove(tmp, 1)
			end
			order = table.concat(tmp)
			table.remove(orders, order)
			say("§8[§3/warp §5"..warp.."§8] §aЗаказ §c№"..order.." §aвыполнен.")
			bridge.clear()
			for i = 1, #orders do glMsg(orders[i], i) end

		elseif y:find("-отзыв") == 1 then
			tmp = api.breakText(msg)
			for i = 1, 12 do
				table.remove(tmp, 1)
			end
			suggestion = table.concat(tmp)
			result = plr..": §9"..suggestion
			say("§8[§3/warp §5"..warp.."§8] §aВаш отзыв принят и скоро будет §aрассмотрен §cадминистраторами §aварпа")
			secretSuggestions[#secretSuggestions+1] = result
		elseif msg == "-close" and player_type == "admin" then
			event.ignore("chat_message", console)
			say("§cПрограмма остановлена.")
		elseif msg == "-?" then
			say("§4-заказ - §cзаказать товар.")
			say("§6-отзыв - §eоставить отзыв.")
			say("§2-отзывы - §aпосмотреть отзывы.")
		elseif y:find("-shell execute") == 1 and player_type == "admin" then
			local tmp = api.breakText(cmd1)
			for i = 1, 15 do table.remove(tmp, 1) end
			local result = table.concat(tmp)
			say("§c-----Вывод программы-----")
			require("shell").execute(result)
			say("§c-----Конец вывода программы-----")
		end
	end
	if powers["tree"] == true then
		term.setCursor(25, 5)
		component.gpu.setForeground(0xFF9900)
		io.write("Лесоруб")
		component.gpu.setForeground(0x11FF11)
		io.write(" вкл. ")
	else
		term.setCursor(25, 5)
		component.gpu.setForeground(0xFF9900)
		io.write("Лесоруб")
		component.gpu.setForeground(0xFF1111)
		io.write(" выкл.")
	end
	if powers["farm"] == true then
		term.setCursor(25, 9)
		component.gpu.setForeground(0x9900FF)
		io.write("Лесоруб2")
		component.gpu.setForeground(0x11FF11)
		io.write(" вкл. ")
	else
		term.setCursor(25, 9)
		component.gpu.setForeground(0x9900FF)
		io.write("Лесоруб2")
		component.gpu.setForeground(0xFF1111)
		io.write(" выкл.")
	end
	if powers["reactor"] == true then
		term.setCursor(25, 13) component.gpu.setForeground(0xFFFF00) io.write("Р") component.gpu.setForeground(0x000000) io.write("e") component.gpu.setForeground(0xFFFF00) io.write("а") component.gpu.setForeground(0x000000) io.write("к") component.gpu.setForeground(0xFFFF00) io.write("т") component.gpu.setForeground(0x000000) io.write("о") component.gpu.setForeground(0xFFFF00) io.write("р") component.gpu.setForeground(0x000000) io.write("ы")
		component.gpu.setForeground(0x11FF11)
		io.write(" вкл. ")
		statuses["reactor"] = "Генерирует..."
		colors["reactor"] = 0xFFFF00
	else
		term.setCursor(25, 13) component.gpu.setForeground(0xFFFF00) io.write("Р") component.gpu.setForeground(0x000000) io.write("e") component.gpu.setForeground(0xFFFF00) io.write("а") component.gpu.setForeground(0x000000) io.write("к") component.gpu.setForeground(0xFFFF00) io.write("т") component.gpu.setForeground(0x000000) io.write("о") component.gpu.setForeground(0xFFFF00) io.write("р") component.gpu.setForeground(0x000000) io.write("ы")
		component.gpu.setForeground(0xFF1111)
		io.write(" выкл.")
		statuses["reactor"] = "выкл."
		colors["reactor"] = 0xFF0000
	end
	local width, height = component.gpu.getResolution()
	component.gpu.fill(40, 5, width, 9, " ")
	component.gpu.setForeground(0x1111FF) term.setCursor(40, 5) io.write("Статус: ")
	component.gpu.setForeground(colors["tree"])
	io.write(statuses["tree"])
	component.gpu.setForeground(0x1111FF) term.setCursor(40, 9) io.write("Статус: ")
	component.gpu.setForeground(colors["farm"])
	io.write(statuses["farm"])
	component.gpu.setForeground(0x1111FF) term.setCursor(40, 13) io.write("Статус: ")
	component.gpu.setForeground(colors["reactor"])
	io.write(statuses["reactor"])
end

