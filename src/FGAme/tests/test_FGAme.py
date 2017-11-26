import pytest
import FGAme

@pytest.yield_fixture
def kivy(world):
	from FGAme.backends import kivy_be
	kivy_be.kivy_world = kivy_be.KivyWorld(world)
	yield kivy_be

	kivy_be.kivy_world = None

@pytest.fixture
def world():
	world = World()
	return world


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
	from FGAme.backends.kivy_be import KivyWorld, KivyInput
	from FGAme.world.world import get_last_world_instance
	assert isinstance(get_last_world_instance(),World)

# def test_kivy_world_instance_backend_kivy():
# 	world = World()
# 	_kivy_world = KivyWorld(world)
# 	from FGAme.backends import kivy_be
# 	kivy_be.kivy_world = _kivy_world	
# 	from FGAme.backends.kivy_be import kivy_world
# 	assert kivy_be.kivy_world is not None

def test_kivy_objects():
	world = World()
	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
	_kivy_world = KivyWorld(world)
	assert _kivy_world.objects[0].obj_fgame == world._objects[0]

def test_kivy_add_objects():
	world = World()
	world.add.circle(20)
	_kivy_world = KivyWorld(world)
	assert len(_kivy_world.objects) == len(world._objects)

# def test_kivy_remove_objects():
# 	world = World()
# 	c = Circle(20, pos=(100, 110), vel=(300, 0), color='random')
# 	world.add(c)
# 	_kivy_world = KivyWorld(world)
# 	this = sys.modules['FGAme.backends.kivy_be']
# 	this.kivy_world = _kivy_world
# 	world.remove(c)
# 	assert len(_kivy_world.objects) == len(world._objects)

# def test_kivy_simulation():
# 	world = World()
# 	world.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
# 	_kivy_world = KivyWorld(world)
# 	assert _kivy_world._simulation == world._simulation