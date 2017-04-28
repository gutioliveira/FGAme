from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout

from FGAme import listen
from FGAme.kivy_backend import KivyWorld, KivyMainLoop, KivyInput


@listen('key-up', 'up')
def key_up(*args):
    print('key-up')


@listen('key-down', 'down')
def key_down():
    print('key-down')


@listen('mouse-button-down')
def mouse_down(x, y):
    print(x)
    print(y)


@listen('mouse-button-up')
def mouse_up(*args):
    print("zeca")


@listen('mouse-long-press', 'left')
def mouse_long_press(*args):
    print(args)


@listen('long-press', 'x')
def long_press(*args):
    print('x')


class WorldExample(KivyWorld):

    def init_objects(self):
        self.add.circle(20, pos=(100, 110), vel=(300, 0), color='random')
        self.add.aabb(shape=(20, 120), pos=(440, 300), color='random')
        self.add.rectangle(shape=(20, 120), pos=(300, 100), color='red')
        self.add.rectangle(shape=(20, 120), pos=(700, 100), color='red')
        self.add.poly([(100, 100), (200, 100), (200, 200), (50, 200), (75, 125)],
                      vel=(100, 100), pos=(400, 100), color='random')
        self.add.margin()


class FGAmeWidget(RelativeLayout):
    """
    Wraps an FGAme World built with circles.
    """

    def __init__(self, world, fps=60):
        super().__init__()
        self.mainloop = KivyMainLoop(None, KivyInput(), fps, self)
        self.world = world
        self.world.widget = self
        self.world.init_objects()
        Clock.schedule_interval(self.fgame_step, self.mainloop.dt)

    def fgame_step(self, dt):
        self.mainloop.step(self.world)


class FGAmeApp(App):
    """
    Kivy App that runs FGAme simulation.
    """

    def __init__(self, world, widget=None):
        super().__init__()
        self.world = world
        self.widget = widget

    def build(self):
        if self.widget is None:
            self.widget = FGAmeWidget(self.world)
        return self.widget


if __name__ == '__main__':
    FGAmeApp(WorldExample()).run()
