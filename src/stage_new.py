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

        log.info('Stage {} initialised.'.format(self.name))

    def setup(self):
        pass

    def update(self, dt):
        if self.is_scrolling:
            new_offset = self.offset + SCROLL_SPEED * dt
            if (new_offset % SECTION_WIDTH) < (self.offset % SECTION_WIDTH):
                self.advance_section()
            self.offset = new_offset
        self.update_actors(dt)

    def advance_section(self):
        try:
            new_section = self.section_iter.next()
        except StopIteration:
            self.is_scrolling = False
            new_section = None
        finally:
            self.despawn(self.old_props)
            self.set_active_section(new_section)

    def set_active_section(self, new_section):
        old_section = self.active_section
        old_section.reset()
        if new_section is not None:
            new_section.setup()
            self.all_props |= new_section.props
        self.active_section = new_section

    def append_section(self, section):
        self.sections.append(section)

    @property
    def current_props(self):
        if self.active_section is not None:
            return self.active_section.props
        else:
            return set()

    @property
    def old_props(self):
        return self.all_props - self.current_props

Stage.register_event_type('on_enter_stage')
Stage.register_event_type('on_exit_stage')


class StageSection(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.props = None

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
