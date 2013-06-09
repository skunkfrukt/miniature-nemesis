import pyglet

import logging
log = logging.getLogger(__name__)

from vector import *


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
                    hitbox_collide(a, b)


def hitbox_collide(a, b):

    # Collision vector from a's perspective, i.e. as if a were static.
    collision_vector = b.speed - a.speed

    if collision_vector != VECTOR_NULL:
        collision_rect = get_collision_rect(a, b)
    else:
        collision_rect = None
    if collision_rect is not None:
        collision_direction = calculate_collision_direction(
            collision_vector, collision_rect)
        a.collide(b, collision_vector, collision_direction)
        b.collide(a, -collision_vector, -collision_direction)

def get_collision_rect(a, b):
    rect_left = max(a.left, b.left)
    rect_right = min(a.right, b.right)
    rect_bottom = max(a.bottom, b.bottom)
    rect_top = min(a.top, b.top)
    if rect_right > rect_left and rect_top > rect_bottom:
        return (rect_left, rect_bottom, rect_right, rect_top)
    else:
        return None

def calculate_collision_direction(vector, overlap_rect):
    return VECTOR_NULL #TODO: Fulfix!!
