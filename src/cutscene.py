import logging
log = logging.getLogger(__name__)

import pyglet
import math


LINEAR = 0
COSINE = 1


class Cutscene(pyglet.event.EventDispatcher):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.images = {}
        self.active_motions = set()
        self.finished_motions = set()
        self.layers = []
        self.time = 0.0
        self.setup()
        pyglet.clock.schedule_interval(self.update, 0.05)

    def setup(self):
        pass

    def add_image(self, name, image_file, layer=1):
        img = pyglet.resource.image(image_file)
        while len(self.layers) <= layer:
            self.layers.append(pyglet.graphics.OrderedGroup(len(self.layers)))
        self.images[name] = pyglet.sprite.Sprite(
            img, batch=self.batch, group=self.layers[layer]
        )
        self.images[name].visible = False

    def hide(self, dt, image_name):
        """ Hide a sprite. """
        self.images[image_name].visible = False

    def show(self, dt, image_name, x=None, y=None):
        """ Show a sprite, optionally specifying new coordinates. """
        if x is not None:
            self.images[image_name].x = x
        if y is not None:
            self.images[image_name].y = y
        self.images[image_name].visible = True

    def swap(self, dt, image_a, image_b, hide_a=False):
        """ Swap the positions of two sprites. """
        if hide_a:
            self.hide(image_a)
        i_a = self.images[image_a]
        i_b = self.images[image_b]
        # Swap the positions.
        i_a.x, i_a.y, i_b.x, i_b.y = i_b.x, i_b.y, i_a.x, i_a.y

    def move(self, dt, image_name, x, y, duration, algorithm=LINEAR):
        if algorithm == LINEAR:
            motion = LinearMotion(self.images[image_name], x, y, duration)
        elif algorithm == COSINE:
            motion = CosineMotion(self.images[image_name], x, y, duration)
        motion.push_handlers(self)
        motion.setup()
        self.active_motions.add(motion)

    def tint(self, dt, image_name, r, g, b, duration, algorithm=LINEAR):
        if algorithm == LINEAR:
            tint = LinearTint(self.images[image_name], r, g, b, duration)
        elif algorithm == COSINE:
            tint = CosineTint(self.images[image_name], r, g, b, duration)
        tint.push_handlers(self)
        tint.setup()
        self.active_motions.add(tint)

    def update(self, dt):
        for motion in self.active_motions:
            motion.update(dt)
        self.active_motions -= self.finished_motions
        self.finished_motions = set()
        self.batch.draw()

    def do(self, what, when, *args, **kwargs):
        pyglet.clock.schedule_once(what, when, *args, **kwargs)

    def add_trigger(self, trigger):
        self.push_handlers(trigger)

    def tick(self, dt):
        self.time += dt
        self.dispatch_event('on_tick', self, self.time)

    def on_finish(self, motion):
        self.finished_motions.add(motion)

Cutscene.register_event_type('on_tick')
Cutscene.register_event_type('on_end')
Cutscene.register_event_type('on_begin')


class Motion(pyglet.event.EventDispatcher):
    def __init__(self, target, x, y, duration, relative=True):
        self.target = target
        self.x = x
        self.y = y
        self.relative = relative
        self.duration = duration
        self.time = 0.0
        self.start_x = None
        self.start_y = None

    def setup(self, time_offset=0.0):
        self.start_x = self.target.x
        self.start_y = self.target.y
        self.time = time_offset

    @property
    def end_x(self):
        if self.relative:
            return self.start_x + self.x
        else:
            return self.x

    @property
    def end_y(self):
        if self.relative:
            return self.start_y + self.y
        else:
            return self.y

    @property
    def delta_x(self):
        return self.end_x - self.start_x

    @property
    def delta_y(self):
        return self.end_y - self.start_y

    def interpolate(self):
        pass

    def update(self, dt):
        self.time += dt
        if self.time >= self.duration:
            self.finish()
        else:
            self.target.x, self.target.y = self.interpolate()

    def finish(self):
        # TODO: Dispatch "done" event for Motion.
        self.target.x, self.target.y = self.end_x, self.end_y
        self.dispatch_event('on_finish', self)

Motion.register_event_type('on_finish')


class LinearMotion(Motion):
    def interpolate(self):
        progress = float(self.time) / float(self.duration)
        new_x = int(self.start_x + progress * self.delta_x)
        new_y = int(self.start_y + progress * self.delta_y)
        return (new_x, new_y)


class CosineMotion(Motion):
    def interpolate(self):
        progress = float(self.time) / float(self.duration)
        mathemagic = -(math.cos(progress * math.pi) - 1) / 2.0
        new_x = int(self.start_x + mathemagic * self.delta_x)
        new_y = int(self.start_y + mathemagic * self.delta_y)
        return (new_x, new_y)

class Tint(pyglet.event.EventDispatcher):
    def __init__(self, target, r, g, b, duration):
        self.target = target
        self.r = r
        self.g = g
        self.b = b
        self.duration = duration
        self.time = 0.0
        self.start_r = None
        self.start_g = None
        self.start_b = None

    def setup(self, time_offset=0.0):
        self.start_r, self.start_g, self.start_b = self.target.color
        self.time = time_offset

    @property
    def end_r(self):
        return self.r

    @property
    def end_g(self):
        return self.g

    @property
    def end_b(self):
        return self.b

    @property
    def delta_r(self):
        return self.end_r - self.start_r

    @property
    def delta_g(self):
        return self.end_g - self.start_g

    @property
    def delta_b(self):
        return self.end_b - self.start_b

    def interpolate(self):
        pass

    def update(self, dt):
        self.time += dt
        if self.time >= self.duration:
            self.finish()
        else:
            self.target.color = self.interpolate()

    def finish(self):
        self.target.color = (self.end_r, self.end_g, self.end_b)
        self.dispatch_event('on_finish', self)

Tint.register_event_type('on_finish')


class LinearTint(Tint):
    def interpolate(self):
        progress = float(self.time) / float(self.duration)
        new_r = int(self.start_r + progress * self.delta_r)
        new_g = int(self.start_g + progress * self.delta_g)
        new_b = int(self.start_b + progress * self.delta_b)
        return (new_r, new_g, new_b)


class CosineTint(Motion):
    def interpolate(self):
        progress = float(self.time) / float(self.duration)
        mathemagic = -(math.cos(progress * math.pi) - 1) / 2.0
        new_r = int(self.start_r + mathemagic * self.delta_r)
        new_g = int(self.start_g + mathemagic * self.delta_g)
        new_b = int(self.start_b + mathemagic * self.delta_b)
        return (new_r, new_g, new_b)