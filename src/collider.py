class Collider:
    def __init__(self, x0=0, y0=0, x1=None, y1=None, width=None, height=None):
        self.x0, self.y0 = x0, y0
        if width is not None:
            assert x1 is None, "Collider has both width and x1"
            self.x1 = x0 + width
        else:
            assert x1 is not None, "Collider lacks both width and x1"
            self.x1 = x1
        if height is not None:
            assert y1 is None, "Collider has both height and y1"
            self.y1 = y0 + height
        else:
            assert y1 is not None, "Collider lacks both width and y1"
            self.y1 = y1
        
        
    def collide(self, other):
        return self.collide_x(other) and self.collide_y(other)  # and self.x < other.x
    
    def collide_x(self, other):
        overlap_x0 = max(self.x0, other.x0)
        overlap_x1 = min(self.x1, other.x1)
        return overlap_x1 > overlap_x0  # True if overlap has positive width.
        
    def collide_y(self, other):
        overlap_y0 = max(self.y0, other.y0)
        overlap_y1 = min(self.y1, other.y1)
        return overlap_y1 > overlap_y0  # True if overlap has positive height.
    
        
if __name__ == '__main__':
    import tests.test_collider