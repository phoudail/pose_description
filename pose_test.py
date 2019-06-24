import unittest
from pose_description import *

class JointTest(unittest.TestCase):

    def setUp(self):
        self.j = Joint("", 15, 15)
        self.s = Segment(Joint("", 13, 13), Joint("", 18, 18))
        self.j1 = Joint("", 10, 7)
        self.j2 = Joint("", 15, 15)
        self.j3 = Joint("", 20, 24)
        

    def test_above(self):
        a = self.j1.above(self.j)
        b = self.j2.above(self.j)
        c = self.j3.above(self.j)
        self.assertTrue(a > b >= c)

    def test_above_all(self):
        a = self.j1.above(self.s)
        b = self.j2.above(self.s)
        c = self.j3.above(self.s)
        self.assertTrue(a > b > c)

    def test_below(self):
        a = self.j3.below(self.j)
        b = self.j2.below(self.j)
        c = self.j1.below(self.j)
        self.assertTrue(a > b >= c)

    def test_below_all(self):
        a = self.j3.below(self.s)
        b = self.j2.below(self.s)
        c = self.j1.below(self.s)
        self.assertTrue(a > b > c)

    def test_to_the_right(self):
        a = self.j3.to_the_right(self.j)
        b = self.j2.to_the_right(self.j)
        c = self.j1.to_the_right(self.j)
        self.assertTrue(a > b >= c)

    def test_to_the_right_all(self):
        a = self.j3.to_the_right(self.s)
        b = self.j2.to_the_right(self.s)
        c = self.j1.to_the_right(self.s)
        self.assertTrue(a > b > c)

    def test_to_the_left(self):
        a = self.j1.to_the_left(self.j)
        b = self.j2.to_the_left(self.j)
        c = self.j3.to_the_left(self.j)
        self.assertTrue(a > b >= c)

    def test_to_the_left_all(self):
        a = self.j1.to_the_left(self.s)
        b = self.j2.to_the_left(self.s)
        c = self.j3.to_the_left(self.s)
        self.assertTrue(a > b > c)

    def test_is_near(self):
        pass

    def test_is_near_all(self):
        pass

    def test_is_far(self):
        pass

    def test_is_far_all(self):
        pass

    def test_at_same_height(self):
        pass

    def test_at_same_height_all(self):
        pass

    def test_at_same_width(self):
        pass

    def test_at_same_width_all(self):
        pass

    def test_aligned_with(self):
        pass

class SegmentTest(unittest.TestCase):

    def setUp(self):
        self.s = Segment(Joint('', 10, 15), Joint('', 15, 10))
        self.s1 = Segment(Joint('', 18, 18), Joint('', 21, 21))
        self.s2 = Segment(Joint('', 17, 17), Joint('', 13, 13))
        self.s3 = Segment(Joint('', 12, 12), Joint("", 6, 6))
        self.s4 = Segment(Joint('', 9, 9), Joint('', 4, 4))

    def test_above(self):
        j1 = Joint("", 13, 18)
        j2 = Joint("", 12, 13)
        j3 = Joint("", 8, 9)
        a = self.s.above(j1)
        b = self.s.above(j2)
        c = self.s.above(j3)
        self.assertTrue(a > b > c)

    def test_above_all(self):
        a = self.s4.above(self.s)
        b = self.s3.above(self.s)
        c = self.s2.above(self.s)
        d = self.s1.above(self.s)
        self.assertTrue(a > b > c >= d)

    def test_below(self):
        j1 = Joint("", 13, 18)
        j2 = Joint("", 12, 13)
        j3 = Joint("", 8, 9)
        a = self.s.below(j3)
        b = self.s.below(j2)
        c = self.s.below(j1)
        self.assertTrue(a > b > c)

    def test_below_all(self):
        a = self.s1.below(self.s)
        b = self.s2.below(self.s)
        c = self.s3.below(self.s)
        d = self.s4.below(self.s)
        self.assertTrue(a > b > c >= d)

    def test_to_the_right(self):
        j1 = Joint("right", 18, 13)
        j2 = Joint("mid", 13, 12)
        j3 = Joint("left", 9, 8)
        a = self.s.to_the_right(j3)
        b = self.s.to_the_right(j2)
        c = self.s.to_the_right(j1)
        self.assertTrue(a > b > c)

    def test_to_the_right_all(self):
        a = self.s1.to_the_right(self.s)
        b = self.s2.to_the_right(self.s)
        c = self.s3.to_the_right(self.s)
        d = self.s4.to_the_right(self.s)
        self.assertTrue(a > b > c >= d)

    def test_to_the_left(self):
        j1 = Joint("right", 18, 13)
        j2 = Joint("mid", 13, 12)
        j3 = Joint("left", 9, 8)
        a = self.s.to_the_left(j1)
        b = self.s.to_the_left(j2)
        c = self.s.to_the_left(j3)
        self.assertTrue(a > b > c)

    def test_to_the_left_all(self):
        a = self.s4.to_the_left(self.s)
        b = self.s3.to_the_left(self.s)
        c = self.s2.to_the_left(self.s)
        d = self.s1.to_the_left(self.s)
        self.assertTrue(a > b > c >= d)


class LimbTest(unittest.TestCase):

    def setUp(self):
        self.l = Limb([Joint('', 10, 15), Joint('', 15, 10)])
        self.s1 = Segment(Joint('', 18, 18), Joint('', 21, 21))
        self.s2 = Segment(Joint('', 17, 17), Joint('', 13, 13))
        self.s3 = Segment(Joint('', 12, 12), Joint("", 6, 6))
        self.s4 = Segment(Joint('', 9, 9), Joint('', 4, 4))

    def test_above(self):
        j1 = Joint("", 13, 18)
        j2 = Joint("", 12, 13)
        j3 = Joint("", 8, 9)
        a = self.l.above(j1)
        b = self.l.above(j2)
        c = self.l.above(j3)
        self.assertTrue(a > b > c)

    def test_above_all(self):
        a = self.s4.above(self.l)
        b = self.s3.above(self.l)
        c = self.s2.above(self.l)
        d = self.s1.above(self.l)
        self.assertTrue(a > b > c >= d)

    def test_below(self):
        j1 = Joint("", 13, 18)
        j2 = Joint("", 12, 13)
        j3 = Joint("", 8, 9)
        a = self.l.below(j3)
        b = self.l.below(j2)
        c = self.l.below(j1)
        self.assertTrue(a > b > c)

    def test_below_all(self):
        a = self.s1.below(self.l)
        b = self.s2.below(self.l)
        c = self.s3.below(self.l)
        d = self.s4.below(self.l)
        self.assertTrue(a > b > c >= d)

    def test_to_the_right(self):
        j1 = Joint("right", 18, 13)
        j2 = Joint("mid", 13, 12)
        j3 = Joint("left", 9, 8)
        a = self.l.to_the_right(j3)
        b = self.l.to_the_right(j2)
        c = self.l.to_the_right(j1)
        self.assertTrue(a > b > c)

    def test_to_the_right_all(self):
        a = self.s1.to_the_right(self.l)
        b = self.s2.to_the_right(self.l)
        c = self.s3.to_the_right(self.l)
        d = self.s4.to_the_right(self.l)
        self.assertTrue(a > b > c >= d)

    def test_to_the_left(self):
        j1 = Joint("right", 18, 13)
        j2 = Joint("mid", 13, 12)
        j3 = Joint("left", 9, 8)
        a = self.l.to_the_left(j1)
        b = self.l.to_the_left(j2)
        c = self.l.to_the_left(j3)
        self.assertTrue(a > b > c)

    def test_to_the_left_all(self):
        a = self.s4.to_the_left(self.l)
        b = self.s3.to_the_left(self.l)
        c = self.s2.to_the_left(self.l)
        d = self.s1.to_the_left(self.l)
        self.assertTrue(a > b > c >= d)
