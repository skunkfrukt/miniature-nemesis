import pyglet

import logging
log = logging.getLogger(__name__)


class Stage(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.sections = []
        self.all_props = set()
        self.all_actors = set()

        self.is_scrolling = False

        self.offset = 0
        self.active_section = None

        log.debug('Initialised Stage {}.'.format(self.name))

    def setup(self):
        pass

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
        old_section.reset()
        self.active_section = None
        self.dispatch_event('on_exit_section', old_section.name)

        log.info('Exited Section {}.'.format(old_section.name))

    def enter_section(self, new_section):
        if new_section is not None:
            new_section.setup()
            self.all_props |= new_section.props
        self.active_section = new_section
        self.dispatch_event('on_enter_section', new_section.name)

        log.info('Entered Section {}.'.format(new_section.name))

    def append_section(self, section):
        self.sections.append(section)

        log.debug('Appended Section {} to Stage {}.'.format(
                section.name, self.name))

    @property
    def current_props(self):
        if self.active_section is not None:
            return self.active_section.props
        else:
            return set()

    @property
    def old_props(self):
        return self.all_props - self.current_props

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
