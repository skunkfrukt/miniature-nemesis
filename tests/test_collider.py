from src.collider import *
import unittest

class TestCollider(unittest.TestCase):
    def setUp(self):
        # The main collider is the one we'll be testing stuff against.
        # The alternative one is just the same, constructed differently.
        self.collider = Collider(0,0,width=10,height=10)
        self.collider_alternative = Collider(0,0,10,10)

        # Concentric colliders.
        self.small_collider = Collider(4,4,width=2,height=2)
        self.large_hadron_collider = Collider(-5,-5,width=20,height=20)

        # Colliders to the north and to the south of main.
        self.north_discrete = Collider(-5,13,width=20,height=2)
        self.north_overlapping = Collider(-5,5,width=20,height=10)
        self.south_discrete = Collider(-5,-5,width=20,height=2)
        self.south_overlapping = Collider(-5,-5,width=20,height=10)

        # Colliders to the east and to the west of main.
        self.east_discrete = Collider(13,-5,width=2,height=20)
        self.east_overlapping = Collider(5,-5,width=10,height=20)
        self.west_discrete = Collider(-5,-5,width=2,height=20)
        self.west_overlapping = Collider(-5,-5,width=10,height=20)

        # Colliders in the corners of main.
        self.southwest_discrete = Collider(-5,-5,width=2,height=2)
        self.southwest_overlapping = Collider(-5,-5,width=10,height=10)
        self.southeast_discrete = Collider(13,13,width=2,height=2)
        self.southeast_overlapping = Collider(5,5,width=10,height=10)
        self.northwest_discrete = Collider(-5,13,width=2,height=2)
        self.northwest_overlapping = Collider(-5,5,width=10,height=10)
        self.northeast_discrete = Collider(13,13,width=2,height=2)
        self.northeast_overlapping = Collider(5,5,width=10,height=10)

        # Close colliders.
        self.north_close = Collider(0,10,width=10,height=5)
        self.south_close = Collider(0,-5,width=10,height=5)
        self.west_close = Collider(-5,0,width=5,height=10)
        self.east_close = Collider(10,0,width=5,height=10)

        all_colliders = [
                self.collider,
                self.collider_alternative,
                self.small_collider,
                self.large_hadron_collider,
                self.north_discrete,
                self.north_overlapping,
                self.south_discrete,
                self.south_overlapping,
                self.east_discrete,
                self.east_overlapping,
                self.west_discrete,
                self.west_overlapping,
                self.southwest_discrete,
                self.southwest_overlapping,
                self.southeast_discrete,
                self.southeast_overlapping,
                self.northwest_discrete,
                self.northwest_overlapping,
                self.northeast_discrete,
                self.northeast_overlapping,
                self.north_close,
                self.south_close,
                self.west_close,
                self.east_close
                ]

        for collider in all_colliders:
            collider.move(0,0)

    def assertCollides(self, other):
        return self.assertEqual(True, self.collider.collide(other))

    def assertDodges(self, other):
        return self.assertEqual(False, self.collider.collide(other))

    def test_both_notations_work_for_x(self):
        self.assertEqual(self.collider.right, self.collider_alternative.right)

    def test_both_notations_work_for_y(self):
        self.assertEqual(self.collider.top, self.collider_alternative.top)

    def test_small_concentric_collider(self):
        self.assertCollides(self.small_collider)

    def test_large_concentric_collider(self):
        self.assertCollides(self.large_hadron_collider)

    def test_north_discrete(self):
        self.assertDodges(self.north_discrete)

    def test_north_overlapping(self):
        self.assertCollides(self.north_overlapping)

    def test_south_discrete(self):
        self.assertDodges(self.south_discrete)

    def test_south_overlapping(self):
        self.assertCollides(self.south_overlapping)

    def test_east_discrete(self):
        self.assertDodges(self.east_discrete)

    def test_east_overlapping(self):
        self.assertCollides(self.east_overlapping)

    def test_west_discrete(self):
        self.assertDodges(self.west_discrete)

    def test_west_overlapping(self):
        self.assertCollides(self.west_overlapping)

    def test_northeast_discrete(self):
        self.assertDodges(self.east_discrete)

    def test_northeast_overlapping(self):
        self.assertCollides(self.east_overlapping)

    def test_northwest_discrete(self):
        self.assertDodges(self.west_discrete)

    def test_northwest_overlapping(self):
        self.assertCollides(self.west_overlapping)

    def test_southeast_discrete(self):
        self.assertDodges(self.east_discrete)

    def test_southeast_overlapping(self):
        self.assertCollides(self.east_overlapping)

    def test_southwest_discrete(self):
        self.assertDodges(self.west_discrete)

    def test_southwest_overlapping(self):
        self.assertCollides(self.west_overlapping)

    def test_north_close(self):
        self.assertDodges(self.north_close)

    def test_south_close(self):
        self.assertDodges(self.south_close)

    def test_west_close(self):
        self.assertDodges(self.west_close)

    def test_east_close(self):
        self.assertDodges(self.east_close)
