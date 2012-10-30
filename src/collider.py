import pyglet
from constants import *

import logging
log = logging.getLogger(__name__)

class Collider(pyglet.event.EventDispatcher):
    def __init__(self, left=0, bottom=0, right=None, top=None,
            width=None, height=None, effect=None, layer=None, parent=None):
        self.left, self.bottom, self.right, self.top = None, None, None, None
        self._offset_left, self._offset_bottom = left, bottom
        self.layer = layer
        self.parent = parent
        if width is not None:
            assert right is None, "Collider has both width and right"
            self._offset_right = left + width
        else:
            assert right is not None, "Collider lacks both width and right"
            self._offset_right = right
        if height is not None:
            assert top is None, "Collider has both height and top"
            self._offset_top = bottom + height
        else:
            assert top is not None, "Collider lacks both width and top"
            self._offset_top = top
        assert self._offset_left < self._offset_right, "left >= right"
        assert self._offset_bottom < self._offset_top, "bottom >= top"
        self.effect = effect

    def collide(self, other):
        assert self.left is not None, "Collider's real left is None."
        assert self.bottom is not None, "Collider's real bottom is None."
        assert self.right is not None, "Collider's real right is None."
        assert self.top is not None, "Collider's real top is None."
        collision_speed = self.get_collision_speed(other)
        if collision_speed is not None:
            collision_rect = self.get_collision_rect(other)
        else:
            collision_rect = None
        if collision_rect is not None:
            self.dispatch_collision_event(other, collision_rect,
                    collision_speed, other.effect)
        return collision_rect

    def dispatch_collision_event(self, other, collision_rect,
            collision_speed, effect):
        self.dispatch_event('on_collision', other, collision_rect,
                    collision_speed, effect)

    def get_collision_rect(self, other):
        rect_left = max(self.left, other.left)
        rect_right = min(self.right, other.right)
        rect_bottom = max(self.bottom, other.bottom)
        rect_top = min(self.top, other.top)
        if rect_right > rect_left and rect_top > rect_bottom:
            return (rect_left, rect_bottom, rect_right, rect_top)
        else:
            return None

    def get_collision_speed(self, other):
        self_speed_x, self_speed_y = self.speed
        other_speed_x, other_speed_y = other.speed
        if self_speed_x != other_speed_x or self_speed_y != other_speed_y:
            return (self_speed_x - other_speed_x, self_speed_y - other_speed_y)
        else:
            return None

    def move(self, base_x, base_y, speed=None):
        if speed is not None:
            self.speed = speed
        else:
            self.speed = (0, 0)
        self.left = base_x + self._offset_left
        self.bottom = base_y + self._offset_bottom
        self.right = base_x + self._offset_right
        self.top = base_y + self._offset_top

    def get_preferred_layer(self):
        return self.layer

    @property
    def rect(self):
        return (self.left, self.bottom, self.right, self.top)

Collider.register_event_type('on_collision')


class Detector(Collider):
    def __init__(self, left=0):
        super(Detector, self).__init__(left=left, bottom=-LOTS, top=LOTS,
            width=1, effect=None, layer=HASH_TRIGGER)
        self.top = LOTS
        self.bottom = -LOTS
        self.speed = (0,0)

    def dispatch_collision_event(self, other, collision_rect,
            collision_speed, effect):
        self.dispatch_event('on_detection', other.parent)

    def move(self, base_x, base_y, speed=None):
        self.left = base_x + self._offset_left
        self.right = base_x + self._offset_right

Detector.register_event_type('on_detection')


def pairs(items):
    for first_index, first_item in enumerate(items):
        for second_index, second_item in enumerate(items[first_index+1:]):
            yield (first_item, second_item)


class SpatialHash(object):
    def __init__(self, width, height, cell_width, cell_height, layer=None):
        self.layer = layer
        self.width = width
        self.height = height
        self.rows = int((height - 1) / cell_height) + 1
        self.cols = int((width - 1) / cell_width) + 1
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid = [[]] * self.rows * self.cols

    def get_cell_indices(self, rect):
        left, bottom, right, top = rect
        left = max(0, left)
        bottom = max(0, bottom)
        right = min(right, self.width- 1)
        top = min(top, self.height - 1)
        left_cell = int(left / self.cell_width)
        right_cell = int(right / self.cell_width) + 1
        bottom_cell = int(bottom / self.cell_height)
        top_cell = int(top / self.cell_height) + 1
        col_span = range(left_cell, right_cell)
        row_span = range(bottom_cell, top_cell)
        for x in col_span:
            for y in row_span:
                yield x * self.rows + y

    def clear(self, rect):
        left, bottom, right, top = rect
        for cell_index in self.get_cell_indices(rect):
            self.grid[cell_index] = []

    def put(self, obj):
        if obj.get_preferred_layer() == self.layer:
            for cell_index in self.get_cell_indices(obj.rect):
                self.grid[cell_index].append(obj)

    def collide(self, rect, *collider_groups):
        self.clear(rect)
        for group in collider_groups:
            for item in group:
                self.put(item)
        cell_indices = self.get_cell_indices(rect)
        for cell_index in cell_indices:
            cell = self.grid[cell_index]
            if len(cell) >= 2:
                for a, b in pairs(cell):
                    a.collide(b)
                    b.collide(a)
