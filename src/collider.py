class Collider:
    def __init__(self, x = 0, y = 0, width = 1, height = 1):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
    def collide(self, other_collider):
        return self.collide_x(other_collider) and self.collide_y(other_collider)
    
    def collide_x(self, other_collider):
        cx0 = max(self.x, other_collider.x)
        cx1 = min(self.x + self.width, other_collider.x + other_collider.width)
        cw = cx1 - cx0
        return cw > 0
        
    def collide_y(self, other_collider):
        cy0 = max(self.y, other_collider.y)
        cy1 = min(self.y + self.height, other_collider.y + other_collider.height)
        ch = cy1 - cy0
        return ch > 0

class PointCollider(Collider):
    def __init__(self,x=0,y=0):
        super(PointCollider, self).__init__(x, y, 1, 1)
        
    def collide(self, other_collider):
        return self.x == other_collider.x and self.y == other_collider.y
    
        
if __name__ == '__main__':
    import tests.test_collider