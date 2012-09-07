class Collider:
    def __init__(self, x = 0, y = 0, width = 1, height = 1):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
    def collide(self, other_collider):
        return self.collide_x(other_collider) and self.collide_y(other_collider)
    
    def collide_x(self, other_collider):
        diff = other_collider.x - self.x
        if diff == 0:
            return true
        elif diff < 0:
            return -diff < other_collider.width
        else: # diff > 0
            return diff < self.width
    
    def collide_y(self, other_collider):
        diff = other_collider.y - self.y
        if diff == 0:
            return true
        elif diff < 0:
            return -diff < other_collider.height
        else: # diff > 0
            return diff < self.height

class PointCollider(Collider):
    def __init__(self,x=0,y=0):
        super(PointCollider, self).__init__(x, y, 1, 1)
        
    def collide(self, other_collider):
        return self.x == other_collider.x and self.y == other_collider.y
    
        
if __name__ == '__main__':
    import tests.test_collider