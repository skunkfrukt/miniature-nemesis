import pyglet

class Collider(pyglet.event.EventDispatcher):
    def __init__(self, left=0, bottom=0, right=None, top=None,
            width=None, height=None):
        self.left, self.bottom, self.right, self.top = None, None, None, None
        self._offset_left, self._offset_bottom = left, bottom
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
        assert self._offset_left < self._offset_right, "Collider's left >= right"
        assert self._offset_bottom < self._offset_top, "Collider's bottom >= top"

    def collide(self, other):
        assert self.left is not None, "Collider's real left is None."
        assert self.bottom is not None, "Collider's real bottom is None."
        assert self.right is not None, "Collider's real right is None."
        assert self.top is not None, "Collider's real top is None."
        collision_rect = self.get_collision_rect(other)
        colliding = collision_rect is not None
        if colliding:
            self.dispatch_event('on_collision', other, collision_rect)
        return collision_rect

    def get_collision_rect(self, other):
        rect_left = max(self.left, other.left)
        rect_right = min(self.right, other.right)
        rect_bottom = max(self.bottom, other.bottom)
        rect_top = min(self.top, other.top)
        if rect_right > rect_left and rect_top > rect_bottom:
            return (rect_left, rect_bottom, rect_right, rect_top)
        else:
            return None

    def move(self, base_x, base_y):
        self.left = base_x + self._offset_left
        self.bottom = base_y + self._offset_bottom
        self.right = base_x + self._offset_right
        self.top = base_y + self._offset_top

    @property
    def rect(self):
        return (self.left, self.bottom, self.right, self.top)

Collider.register_event_type('on_collision')


def collide(*colliders):
    if len(colliders) == 0:
        return None
    elif len(colliders) == 1:
        return collide(colliders[0], colliders[0])


def pairs(items):
    for first_index, first_item in enumerate(items):
        for second_index, second_item in enumerate(items[first_index+1:]):
            yield (first_item, second_item)


class SpatialHash():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.rows = int(height / cell_size + 0.5)
        self.cols = int(width / cell_size + 0.5)
        self.cell_size = cell_size
        self.grid = [[]] * self.rows * self.cols

    def get_cell_indices(self, rect):
        left, bottom, right, top = rect
        left = max(0, left)
        bottom = max(0, bottom)
        right = min(right, self.width- 1)
        top = min(top, self.height - 1)
        left_cell = int(left / self.cell_size)
        right_cell = int(right / self.cell_size) + 1
        bottom_cell = int(bottom / self.cell_size)
        top_cell = int(top / self.cell_size) + 1
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
                    a.collide(b)
                    b.collide(a)
