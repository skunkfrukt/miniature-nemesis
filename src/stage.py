import logging
log = logging.getLogger(__name__)

import pyglet

import world

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

        self.batch = pyglet.graphics.Batch()
        self.groups = {}
        for group_name in [
            'STATIC_BG', 'DYNAMIC_BG',
            'PROPS', 'ACTORS', 'HERO',
            'PROJECTILES', 'FG']:
            self.groups[group_name] = pyglet.graphics.OrderedGroup(
                len(self.groups))

        self.is_scrolling = False

        self.offset = 0
        self.active_section = None

        log.debug('Initialised Stage {}.'.format(self.name))

    def setup_deprecated_shit(self):
        self.setup_background(color)
        self.spatial_hashes = {}
        self.spatial_hashes[HASH_GROUND] = collider.SpatialHash(
                self.width, self.height, 60, 60, layer=HASH_GROUND)
        self.spatial_hashes[HASH_AIR] = collider.SpatialHash(
                self.width, self.height, 60, 60, layer=HASH_AIR)
        self.spatial_hashes[HASH_TRIGGER] = collider.SpatialHash(
                self.width, self.height, 60, self.height, layer=HASH_TRIGGER)
        self.scroll_speed = 100

    def setup(self):
        '''bg_pattern = pyglet.image.SolidColorImagePattern(
            self.backgroundColor)
        bg_image = bg_pattern.create_image(
            world.constants['WIN_WIDTH'], world.constants['WIN_HEIGHT'])
        pyglet.sprite.Sprite(
            background_image, batch=self.batch,
            group=self.groups['STATIC_BG'])'''

        self.section_iter = iter(self.sections)
        self.advance_section()

    def reset(self):
        self.despawn_props(self.all_props)
        self.despawn_actors(self.all_actors)

        self.is_scrolling = False
        self.offset = 0
        self.active_section = None

        log.info('Reset Stage {}.'.format(self.name))

    def update(self, dt):
        if self.is_scrolling:
            new_offset = self.offset + SCROLL_SPEED * dt
            if (new_offset % SECTION_WIDTH) < (self.offset % SECTION_WIDTH):
                self.advance_section()
            self.offset = new_offset
        self.update_actors(dt)

    def update_actors(self, dt):
        for actor in self.active_actors:
            actor.update(dt)

    def advance_section(self):
        if self.active_section is not None:
            self.exit_section(self.active_section)
        try:
            new_section = self.section_iter.next()
            self.enter_section(new_section)
        except StopIteration:
            self.is_scrolling = False
            self.dispatch_event('on_enter_final_section')

    def exit_section(self, old_section):
        self.despawn_props(self.old_props)
        if old_section is not None:
            self.spawn_actors(old_section.ambush_actors)
            old_section.reset()
        self.active_section = None
        self.dispatch_event('on_exit_section', old_section.name)

        log.info('Exited Section {}.'.format(old_section.name))

    def enter_section(self, new_section):
        if new_section is not None:
            new_section.setup(self.offset)
            self.spawn_props(new_section.props)
            self.spawn_actors(new_section.initial_actors)
        self.active_section = new_section
        self.dispatch_event('on_enter_section', new_section.name)

        log.info('Entered Section {}.'.format(new_section.name))

    def add_section(self, section):
        section.offset = self.stage_width
        self.sections.append(section)

        log.debug('Appended Section {} to Stage {}.'.format(
                section.name, self.name))

    def spawn_props(self, props):
        self.all_props |= props

    def despawn_props(self, props):
        for prop in props:
            prop.despawn()
        self.all_props -= props

    def spawn_actors(self, actors):
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
        return 640 * len(self.sections)
        return world.constants['WIN_WIDTH'] * len(self.sections)

    @property
    def stage_height(self):
        return 360
        return world.constants['WIN_HEIGHT']

Stage.register_event_type('on_begin_stage')
Stage.register_event_type('on_end_stage')
Stage.register_event_type('on_enter_section')
Stage.register_event_type('on_exit_section')


class StageSection(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.props = None

        log.debug('Initialised StageSection {}.'.format(self.name))

    def setup(self, offset):
        self.setup_props(offset)
        self.setup_actors(offset)

    def setup_props(self, offset):
        pass

    def setup_actors(self, offset):
        pass

    def reset(self):
        self.props = None

StageSection.register_event_type('on_enter_section')
StageSection.register_event_type('on_display_section')


class ProceduralStageSection(StageSection):
    def __init__(self, name):
        super(ProceduralStageSection, self).__init__(name)
