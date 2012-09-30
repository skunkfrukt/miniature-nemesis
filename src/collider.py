class Collider:
    def __init__(self, left=0, bottom=0, right=None, top=None,
            width=None, height=None):
        self.left, self.bottom, self.right, self.top = None, None, None, None
        self.offset_left, self.offset_bottom = left, bottom
        if width is not None:
            assert right is None, "Collider has both width and right"
            self.offset_right = left + width
        else:
            assert right is not None, "Collider lacks both width and right"
            self.offset_right = right
        if height is not None:
            assert top is None, "Collider has both height and top"
            self.offset_top = bottom + height
        else:
            assert top is not None, "Collider lacks both width and top"
            self.offset_top = top
        assert self.offset_left < self.offset_right, "Collider's left >= right"
        assert self.offset_bottom < self.offset_top, "Collider's bottom >= top"
        
    def collide(self, other):
        assert self.left is not None, "Collider's real left is None."
        assert self.bottom is not None, "Collider's real bottom is None."
        assert self.right is not None, "Collider's real right is None."
        assert self.top is not None, "Collider's real top is None."
        return self.collide_x(other) and self.collide_y(other)
    
    def collide_x(self, other):
        overlap_left = max(self.left, other.left)
        overlap_right = min(self.right, other.right)
        return overlap_right > overlap_left  # True if overlap has positive width.
        
    def collide_y(self, other):
        overlap_bottom = max(self.bottom, other.bottom)
        overlap_top = min(self.top, other.top)
        return overlap_top > overlap_bottom  # True if overlap has positive height.
        
    def move(self, base_x, base_y):
        self.left = base_x + self.offset_left
        self.bottom = base_y + self.offset_bottom
        self.right = base_x + self.offset_right
        self.top = base_y + self.offset_top