import logging
log = logging.getLogger(__name__)

import pyglet

import world

SCROLL_SPEED = 100
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

        self.batch = pyglet.graphics.Batch()
        self.root_group = pyglet.graphics.OrderedGroup(0)
        self.groups = {}
        for group_name in [
            'STATIC_BG', 'DYNAMIC_BG',
            'PROPS', 'ACTORS', 'HERO',
            'PROJECTILES', 'FG']:
            self.groups[group_name] = pyglet.graphics.OrderedGroup(
                len(self.groups), parent=self.root_group)

        self.is_scrolling = False

        self.offset = 0
        self.active_section = None

        log.debug('Initialised Stage {}.'.format(self.name))

    def setup(self):
        self.reset()
        bg_pattern = pyglet.image.SolidColorImagePattern(
            self.background_color)
        bg_image = bg_pattern.create_image(640, 360)
        self.background = pyglet.sprite.Sprite(
            bg_image, batch=self.batch,
            group=self.groups['STATIC_BG'])

        for sect in self.sections:
            sect.setup()

        self.section_iter = iter(self.sections)
        self.advance_section()
        self.is_scrolling = True

    def reset(self):
        self.despawn_props(self.all_props)
        self.despawn_actors(self.all_actors)

        self.is_scrolling = False
        self.offset = 0
        self.active_section = None

        log.info('Reset Stage {}.'.format(self.name))

    def update(self, dt):
        if self.is_scrolling:
            self.offset += SCROLL_SPEED * dt
            if self.offset >= self.active_section.offset:
                self.advance_section()
        # self.update_actors(dt)
        self.update_sprites()

    def update_actors(self, dt):
        for actor in self.active_actors:
            actor.update(dt)

    def update_sprites(self):
        for actor in self.all_actors:
            actor.update_sprite(self.offset)
        for prop in self.all_props:
            prop.update_sprite(self.offset)

    def advance_section(self):
        if self.active_section is not None:
            self.exit_section(self.active_section)
        try:
            new_section = self.section_iter.next()
            self.enter_section(new_section)
        except StopIteration:
            self.is_scrolling = False
            # self.dispatch_event('on_enter_final_section')

    def exit_section(self, old_section):
        self.despawn_props(self.old_props)
        if old_section is not None:
            # self.spawn_actors(old_section.ambush_actors)
            old_section.reset()
        self.active_section = None
        self.dispatch_event('on_exit_section', old_section.name)

        log.info('Exited Section {}.'.format(old_section.name))

    def enter_section(self, new_section):
        if new_section is not None:
            # new_section.setup()
            self.spawn_props(new_section.props)
            self.spawn_actors(new_section.actors)
        self.active_section = new_section
        self.dispatch_event('on_enter_section', new_section.name)

        log.info('Entered Section {}.'.format(new_section.name))

    def add_section(self, section):
        section.offset = self.stage_width
        self.sections.append(section)

        log.debug('Appended Section {} to Stage {}.'.format(
                section.name, self.name))

    def spawn_props(self, props):
        for prop in props:
            prop.setup_sprite(self.batch, self.groups['PROPS'])
        self.all_props |= props

    def despawn_props(self, props):
        for prop in props:
            prop.despawn()
        self.all_props -= props

    def spawn_actors(self, actors):
        for actor in actors:
            actor.setup_sprite(self.batch, self.groups['ACTORS'])
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
        self.prop_list = []
        self.actor_list = []
        self.second_actor_list = []
        self.offset = None

        self.props = None

        log.debug('Initialised StageSection {}.'.format(self.name))

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
            self.second_actors.add(placeholder.spawn(self.offset))

    def reset(self):
        self.props = None
        self.actors = None

StageSection.register_event_type('on_enter_section')
StageSection.register_event_type('on_display_section')


class Placeholder(object):
    def __init__(self, Cls, x, y, **kwargs):
        self.Cls = Cls
        self.x = x
        self.y = y
        self.kwargs = kwargs

    def spawn(self, offset):
        return self.Cls(self.x + offset, self.y, **self.kwargs)


class ProceduralStageSection(StageSection):
    def __init__(self, name):
        super(ProceduralStageSection, self).__init__(name)
