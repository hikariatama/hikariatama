-----Librares-------pastebin run ryhyXUKZ--Download Librares
local component = require("component")
local event = require("event")
local shell = require("shell")
local term = require("term")
local fs = require("filesystem")
local api = require("api")
local matrix = require("matrix")
-----Constants-----
local likedplayer = "utevaugu36"
local chat = component.chat_box
local gpu = component.gpu
local say = chat.say
local name = chat.setName
name("§4Console§7")
-----Variables-----
local prefixes = 8
local orders = {} local customers = {}
local power, powerlisten = false, false
local ignoreList = {"Штопковольт", "Мира", "Старик Райз", "Лория"}
local models = {"kupon", "telega", "afsu", "akame_girl", "apple", "balloon", "bath", "bee", "book", "burger", "click_sofa", "clock", "deer_head", "dog", "doodler", "duck", "flower", "fox", "gifts", "girlanda", "gold_cart", "happy_new_year", "headphones", "heart", "horse_head", "kassa", "mario", "mouse", "notebook", "old_man", "orange_girl", "overwatch", "poisons", "pokeball", "pringles", "printer", "pult", "qgen", "radio", "rock", "rocket", "sapling", "sofa", "solar7", "sword", "washing_machine", "yellow_girl", "youtube"}
local colors = {}
local winners = {}
local prefixList = {"§9Думбльдур", "§3Пингвин", "§2Помогатор", "§9Букля", "§aТехушка", "§6К§2актус", "§4Коммунист§6СС§4ахалина", "§6Пися"}
local clearPrefixList = {"utevaugu36", "Tequila1337", "Dycedarg", "Crazy_doter", "SkyDrive_", "CaMpeRGoLD", "DulKey", "Yew"}
local adminList = {"utevaugu36"}
-----Images-----
local house = {"  *__Π___*。* ", "*/______/~\\ *", "*|田田 . .|門| |"}
local foot = {"§7....§8oooO§7..............", "§7.....§8(....)§7...§8Oooo§7...", "§7......§8)../§7.....§8(....)§7...", "§7.....§8(_/§7.......§8)../§7.....", "§7...............§8(_/§7......"}
local cat = {"       ／＞　 フ", "　　　　　| 　_　 _|", "　 　　　／`ミ _x 彡", "　　 　 /　　　 　 |", "　　　 /　 ヽ　　 ﾉ", "　／￣|　　 |　|　|", "　| (￣ヽ＿_ヽ_)_)", "　＼二つ"}
-----Functions-----
function ask(ask, answer1, answer2)
	say(ask)
	while true do
		_,_,plr,msg = event.pull("chat_message")
		if msg == answer1 or msg == answer2 then
			break
		end
	end
	say("§c"..plr.."§2 ответил верно")
	winners[#winners+1] = plr
end
local urls = {}
function getModels()
	say("§2Получение списка моделей")
	os.sleep(0.5)
	say("§5Инициализация")
	for i = 1, #models do
		urls[i] = "http://d620.win/models/"..models[i]
	end
	os.sleep(0.5)
	say("§6Скачивание...")
	for i = 1, #models do
		loadfile("/bin/wget.lua")(urls[i], "/home/"..models[i], "-fq")
	end
	say("§2Скачивание §4"..#models.." §2файлов завершено! Печать...")
	for i = 1, #models do
		shell.execute("3d "..models[i].." 2 5")
	end
	say("§2Печать завершена! Выставляйте на продажу ^.^")
end
gpu.setResolution(150, 51)
local o = 1
local iter = 1
function show(l, l, plr, msg)
	local messageType = "default"
	for i = 1, #ignoreList do
		if plr == ignoreList[i] then
			messageType = "ignore"
		end
	end
	if messageType ~= "ignore" then
		for i = 1, prefixes do
			if clearPrefixList[i] == plr then
				local temp = api.breakText(msg)
				while temp[1] == " " do
					table.remove(temp, 1)
				end
				if string.find(msg, "!") == 1 then
					while true do 
						if temp[1] == " " or temp[1] == "!" then
							table.remove(temp, 1)
						else
							break
						end
					end
					for i = 1, #temp do
						if temp[i] == "&" then
							temp[i] = "§"
						end
					end
					msg = table.concat(temp)
					messageType = "!prefix"
					pref = i
				else
					for i = 1, #temp do
						if temp[i] == "&" then
							temp[i] = "§"
						end
					end
					msg = table.concat(temp)
					messageType = "prefix"
					pref = i
				end
			end
		end
	end
	if messageType == "ns" then
		local temp = api.breakText(msg)
		while temp[1] == " " do
			table.remove(temp, 1)
		end
		if string.find(msg, "!") == 1 then
			while true do
				if temp[1] == " " or temp[1] == "!" then
					table.remove(temp, 1)
				else
					break
				end
			end
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			messageType = "!default"
		else
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			messageType = "default"
		end
	end
	if messageType ~= "ignore" then
		if messageType == "!default" then
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			api.smartText(1, o, "§8[§6G§8] §7"..plr..": §7"..msg)
		elseif messageType == "default" then
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			api.smartText(1, o, "§8[§2§fL§8] §7"..plr..": §7"..msg)
		elseif messageType == "!prefix" then
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			api.smartText(1, o, "§8[§6G§8] §8[§r"..prefixList[pref].."§8] §7"..plr..": §7"..msg)
		elseif messageType == "prefix" then
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			api.smartText(1, o, "§8[§2§fL§8] §8[§r"..prefixList[pref].."§8] §7"..plr..": §7"..msg)
		end
		if iter >= 51 then
			o = 1
			iter = 0
			gpu.fill(1, 1, 150, 51, " ")
		end
		o = o + 1
		iter = iter + 1
	end
end
function chat(_, _, plr, msg)
	date = os.date("!*t", seconds_since_epoch)
	local time = date.hour..":"..date.min
	tmp = false
	temp = {}
	for i = 1, #ignoreList do
		if plr == ignoreList[i] then
			tmp = true
		end
	end 
	for i = 1, prefixes do
		if plr == clearPrefixList[i] then
		tmp = true
		if msg:find("!") ~= 1 then
			name("§fL§7")
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			if plr == "utevaugu36" then 
				tmp = false
				for i = 1, prefixes do
					if likedplayer == clearPrefixList[i] then
						tmp = true
						if msg:find("!") ~= 1 then
							name("§fL§7")
							local temp = api.breakText(msg)
							for i = 1, #temp do
								if temp[i] == "&" then
									temp[i] = "§"
								end
							end
							msg = table.concat(temp)
							say("§8["..prefixList[i].."§8] §7"..likedplayer..": §f"..msg)
						end
					end
				end
				if tmp == false then say("§7"..likedplayer..": §f"..msg) end
			else
				say("§8["..prefixList[i].."§8] §7"..plr..": §f"..msg) end
			end
		end
	end
	if tmp == false then
		if msg:find("!") ~= 1 then
			local temp = api.breakText(msg)
			for i = 1, #temp do
				if temp[i] == "&" then
					temp[i] = "§"
				end
			end
			msg = table.concat(temp)
			name("§3"..time.."§7")
			say(plr..": §f"..msg)
		end
	end
end
function separator()
	say("§4=§6=§2=§3=§1=§5=§4=§6=§2=§3=§1=§5=§4=§6=§2=§3=§1=§5=§4=§6=§2=§3=§1=§5=")
end
function checker(_,_,plr,cmd1)
	if clearPrefixList == nil then
		clearPrefixList = {}
	end
	if prefixList == nil then
		prefixList = {}
	end
	local ran = math.random(1, 5)
	if cmd1 == "-привет" then
		if ran == 1 then
			say("§2Хаюшки ^.^")
		elseif ran == 2 then
			say("§2Здравствуйте")
		elseif ran == 3 then
			say("§2Привет")
		elseif ran == 4 then
			say("§2Дарова")
		elseif ran == 5 then
			say("§2Пребывай в добром здравии, путник.")
	end
	elseif cmd1 == "-яндекс" then
		name("§4Я§0ндекс§r")
		if ran == 1 then
			say("§rА?Что?Где?Когда?")
		elseif ran == 2 then
			say("§rЯ здесь!")
		elseif ran == 3 then
			say("§rЯ здеся")
		elseif ran == 4 then
			say("§rХотите что-то спросить?")
		elseif ran == 5 then
			say("§rConsole.WriteLine(\"Привет\")")
		end
	elseif cmd1 == "-гугл" then
		name("§1G§4o§6o§1g§2l§4e§7")
		if ran == 1 then
			say("§rА?Что?Где?Когда?")
		elseif ran == 2 then
			say("§rЯ здесь!")
		elseif ran == 3 then
			say("§rЯ здеся")
		elseif ran == 4 then
			say("§rХотите что-то спросить?")
		elseif ran == 5 then
			say("§rConsole.WriteLine(\"Привет\")")
		end
	elseif cmd1 == "==money" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				say("§2[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]")
				admin = true
				end
			end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "==foot" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				for i = 1, #foot do
					say(foot[i])
				end
				admin = true
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "==love" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				say("§4♥")
				admin = true
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1:find("-prefix del") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local temp = api.breakText(cmd1)
				for i = 1, 12 do
					table.remove(temp, 1)
				end
				local del = table.concat(temp)
				table.remove(prefixList, tonumber(del))
				table.remove(clearPrefixList, tonumber(del))
				say("§2Successfully")
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-bl clear" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				ignoreList = {}
				say("§2§nSuccessfully!")
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-colors" then
		for i = 0, 9 do
			say("§"..i.."&"..i)
		end
		say("§a&a")
		say("§b&b")
		say("§c&c")
		say("§d&d")
		say("§e&e")
		say("§f&f")
		say("§m&m")
		say("§n&n")
		say("§l&l")
	elseif cmd1 == "-chatshow on" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				say("§2Слушаюсь, мой повелитель!")
				event.ignore("chat_message", show)
				event.ignore("chat_message", chat)
				event.listen("chat_message", chat)
				matrix.start()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-chatshow off" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				say("§2Слушаюсь, мой повелитель!")
				event.ignore("chat_message", chat)
				event.listen("chat_message", show)
				matrix.stop()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-price list" then
		separator()
		say("§13§4D §2модель в 1 блок - 2 эма")
		say("§13§4D §2надпись в 1 блок - 2 эма")
		separator()
	elseif cmd1 == "-?" then
		separator()
		say("§c-заказ [заказ] - Заказать §13§4D§c модель")
		say("§9-price list - Список цен")
		say("§a-colors - Числовые коды цветов чата")
		separator()
	elseif cmd1 == "-прослушка" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				if powerlisten == false then
					event.listen("chat_message", show)
					say("§3Прослушка §aвключена!")
					powerlisten = true
					matrix.stop()
				else
					say("§3Прослушка §cвыключена!")
					powerlisten = false
					event.ignore("chat_message", show)
					event.ignore("chat_message", chat)
					matrix.start()
				end
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-exit" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				close()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-prefix list" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				separator()
				for i = 1, prefixes do
					say("§f"..i..". §8[§f"..prefixList[i].."§8] §r"..clearPrefixList[i])
				end
				separator()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-bl list" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				separator()
				for i = 1, #ignoreList do
					say("§"..math.random(1, 9)..ignoreList[i])
				end
				separator()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-order list" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				separator()
				for i = 1, #customers do
					say("§4"..customers[i].."§2: §5"..orders[i])
				end
				separator()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1:find("-morph") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				tmp = api.breakText(cmd1)
				for i = 1, 7 do
					table.remove(tmp, 1)
				end
				likedplayer = table.concat(tmp)
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-getModels" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				getModels()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-bl add") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local temp = api.breakText(cmd1)
				for i = 1, 8 do
					table.remove(temp, 1)
				end
				result = table.concat(temp)
				ignoreList[#ignoreList+1] = result
				say("§4"..result.."§2 успешно добавлен")
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-bl remove") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local temp = api.breakText(cmd1)
				for i = 1, 11 do
					table.remove(temp, 1)
				end
				result = table.concat(temp)
				tmp1 = false
				for i = 1, #ignoreList do
					if ignoreList[i] == result then
						table.remove(ignoreList, i)
						tmp1 = true
						say("§4"..result.."§2 успешно удален")
					end
				end
				if tmp1 == false then
					say("§4Данного игрока нету в чс!")
				end
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-prefix set") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				temp = api.breakText(cmd1)
				temp2 = api.breakText(cmd1)
				for i = 1, 12 do
					table.remove(temp, 1)
					table.remove(temp2, 1)
				end
				while temp2[1] ~= " " do
					table.remove(temp2, 1)
				end
				table.remove(temp2, 1)
				while temp[#temp] ~= " " do
					table.remove(temp, #temp)
				end
				table.remove(temp, #temp)
				for i = 1, #temp2 do
					if temp2[i] == "&" then
						temp2[i] = "§"
					end
				end
				for i = 1, #temp2 do
					if temp2[i] == "_" then
						temp2[i] = " "
					end
				end
				prefix = table.concat(temp2)
				nick = table.concat(temp)
				local tmp5 = false
				for i = 1, prefixes do
					if clearPrefixList[i] == nick then
						say("§4"..nick.." §2§n§lуже §f§2имеет префикс! Будет произведена замена.")
						table.remove(clearPrefixList, i)
						clearPrefixList[prefixes] = nick
						table.remove(prefixList, i)
						prefixList[prefixes] = prefix
						tmp5 = true
					end
				end
				if tmp5 == false then
					prefixList[#prefixList+1] = prefix
					clearPrefixList[prefixes+1] = nick
					say("§2Теперь у игрока §4"..nick.." §2будет префикс §8[§f"..prefix.."§8]")
					prefixes = prefixes + 1
				end
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-pex give") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local temp = api.breakText(cmd1)
				for i = 1, 10 do
					table.remove(temp, 1)
				end
				tmp = false
				for i = 1, #adminList do
					if adminList[i] == table.concat(temp) then
						tmp = true
						say("§2"..table.concat(temp).." §cуже администратор")
					end
				end
				if tmp == false then
					adminList[#adminList+1] = table.concat(temp)
					say("§2"..table.concat(temp).." §cназначен администратором")
				end
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-pex take") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local temp = api.breakText(cmd1)
				for i = 1, 10 do
					table.remove(temp, 1)
				end
				tmp = false
				for i = 1, #adminList do
					if adminList[i] == table.concat(temp) then
						tmp = true
						say("§2"..adminList[i].." §cснят с администрации")
						table.remove(adminList, i)
					end
				end
				if tmp == false then
					say("§2"..table.concat(temp).." §cне является администратором")
				end
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif string.find(cmd1, "-заказ") == 1 and cmd1 ~= "-заказ" then
		local temp = api.breakText(cmd1)
		for i = 1, 12 do
			table.remove(temp, 1)
		end
		result = table.concat(temp)
		orders[#orders+1] = result
		customers[#customers+1] = plr
		say("§2Ваш идиотский заказ принят и скоро будет рассмотрен §cадминистраторами §2варпа.")
	elseif cmd1:find("-shell execute") == 1 then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				local tmp = api.breakText(cmd1)
				for i = 1, 15 do
					table.remove(tmp, 1)
				end
				local result = table.concat(tmp)
				say("§c-----Вывод программы-----")
				shell.execute(result)
				say("§c-----Конец вывода программы-----")
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	elseif cmd1 == "-admin list" then
		admin = false
		for i = 1, #adminList do
			if plr == adminList[i] or plr == "utevaugu36" then
				admin = true
				separator()
				for i = 1, #adminList do
					say("§f"..i..". §"..math.random(1, 9)..adminList[i])
				end
				separator()
			end
		end
		if admin == false then
			say("§4Permission denied")
		end
	end
end
local width, height = gpu.getResolution()
gpu.fill(1, 1, width, height, " ")
function close(_,_,_,key)
	if key == 28 then
		event.ignore("chat_message", show)
		event.ignore("chat_message", chat)
		event.ignore("key_down", close)
		event.ignore("chat_message", checker)
		gpu.fill(1, 1, width, height, " ")
		term.setCursor(1, 1)
		gpu.setBackground(0x333333)
		os.reboot()
	end
end
event.listen("key_down", close)
event.listen("chat_message", checker)
-----Code-----
api.license()
