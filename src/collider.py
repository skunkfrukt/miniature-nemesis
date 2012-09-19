class Collider:
    def __init__(self, x = 0, y = 0, width = 1, height = 1):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
    def collide(self, other):
        return (self.collide_x(other) and self.collide_y(other))
    
    def collide_x(self, other):
        cx0 = max(self.x, other.x)
        cx1 = min(self.x + self.width, other.x + other.width)
        return cx1 > cx0
        
    def collide_y(self, other):
        cy0 = max(self.y, other.y)
        cy1 = min(self.y + self.height, other.y + other.height)
        return cy1 > cy0

class PointCollider(Collider):
    def __init__(self,x=0,y=0):
        super(PointCollider, self).__init__(x, y, 1, 1)
        
    def collide(self, other):
        return self.x == other.x and self.y == other.y
    
        
if __name__ == '__main__':
    import tests.test_collider