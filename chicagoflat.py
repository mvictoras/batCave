###############################################################
#
# Sample code for CS 526 Fall 2013
# Copyright 2013 by Andrew Johnson, evl, uic
#
# example code integrating osgearth and omegalib
# and overlaying data onto a flat map of the chicago area
#
###############################################################

from math import *
from euclid import *
from omega import *
from cyclops import *

# makes use of python utm converter from https://pypi.python.org/pypi/utm
import utm

# deal with audio
env = getSoundEnvironment()
s_sound = env.loadSoundFromFile("beep", "/menu_sounds/menu_select.wav")

scene = getSceneManager()

# set background to black
scene.setBackgroundColor(Color(0, 0, 0, 1))

# Create a directional light
light1 = Light.create()
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(-1.0, -1.0, -1.0))
light1.setColor(Color(0.5, 0.5, 0.5, 1.0))
light1.setAmbient(Color(0.2, 0.2, 0.2, 1.0))
light1.setEnabled(True)

# Load a static osgearth 'model'
cityModel1 = ModelInfo()
cityModel1.name = "city1"
cityModel1.path = "chicago_yahoo.earth"
scene.loadModel(cityModel1)

# Create a scene object using the loaded model
city1 = StaticObject.create("city1")
city1.getMaterial().setLit(False)

# Load a kmz file

loadedModels = []

def loadKmz(name, filename, mapName):
  model = ModelInfo()
  model.name = name
  model.path = filename
  model.mapName = mapName
  scene.loadModel(model)

  sModel = StaticObject.create(name)
  loadedModels.append(sModel)

  return sModel

absCrimes = loadKmz("absCrimes", "absoluteCrimes.kmz", "city1")
absCrimesTime = loadKmz("absCrimesTime", "absoluteTimezone.kmz", "city1")
#areaAround = loadKmz("areaAround", "areaAround.kmz", "city1")
areaLess = loadKmz("areaLess", "areaLess.kmz", "city1")
areaMore = loadKmz("areaMore", "areaMore.kmz", "city1")
#areaEqual = loadKmz("areaEqual", "areaEqual.kmz", "city1")
#areaZero = loadKmz("areaZero", "areaZero.kmz", "city1")
schools = loadKmz("schools", "schools.kml", "city1")
seriousCrimesPerTract = loadKmz("seriousCrimesPerTract", "seriousCrimesPerTract.kml", "city1")


setNearFarZ(1, 2 * city1.getBoundRadius())

#deal with the camera
cam = getDefaultCamera()
cam.setPosition(city1.getBoundCenter() + Vector3(7768.82, 2281.18, 2034.08))
cam.getController().setSpeed(500)
cam.pitch(3.14159*0.45) #pitch up to start off flying over the city

#set up the scene
all = SceneNode.create("everything")
all.addChild(city1)

for model in loadedModels:
  all.addChild(model)
  model.setVisible(False)

#turn off one of the two maps
city1.setVisible(True)

#handle events from the wand
# left and right buttons shift between the two maps

def handleEvent():
    global userScaleFactor

    e = getEvent()
    if(e.isButtonDown(EventFlags.ButtonLeft)):
        print("Left button pressed")
	city1.setVisible(False)

	#play button sound
	si_sound = SoundInstance(s_sound)
	si_sound.setPosition( e.getPosition() )
	si_sound.setVolume(1.0)
	si_sound.setWidth(20)
	si_sound.play()

    if(e.isButtonDown(EventFlags.ButtonRight)):
        print("Right button pressed")
	city1.setVisible(True)

	#play button sound
	si_sound = SoundInstance(s_sound)
	si_sound.setPosition( e.getPosition() )
	si_sound.setVolume(1.0)
	si_sound.setWidth(20)
	si_sound.play()

# by default user can use the joystick to spin the world and fly
# but a better flying model should be added in

#### MENUS
mm = MenuManager.createAndInitialize()

filters = mm.getMainMenu().addSubMenu("Filters")

filtersContainer = filters.getContainer()
filtersContainer.setLayout(ContainerLayout.LayoutHorizontal)
f1 = Container.create(ContainerLayout.LayoutVertical, filtersContainer)

#absCrimesBtn = Button.create(f1)
#absCrimesBtn.setUIEventCommand( "showAllCrimesSelected( '%value%' )" )
#absCrimesBtn.setText("Show Crimes")
#absCrimesBtn.setCheckable(True)
#absCrimes.setChecked(False)

def createButton(container, kmzObj, text):
  btn = Button.create(container)
  btn.setUIEventCommand( "%s.setVisible(not %s.isVisible())" % (kmzObj, kmzObj))
  #btn.setUIEventCommand( function + "()" )
  btn.setText(text)
  btn.setCheckable(True)
  btn.setChecked(False)

createButton(f1, "absCrimes", "Absolute Nmb of serious crimes")
createButton(f1, "absCrimesTime", "Absolute Nmb of serious crimes per timezone")
#createButton(f1, "areaAround", "Serious crimes compared with the surrounding area")
#createButton(f1, "areaEqual", "Serious crimes compared with the surrounding area (Equal)")
createButton(f1, "areaLess", "Serious crimes compared with the surrounding area (Less)")
createButton(f1, "areaMore", "Serious crimes compared with the surrounding area (More)")
#createButton(f1, "areaZero", "Show surrounding area")
createButton(f1, "schools", "Schools")
createButton(f1, "seriousCrimesPerTract", "Serious crimes per tract")

setEventFunction(handleEvent)
