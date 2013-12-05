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

mi = ModelInfo()
mi.name = "defaultSphere"
mi.path = "sphere.obj"
scene.loadModel(mi)

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
cityModel1.path = "chicago_flat.map.earth"
scene.loadModel(cityModel1)

# Create a scene object using the loaded model
city1 = StaticObject.create("city1")
city1.getMaterial().setLit(False)

# Load a kmz file
searsModel = ModelInfo()
searsModel.name = "SearsTower"
searsModel.path = "absoluteTimezone.kmz"
searsModel.mapName = "city1"
scene.loadModel(searsModel)

sears = StaticObject.create("SearsTower")

setNearFarZ(1, 2 * city1.getBoundRadius())

# add another version with a different type of map
cityModel2 = ModelInfo()
cityModel2.name = "city2"
#cityModel2.path = "chicago_flat.sat.earth"
cityModel2.path = "chicago_yahoo.earth"
scene.loadModel(cityModel2)

# Create a scene object using the second loaded model
city2 = StaticObject.create("city2")
city2.getMaterial().setLit(False)

#deal with the camera
cam = getDefaultCamera()
cam.setPosition(city1.getBoundCenter() + Vector3(7768.82, 2281.18, 2034.08))
cam.getController().setSpeed(500)
cam.pitch(3.14159*0.45) #pitch up to start off flying over the city

#set up the scene
all = SceneNode.create("everything")
all.addChild(city1)
all.addChild(city2)
all.addChild(sears)

#turn off one of the two maps
city1.setVisible(False)

#handle events from the wand
# left and right buttons shift between the two maps

def handleEvent():
    global userScaleFactor

    e = getEvent()
    if(e.isButtonDown(EventFlags.ButtonLeft)):
        print("Left button pressed")
	city1.setVisible(False)
	city2.setVisible(True)

	#play button sound
	si_sound = SoundInstance(s_sound)
	si_sound.setPosition( e.getPosition() )
	si_sound.setVolume(1.0)
	si_sound.setWidth(20)
	si_sound.play()

    if(e.isButtonDown(EventFlags.ButtonRight)):
        print("Right button pressed")
	city2.setVisible(False)
	city1.setVisible(True)

	#play button sound
	si_sound = SoundInstance(s_sound)
	si_sound.setPosition( e.getPosition() )
	si_sound.setVolume(1.0)
	si_sound.setWidth(20)
	si_sound.play()

# by default user can use the joystick to spin the world and fly
# but a better flying model should be added in
#absoluteCrimes.kmz                                                                                          100%  553KB  92.2KB/s   00:06
#absoluteTimezone.kml                                                                                                      100% 9935KB 124.2KB/s   01:20
#absoluteTimezone.kmz                                                                                                      100%  559KB 139.8KB/s   00:04
#areaAround.kmz                                                                                                            100%  476KB 475.6KB/s   00:01
#areaEqual.kmz                                                                                                             100%  114KB 113.6KB/s   00:01
#areaLess.kmz                                                                                                              100%  411KB 137.0KB/s   00:03
#areaMore.kmz                                                                                                              100%  135KB 135.5KB/s   00:00
#areaZero.kmz                                                                                                              100%  983KB 491.5KB/s   00:02
#CTABusArea.kmz                                                                                                            100% 3364KB  15.9KB/s   03:32
#schools.kml                                                                                                               100% 1028KB  15.1KB/s   01:08
#timezone.kmz
setEventFunction(handleEvent)
