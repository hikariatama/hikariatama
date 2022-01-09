-----Librares-----
local event = require("event")
local term = require("term")
-----Components-----
local gpu = require("component").gpu
-----Constants-----
local lessons = {"Русский", "Ф-ра", "История", "Лит-ра", "Мат-ка", "English", "Труд", "Русский", "Русский", "English", "Лит-ра", "Мат-ка", "История", "Deutsch", "Обществознание", "Музыка", "Мат-ка", "География", "Русский", "Русский", "Ф-ра", "English", "English", "Мат-ка", "Русский", "Лит-ра", "Ф-ра", "Биология", "Мат-ка", "English"}
local days = {"Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"}
local months = {"января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"}
local image = {"  *__Π_____*。* ", "*/________/~\\ *", "*| 田田田 | |"}
image = {"      oooO              ", "     (    )    Oooo     ", "      )  /    (    )    ", "     (_/       )  /     ", "               (_/      "}
-----Functions-----
function sort(a,b)         
	if a > b then 
		return true; 
	else 
		return false; 
	end
end
function printColored(text, col)
gpu.setForeground(col)
print(text)
gpu.setForeground(0xFFFFFF)
end
function loading(time)
	w = width-time
	w = w/2
	local temp = width-time
	temp = temp%2/2
	w = w+temp
	local back1, back2 = term.getCursor()
	gpu.fill(1, 1, width, height, " ")
	gpu.setForeground(0xFF0000)
	term.setCursor(w, height/2)
	io.write("[")
	for i = 1, time do
		io.write("■")
		os.sleep(0.05)
	end
	io.write("]")
	gpu.fill(1, 1, width, height/2, " ")
	term.setCursor(w, height/2)
	gpu.setForeground(0x00FF00)
	io.write("[") for i = 1, time do io.write("■") end io.write("]")
	term.setCursor(back1, back2)
end
function showLessonList(r, t)
	gpu.setBackground(0x333333)
	gpu.fill(1, 1, width, height, " ")
	seconds_since_epoch = os.time()
	date = os.date("!*t", seconds_since_epoch)
	local day = tonumber(date.wday) - 1
	n = 1
	term.setCursor(r+3, t-1)
	printColored("Сегодня, "..days[day], 0x0000FF)
	term.setCursor(r+30, t-1)
	printColored("Завтра, "..days[day+1], 0xFF00FF)
	if day == 1 then for i = 1, 6 do if dz[n] == nil or dz[n] == "" then dz[n] = "не указано" end term.setCursor(r, t+n) print(n..". "..lessons[i]) n = n + 1 end n = 1 for i = 7, 12 do term.setCursor(r+27, t+n) print(n..". "..lessons[i].." - "..dz[n]) n = n + 1 end
		elseif day == 2 then for i = 7, 12 do if dz[n] == nil or dz[n] == "" then dz[n] = "не указано" end term.setCursor(r, t+n) print(n..". "..lessons[i]) n = n + 1  end n = 1 for i = 13, 18 do term.setCursor(r+27, t+n) print(n..". "..lessons[i].." - "..dz[n]) n = n + 1  end
			elseif day == 3 then for i = 13, 18 do if dz[n] == nil or dz[n] == "" then dz[n] = "не указано" end term.setCursor(r, t+n) print(n..". "..lessons[i]) n = n + 1  end n = 1 for i = 19, 24 do term.setCursor(r+27, t+n) print(n..". "..lessons[i].." - "..dz[n]) n = n + 1  end
				elseif day == 4 then for i = 19, 24 do if dz[n] == nil or dz[n] == "" then dz[n] = "не указано" end term.setCursor(r, t+n) print(n..". "..lessons[i]) n = n + 1  end n = 1 for i = 25, 30 do term.setCursor(r+27, t+n) print(n..". "..lessons[i].." - "..dz[n]) n = n + 1  end
					elseif day == 5 then for i = 25, 30 do if dz[n] == nil or dz[n] == "" then dz[n] = "не указано" end term.setCursor(r, t+n) print(n..". "..lessons[i]) n = n + 1 end term.setCursor(r+28, t+1) print("В этот день нет уроков!")
						elseif day == 6 then term.setCursor(r, t+1) print("В этот день нет уроков!") term.setCursor(r+28, t+1) print("В этот день нет уроков!")
	end
	gpu.setForeground(0xFFFFFF)
	local o = height-#image-5
	for i = 1, #image-1 do
		if #image[i] > #image[i + 1] then
			max = #image[i]
		end
	end
	local number = max
	print(max)
	-- for i = 1, #image do
	-- 	term.setCursor(width/2-number, o)
	-- 	print(image[i])
	-- 	o = o + 1
	-- end
end
function getTime()
	seconds_since_epoch = os.time()
	date = os.date("!*t", seconds_since_epoch)
	if tonumber(date.hour) < 10 then hour = "0"..tostring(date.hour) else hour = tostring(date.hour) end
	if tonumber(date.min) < 10 then min = "0"..tostring(date.min) else min = tostring(date.min) end
	if tonumber(date.sec) < 10 then sec = "0"..tostring(date.sec) else sec = tostring(date.sec) end
	return hour..":"..min..":"..sec
end
function getDate()
	seconds_since_epoch = os.time()
	date = os.date("!*t", seconds_since_epoch)
	if tonumber(date.year) < 10 then year = "0"..tostring(date.year) else year = tostring(date.year) end
	return tonumber(date.day).." "..months[tonumber(date.month)].." "..year
end
-----Code-----
width, height = gpu.getResolution()
loading(10)
n = 1
dz = {}
seconds_since_epoch = os.time()
date = os.date("!*t", seconds_since_epoch)
local day = tonumber(date.wday) - 1
if day == 1 then for i = 7, 12 do io.write("Введите д\\з по предмету: "..lessons[i].." - ") dz[n] = io.read() n = n + 1 end
	elseif day == 2 then for i = 13, 18 do io.write("Введите д\\з по предмету: "..lessons[i].." - ") dz[n] = io.read() n = n + 1 end
		elseif day == 3 then for i = 19, 24 do io.write("Введите д\\з по предмету: "..lessons[i].." - ") dz[n] = io.read() n = n + 1 end
			elseif day == 4 then for i = 25, 30 do io.write("Введите д\\з по предмету: "..lessons[i].." - ") dz[n] = io.read() n = n + 1 end
				elseif day == 5 then io.write("На завтра д\\з не задано.") answer = io.read() end
while true do
	showLessonList(width/2-30, height/2-10)
	gpu.setForeground(0xFF0000) term.setCursor(width-9, height-1) print(getTime())
	gpu.setForeground(0x00FF00) term.setCursor(3, height-1) print(getDate())
	local eventType = event.pull(1)
	if eventType == "touch" then
		local eventType = event.pull(1)
		if eventType == "touch" then
				gpu.setBackground(0x000000)
				gpu.fill(1, 1, width, height, " ")
				term.setCursor(1, 1)
				break
		end
	end
end
