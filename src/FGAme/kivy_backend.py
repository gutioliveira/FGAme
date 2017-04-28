from FGAme.input import Input
from FGAme import World
from FGAme import Circle, AABB, Rectangle as FGAmeRectangle, Poly
from FGAme.mainloop import MainLoop

from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle, Rotate, PushMatrix, PopMatrix, Translate
from kivy.graphics.tesselator import Tesselator
from kivy.graphics import Mesh

from math import pi

import time

from functools import singledispatch

from queue import Queue

class KivyInput(Input):

    def __init__(self):
        super(KivyInput, self).__init__()
        self.events = Queue()
        ## algumas teclas possuem nomes diferentes
        self.keys = {v: k for k, v in Window._system_keyboard.keycodes.items()}
        Window.bind(on_key_up=self.add_on_key_up)
        Window.bind(on_key_down=self.add_on_key_down)
        Window.bind(on_touch_down=self.add_on_touch_down)
        # Window.bind(on_touch_move=self.add_on_touch_move)
        Window.bind(on_touch_up=self.add_on_touch_up)
        self.hold_mouse = True
        self.hold_key = True

    
    def poll(self):

        while not self.events.empty():
            event = self.events.get()
            if event.type == 'key-up':
                self.process_key_up(event.key)
            elif event.type == 'key-down':
                self.process_key_down(event.key)
            elif event.type == 'long-press':
                self.process_long_press()
            elif event.type == 'mouse-button-down':
                self.process_mouse_button_down('left', event.pos)
            elif event.type == 'mouse-button-up':
                self.process_mouse_button_up('left', event.pos)
            elif event.type == 'mouse-long-press':
                self.process_mouse_longpress()

    def add_on_key_up(self, *args):
        self.events.put(Event('key-up', self.keys[args[1]], None))
        self.hold_key = True

    def add_on_key_down(self, *args):

        if self.hold_key:
            self.events.put(Event('key-down', self.keys[args[1]], None))
            self.hold_key = False

        self.events.put(Event('long-press', self.keys[args[1]], None))

    def add_on_touch_down(self, *args):

        self.hold_mouse = True

        self.events.put(Event('mouse-button-down', None, args[1].pos))

        if self.hold_mouse == True:
            import threading

            def work():
                while self.hold_mouse == True:
                    self.events.put(Event('mouse-long-press', None, args[1].pos))
                    time.sleep(0.1)

            t = threading.Thread(target=work)
            t.daemon = True
            t.start()

    def add_on_touch_up(self, *args):
        self.events.put(Event('mouse-button-up', None, args[1].pos))
        self.hold_mouse = False

class Event:

    def __init__(self, type, key, pos):
        self.type = type
        self.key = key
        self.pos = pos

class KivyObjectWrapper:
    def __init__(self, obj_fgame, obj_kivy, translation=None, rotation=None):
        self.obj_fgame = obj_fgame
        self.obj_kivy = obj_kivy
        self.translation = translation
        self.rotation = rotation
        self.initial_pos = obj_fgame.pos

class KivyWorld(World):

    def __init__(self, widget=None):
        super().__init__()
        self.widget = widget
        self.objects = []

    def _add(self, obj, layer=0):
        super()._add(obj, layer)
        register_to_canvas(obj, self)

    def update(self, dt):
        super().update(dt)
        for obj in self.objects:
            if isinstance(obj.obj_fgame, FGAmeRectangle) or isinstance(obj.obj_fgame, Poly):
                obj.translation.x = obj.obj_fgame.pos.x - obj.initial_pos.x
                obj.translation.y = obj.obj_fgame.pos.y - obj.initial_pos.y
                obj.rotation.angle = obj.obj_fgame.theta * 180.0 / pi
            else:
                obj.obj_kivy.pos = obj.obj_fgame.pos_sw


@singledispatch
def register_to_canvas(obj, world):
    pass

@register_to_canvas.register(Circle)
def _(obj, world):
    with world.widget.canvas:
        diameter = 2 * obj.radius
        Color(*obj.color.rgbf)
        kcircle = Ellipse(pos=obj.pos_sw, size=(diameter,diameter))
        world.objects.append(KivyObjectWrapper(obj, kcircle))


@register_to_canvas.register(AABB)
def _(obj, world):
    with world.widget.canvas:
        Color(*obj.color.rgbf)
        krectangle = Rectangle(pos=obj.pos_sw,size=(obj.xmax-obj.xmin,obj.ymax-obj.ymin))
        world.objects.append(KivyObjectWrapper(obj, krectangle))

@register_to_canvas.register(Poly)
def _(obj, world):
    tess = Tesselator()
    vertices = []
    for x,y in obj.vertices:
        vertices.append(x)
        vertices.append(y)
    tess.add_contour(vertices)
    if not tess.tesselate():
        raise Exception('Tesselator didn\'t work')
    with world.widget.canvas:
        Color(*obj.color.rgbf)
        PushMatrix()
        translation = Translate(0,0)
        rotation = Rotate(axis=(0, 0, 1), origin=(obj.pos.x, obj.pos.y, 0))
        for vertices, indices in tess.meshes:
            Mesh(vertices=vertices,indices=indices,mode="triangle_fan")
        PopMatrix()
        world.objects.append(KivyObjectWrapper(obj, tess, translation, rotation))

@register_to_canvas.register(FGAmeRectangle)
def _(obj, world):
    with world.widget.canvas:
        PushMatrix()
        translation = Translate(0,0)             
        rotation = Rotate(axis=(0, 0, 1), origin=(obj.pos.x, obj.pos.y, 0))
        Color(*obj.color.rgbf)
        krectangle = Rectangle(pos=obj.pos_sw, size=(obj.xmax-obj.xmin,obj.ymax-obj.ymin))
        PopMatrix()
        world.objects.append(KivyObjectWrapper(obj, krectangle, translation, rotation))

class KivyMainLoop(MainLoop):

    def __init__(self, screen, input, fps=None, widget=None):
        super().__init__(screen, input, fps)
        self.widget = widget

    def step_screen(self, world):
        pass

    def sleep(self, dt):
        pass