from gameobject import GameObject

class Projectile(GameObject):
    preferred_rendering_group_index = 3  # R_GROUP_PROJECTILES

    def launch(self, origin_x, origin_y, target_x, target_y, speed):
        print("Launching %s." % self)
        self.x = origin_x
        self.y = origin_y
        delta_x = target_x - origin_x
        delta_y = target_y - origin_y
        delta_x_squared = delta_x ** 2
        delta_y_squared = delta_y ** 2
        speed_squared = speed ** 2
        speed_squared_from_deltas = delta_x_squared + delta_y_squared
        speed_factor = math.sqrt(speed_squared / speed_squared_from_deltas)
        dx = delta_x * speed_factor
        dy = delta_y * speed_factor
        self.speed = (dx, dy)
        self.dead = False;
        self.width = 1
