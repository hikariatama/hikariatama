-- Libraries
local component = require("component")
local fs = require("filesystem")
local serial = require("serialization")
local text = require("text")
local shell = require("shell")
local term = require("term")
-- Componentes
local gpu = component.gpu
local printer = nil
local say = component.chat_box.say
-- Constants
local PROGRESS_BAR_LENGTH = 30
local SCREEN_X, SCREEN_Y = gpu.getResolution()
local WAITING = 2
local COPIES = 1
-- Global variables
local args = shell.parse(...)
-- Functions
function eror()
say("§4Произошла ошибка!")
end
function normalizeModel(model)
  local nModel = {}
  for _, i in pairs(model) do
    if (#i.shapes > 0) then
      table.insert(nModel, i)
    end
  end
  return nModel
end

function getArgumnet(index)
  if ((#args > 0) and (#args >= index)) then
    return args[index]
  else
    return nil
  end
end

function getFile(text)
  if (fs.exists(text)) then
    return text
  else
    if (fs.exists(shell.getWorkingDirectory() .. "/" .. text)) then
      return shell.getWorkingDirectory() .. "/" .. text
    end
  end
  return nil
end

function getModel(path)
  local object
  if (fs.exists(path)) then
    local text = ""
    local file = fs.open(path)
    while true do
      local temp = file:read(9999999)
      if (temp) then
        text = text .. temp
      else
        break
      end
    end
    text2 = "{" .. text .. "}"
    object = serial.unserialize(text2)
    if (object) then
      if (#object > 1) then
      return true, serial.unserialize(text2)
    else
      return true, serial.unserialize(text)
    end
    else
      return false, "Ошибка чтения файла! Файл поврежден!"
    end
  else
    return false, "Файл по указанному пути не найден!"
  end
end

function isValid(model)
  if (model.shapes) then
    return true, "SIMPLE"
  else
    for _, i in pairs(model) do
      if (not i.shapes) then
        return false
      end
    end
    return true, "ADVANCED"
  end
end

function getBar(status)
  local bar = ""
  if (status == 100) then
    for i = 1,PROGRESS_BAR_LENGTH do
      bar = bar .. "="
    end
  else
    local one = 100 / PROGRESS_BAR_LENGTH
    local prg = status / one
    for i = 1,prg do
      bar = bar .. "="
    end
    bar = text.padRight(bar, PROGRESS_BAR_LENGTH)
  end
  return bar
end

function write(text)
  local x, y = term.getCursor()
  term.setCursor(1, y)
  term.write(text)
end

function drawStatus(modelName, count, status, length)

end

function setupShapes(shapes)
  for _, shape in pairs(shapes) do
    printer.addShape(shape[1], shape[2], shape[3], shape[4], shape[5], shape[6], shape.texture, shape.state, shape.tint)
  end
end

function setupPrinter(model, count)
  printer.reset()
  if (model.label) then printer.setLabel(model.label) end
  if (model.tooltip) then printer.setTooltip("[" .. count .. "] " .. model.tooltip) else printer.setTooltip("[" .. count .. "]") end
  if (model.emitRedstone) then printer.setRedstoneEmitter(model.emitRedstone) end
  if (model.buttonMode) then printer.setButtonMode(model.buttonMode) end
  if (model.shapes) then setupShapes(model.shapes) end
end

function printModel(model, count, length)
  setupPrinter(model, count)
  local status, valid = printer.status()
  if (not valid) then
    if (#model.shapes > printer.getMaxShapeCount()) then
      eror()
    else
      eror()
    end
  else
    drawStatus(model.label, count, -1, length)
    os.sleep(WAITING)
    if (not printer.commit(1)) then
      return false, "В принтере закончились материалы для создания 3D модели."
    end
    while true do
      local status, progress = printer.status()
      if (status == "idle") then
        drawStatus(model.label, count, 100, length)
        break
      elseif (status == "busy") then
        drawStatus(model.label, count, progress, length)
      end
    end
  end
  return true, 1
end

function printModels(models)
  for i, model in pairs(models) do
    local status, reason = printModel(model, i, string.len(tostring(#models)))
    if (not status) then
      return false, i, model.label, reason
    end
  end
  return true, #models
end

-- Check system requirements
if (getArgumnet(3)) then COPIES = tonumber(getArgumnet(3)) end
if (COPIES > 1) then say("§2Печать §4" .. COPIES .. " §2копий.") end

for i = 1,COPIES do
  if (not component.isAvailable("printer3d")) then
    eror()
  else
    printer = component.printer3d
    if (getArgumnet(2)) then WAITING = tonumber(getArgumnet(2)) end
    if (getArgumnet(1)) then
      local file = getFile(getArgumnet(1))
      if (file) then
        local status, model = getModel(file)
        if (status) then
          local status, modelType = isValid(model)
          if (status) then       
            if (modelType == "ADVANCED") then
              if (not getArgumnet(4)) then
                say("§2Печать...")
                local status, count, name, reason = printModels(normalizeModel(model))
                if (status) then
                   say("§6Печать завершена.")
                else
                end
              else
                say("§2Печать...")
              local status, reason = printModel(normalizeModel(model)[tonumber(getArgumnet(4))], tonumber(getArgumnet(4)), string.len(getArgumnet(4)))
              if (status) then
                say("§6Печать завершена!")
              else
              end
              end
            elseif (modelType == "SIMPLE") then
              say("§2Печать...")
              local status, reason = printModel(model, 1, 1)
              if (status) then
                say("§6Печать завершена!")
              else
              end
            end
          else
            eror()
          end
        else
          eror()
        end
      else
        eror()
      end
    else
      eror()
    end
  end
end
