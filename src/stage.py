import logging
log = logging.getLogger(__name__)

import pyglet
import random
import itertools

import world
import spritehandler
SH = spritehandler

from hero import Hero

from vector import *

SCROLL_SPEED = Vector(100, 0)
SECTION_WIDTH = 640

_section_num = 0
def generate_section_name():
    global _section_num
    section_name = 'Section #{}'.format(_section_num)
    _section_num += 1
    return section_name


class Stage(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.sections = []
        self.all_props = set()
        self.all_actors = set()

        self.offset = VECTOR_NULL
        self.is_scrolling = False
        self.actual_scroll_speed = VECTOR_NULL
        self.target_scroll_speed = SCROLL_SPEED
        self.active_section = None

        log.debug(D_INIT.format(type(self).__name__, self.name))

    def setup(self):
        self.reset()
        if self.seed is not None:
            random.seed(self.seed)
        bg_pattern = pyglet.image.SolidColorImagePattern(
            self.background_color)
        bg_img = bg_pattern.create_image(640, 360)
        self.background = SH.show_sprite(SH.BG, 0)
        self.background.image = bg_img
        self.background.x = world.ZERO

        for sect in self.sections:
            sect.setup()

        self.section_iter = iter(self.sections)
        self.advance_section()
        self.is_scrolling = True
        self.hero = Hero(Vector(100, 100))
        self.spawn_actors(set([self.hero]))

    def reset(self):
        self.despawn_props(self.all_props)
        self.despawn_actors(self.all_actors)

        self.actual_scroll_speed = VECTOR_NULL
        self.offset = VECTOR_NULL
        self.active_section = None

        log.info('Reset Stage {}.'.format(self.name))

    def update(self, dt):
        self.update_stage_position(dt)
        self.update_actors(dt)
        self.update_sprites()

    def update_stage_position(self, dt):
        if self.is_scrolling:
            self.update_scroll_speed(dt)
            self.offset += self.actual_scroll_speed * dt
        if self.active_section is not None:
            if self.offset.x >= self.active_section.offset.x:
                self.advance_section()

    def update_scroll_speed(self, dt):
        actual = self.actual_scroll_speed.x
        target = self.target_scroll_speed.x
        if actual < target:
            delta = 50 * dt  ##TODO## Magic number.
            new_scroll_speed = min(target, actual + delta)
            self.actual_scroll_speed = Vector(new_scroll_speed, 0)

    def start_scrolling(self, scroll_speed):
        self.target_scroll_speed = scroll_speed
        self.is_scrolling = True

    def stop_scrolling(self):
        self.actual_scroll_speed = VECTOR_NULL
        self.is_scrolling = False

    def update_actors(self, dt):
        for actor in self.all_actors:
            actor.update(dt)

    def update_sprites(self):
        for actor in self.all_actors:
            actor.align_sprite(self.offset)
        for prop in self.all_props:
            prop.align_sprite(self.offset)

    def advance_section(self):
        if self.active_section is not None:
            self.exit_section(self.active_section)
        try:
            new_section = self.section_iter.next()
            self.enter_section(new_section)
        except StopIteration:
            self.stop_scrolling()
            # self.dispatch_event('on_enter_final_section')

    def exit_section(self, old_section):
        self.despawn_props(self.old_props)
        if old_section is not None:
            self.spawn_actors(old_section.second_actors)
            old_section.reset()
        self.active_section = None
        self.dispatch_event('on_exit_section', old_section.name)

        log.info(I_EXIT_SECTION.format(old_section.name))

    def enter_section(self, new_section):
        if new_section is not None:
            # new_section.setup()
            self.spawn_props(new_section.props)
            self.spawn_actors(new_section.actors)
        self.active_section = new_section
        self.dispatch_event('on_enter_section', new_section.name)

        log.info(I_ENTER_SECTION.format(new_section.name))

    def add_section(self, section):
        section.offset = Vector(self.stage_width, 0)
        self.sections.append(section)

        log.debug(D_ADD_SECTION.format(section.name, self.name))

    def spawn_props(self, props):
        for prop in props:
            prop.allocate_sprite()
            prop.show()
        self.all_props |= props

    def despawn_props(self, props):
        for prop in props:
            prop.despawn()
        self.all_props -= props

    def spawn_actors(self, actors):
        for actor in actors:
            actor.allocate_sprite()
            actor.show()
            log.debug(D_SPAWN_ACTOR.format(type(actor).__name__))
        self.all_actors |= actors

    def despawn_actors(self, actors):
        for actor in actors:
            actor.despawn()
        self.all_actors -= actors

    @property
    def current_props(self):
        if self.active_section is not None:
            return self.active_section.props
        else:
            return set()

    @property
    def old_props(self):
        return self.all_props - self.current_props

    @property
    def stage_width(self):
        return 640 * len(self.sections)  ##TODO## MN
        return world.constants['WIN_WIDTH'] * len(self.sections)

    @property
    def stage_height(self):
        return 360  ##TODO## MN
        return world.constants['WIN_HEIGHT']

    def send_keys_to_hero(self, keys, pressed=None, released=None):
        if self.hero is not None:
            self.hero.fixSpeed(keys)

Stage.register_event_type('on_begin_stage')
Stage.register_event_type('on_end_stage')
Stage.register_event_type('on_enter_section')
Stage.register_event_type('on_exit_section')


class StageSection(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.prop_list = []
        self.actor_list = []
        self.second_actor_list = []
        self.offset = None

        self.props = None

        log.debug(D_INIT.format(type(self).__name__, self.name))

    def setup(self):
        self.setup_props()
        self.setup_actors()

    def setup_props(self):
        self.props = set()
        for placeholder in self.prop_list:
            self.props.add(placeholder.spawn(self.offset))

    def setup_actors(self):
        self.actors = set()
        self.second_actors = set()
        for placeholder in self.actor_list:
            self.actors.add(placeholder.spawn(self.offset))
        for placeholder in self.second_actor_list:
            ambusher = placeholder.spawn(self.offset)
            ambusher.behavior = ambusher.behave_charge_ahead
            self.second_actors.add(ambusher)

    def reset(self):
        self.props = None
        self.actors = None
        self.second_actors = None

StageSection.register_event_type('on_enter_section')
StageSection.register_event_type('on_display_section')


class Placeholder(object):
    def __init__(self, Cls, position, **kwargs):
        self.Cls = Cls
        self.position = position
        self.kwargs = kwargs

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def spawn(self, offset):
        return self.Cls(self.position + offset, **self.kwargs)


class ProceduralStageSection(StageSection):
    def __init__(self, name):
        super(ProceduralStageSection, self).__init__(name)

    def setup_props(self):
        self.prop_list = self.generate_props()
        super(ProceduralStageSection, self).setup_props()

    def generate_props(self):
        return generate_map(knight_path, self.prop_pool)


def rect(x, y, width, height, cls):
    return (x, y, width, height, cls)

def cells_in_rect(r):
    x, y, w, h, n = r
    return set(itertools.product(range(x, x + w), range(y, y + h)))

def possible_rects(cls):
    builder_data = cls.builder_data
    width = builder_data.get('width', 1)
    height = builder_data.get('height', 1)
    start_x = 0
    limit_x = 16 + 1 - width
    start_y = builder_data.get('min_y', 0)
    limit_y = builder_data.get('max_y', 8) + 1
    range_x = range(start_x, limit_x)
    range_y = range(start_y, limit_y)
    coords = itertools.product(range_x, range_y)
    rects = set()
    for coord in coords:
        x, y = coord
        r = rect(x, y, width, height, cls)
        rects.add(r)
    return rects

def generate_map(path_algorithm, props={}):
    rects = {cls: possible_rects(cls) for cls in props.keys()}
    limits = props
    object_type_order = sorted(limits.keys(), key=lambda x: len(rects[x]))
    all_cells = set(itertools.product(range(16), range(9)))
    rects_by_cell = {}
    for c in all_cells:
        rects_by_cell[c] = set()
    all_rects = set()
    for object_type in object_type_order:
        all_rects |= rects[object_type]
    for r in all_rects:
        cells = cells_in_rect(r)
        for cell in cells:
            try:
                rects_by_cell[cell].add(r)
            except KeyError:
                pass
    invalid_rects = set()
    used_rects = set()
    path = path_algorithm() & all_cells
    for c in path:
        invalid_rects |= rects_by_cell[c]
    for object_type in object_type_order:
        typed_rects = rects[object_type]
        quantity = 0
        while quantity < limits[object_type]:
            valid_rects = typed_rects - invalid_rects
            if len(valid_rects) == 0:
                break
            r = random.choice(sorted(valid_rects))
            used_rects.add(r)
            quantity += 1
            for c in cells_in_rect(r) & all_cells:
                invalid_rects |= rects_by_cell[c]
    return [rect_to_placeholder(r) for r in used_rects]

def rect_to_placeholder(r):
    x = r[0] * 40
    y = r[1] * 40
    cls = r[4]
    x_variance = cls.builder_data.get('x_variance', 0)
    y_variance = cls.builder_data.get('y_variance', 0)
    x += random.randint(0, x_variance)
    y += random.randint(0, y_variance)
    return Placeholder(cls, Vector(x, y))

def knight_path():
    traversed_cells = set()

    current_cell = (0, 4)
    traversed_cells.add(current_cell)

    max_y = 6
    min_y = 0

    while current_cell[0] < 16:
        next_move = random.randint(0,3)
        cx, cy = current_cell
        if next_move == 0 and cy < max_y - 1:
            traversed_cells.add((cx + 1, cy))
            traversed_cells.add((cx + 1, cy + 1))
            traversed_cells.add((cx + 1, cy + 2))
            current_cell = (cx + 1, cy + 2)
        elif next_move == 1 and cy < max_y:
            traversed_cells.add((cx + 1, cy))
            traversed_cells.add((cx + 2, cy))
            traversed_cells.add((cx + 2, cy + 1))
            current_cell = (cx + 2, cy + 1)
        elif next_move == 2 and cy > min_y:
            traversed_cells.add((cx + 1, cy))
            traversed_cells.add((cx + 2, cy))
            traversed_cells.add((cx + 2, cy - 1))
            current_cell = (cx + 2, cy - 1)
        elif next_move == 3 and cy > min_y + 1:
            traversed_cells.add((cx + 1, cy))
            traversed_cells.add((cx + 1, cy - 1))
            traversed_cells.add((cx + 1, cy - 2))
            current_cell = (cx + 1, cy - 2)
    return traversed_cells

def faff_path():
    traversed_cells = set()

    current_cell = (0, 4)
    traversed_cells.add(current_cell)

    max_y = MAP_HEIGHT - 3
    min_y = 0

    while current_cell[0] < MAP_WIDTH:
        next_move = random.randint(0,2)
        cx, cy = current_cell
        if next_move == 0:
            traversed_cells.add((cx + 1, cy))
            current_cell = (cx + 1, cy)
        elif next_move == 1 and cy < max_y:
            traversed_cells.add((cx, cy + 1))
            current_cell = (cx, cy + 1)
        elif next_move == 2 and cy > min_y:
            traversed_cells.add((cx, cy - 1))
            current_cell = (cx, cy - 1)
    return traversed_cells

def noise_path():
    traversed_cells = set()

    current_cell = (-1, 4)
    traversed_cells.add(current_cell)

    max_y = MAP_HEIGHT - 1
    min_y = 0

    while current_cell[0] < MAP_WIDTH:
        cx, cy = current_cell
        traversed_cells.add((cx + 1, cy))
        traversed_cells.add((cx + 2, cy))
        current_cell = (cx + 2, cy)
        cx, cy = current_cell
        next_y = random.randint(min_y, max_y)
        for y in range(min(cy, next_y), max(cy, next_y) + 1):
            traversed_cells.add((cx, y))
        current_cell = (cx, next_y)
    return traversed_cells


I_ENTER_SECTION = "Entered Section {}."
I_EXIT_SECTION = "Exited Section {}."
D_ADD_SECTION = "Appended Section {} to Stage {}."
D_INIT = "Initialised {} {}."
D_SPAWN_ACTOR = "Spawned actor {}."
