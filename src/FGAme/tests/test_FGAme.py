import pytest
import FGAme


def test_project_defines_author_and_version():
    assert hasattr(FGAme, '__author__')
    assert hasattr(FGAme, '__version__')


#TODO: PUT THIS ON OTHER FILE LATER
from FGAme import conf
from FGAme import World, Circle
from FGAme.backends.kivy_be import KivyWorld
import sys

def test_kivy_backend():
	assert 'kivy' in conf._backends

def test_kivy_world_instance_backend_testing():
	from FGAme.backends.kivy_be import kivy_world
	assert kivy_world == None

def test_kivy_world_instance_backend_kivy():
	world = World()
	_kivy_world = KivyWorld(world)
	this = sys.modules['FGAme.backends.kivy_be']
	this.kivy_world = _kivy_world
	from FGAme.backends.kivy_be import kivy_world
	assert kivy_world is not None

def test_kivy_objects():
	world = World()
	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
	_kivy_world = KivyWorld(world)
	assert _kivy_world.objects[0].obj_fgame == world._objects[0]

def test_kivy_add_objects():
	world = World()
	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
	_kivy_world = KivyWorld(world)
	this = sys.modules['FGAme.backends.kivy_be']
	this.kivy_world = _kivy_world
	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
	assert len(_kivy_world.objects) == len(world._objects)

def test_kivy_remove_objects():
	world = World()
	c = Circle(20, pos=(100, 110), vel=(300, 0), color='random')
	world.add(c)
	_kivy_world = KivyWorld(world)
	this = sys.modules['FGAme.backends.kivy_be']
	this.kivy_world = _kivy_world
	world.remove(c)
	assert len(_kivy_world.objects) == len(world._objects)

def test_kivy_simulation():
	world = World()
	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
	_kivy_world = KivyWorld(world)
	assert _kivy_world._simulation == world._simulation