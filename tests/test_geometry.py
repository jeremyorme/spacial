import unittest
from spacial.geometry import Vector, Matrix, Rectangle, Line


tolerance: float = 1e-7


class VectorTests(unittest.TestCase):
    def test_init(self):
        p = Vector(1.0, 2.0)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)

    def test_add(self):
        p1 = Vector(5.0, 3.0)
        p2 = Vector(6.0, 1.0)
        p3 = p2 + p1
        self.assertTrue(p3.equals(Vector(11.0, 4.0), tolerance))

    def test_sub(self):
        p1 = Vector(5.0, 3.0)
        p2 = Vector(6.0, 1.0)
        p3 = p2 - p1
        self.assertTrue(p3.equals(Vector(1.0, -2.0), tolerance))

    def test_neg(self):
        p1 = Vector(5.0, 3.0)
        p2 = Vector(-5.0, -3.0)
        p3 = -p1
        self.assertTrue(p2.equals(p3, tolerance))

    def test_mul(self):
        p1 = Vector(5.0, 3.0)
        p2 = Vector(15.0, 9.0)
        p3 = p1 * 3.0
        self.assertTrue(p2.equals(p3, tolerance))

    def test_truediv(self):
        p1 = Vector(15.0, 9.0)
        p2 = Vector(5.0, 3.0)
        p3 = p1 / 3.0
        self.assertTrue(p2.equals(p3, tolerance))

    def test_equals(self):
        p1 = Vector(1.0, 2.0)
        p2 = Vector(1.0 + tolerance, 2.0 - tolerance)
        self.assertTrue(p1.equals(p2, tolerance * 2.0))

    def test_dot(self):
        p1 = Vector(0.0, 1.0)
        p2 = Vector(1.0, 0.0)
        self.assertEqual(p1.dot(p2), 0.0)
        self.assertEqual(p1.dot(p1), 1.0)
        self.assertEqual(p2.dot(p2), 1.0)

    def test_magnitude(self):
        self.assertEqual(Vector(3.0, 4.0).magnitude(), 5.0)


class MatrixTests(unittest.TestCase):
    def test_init(self):
        m = Matrix(0.0, 1.0, 2.0, 3.0)
        self.assertEqual(m.ix, 0.0)
        self.assertEqual(m.iy, 1.0)
        self.assertEqual(m.jx, 2.0)
        self.assertEqual(m.jy, 3.0)

    def test_eq(self):
        m1 = Matrix(1.0, 2.0, 3.0, 4.0)
        m2 = Matrix(1.0, 2.0, 3.0, 4.0)
        m3 = Matrix(4.0, 3.0, 2.0, 1.0)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m2, m3)

    def test_add(self):
        m1 = Matrix(5.0, 3.0, 1.0, -1.0)
        m2 = Matrix(6.0, 1.0, 4.0, 2.0)
        m3 = m2 + m1
        self.assertEqual(m3, Matrix(11.0, 4.0, 5.0, 1.0))

    def test_sub(self):
        m1 = Matrix(6.0, 1.0, 4.0, 2.0)
        m2 = Matrix(11.0, 4.0, 5.0, 1.0)
        m3 = m2 - m1
        self.assertEqual(m3, Matrix(5.0, 3.0, 1.0, -1.0))

    def test_neg(self):
        m1 = Matrix(6.0, 1.0, 4.0, 2.0)
        m2 = -m1
        self.assertEqual(m2, Matrix(-6.0, -1.0, -4.0, -2.0))

    def test_mul(self):
        m1 = Matrix(6.0, 1.0, 4.0, 2.0)
        m2 = m1 * 2.0
        self.assertEqual(m2, Matrix(12.0, 2.0, 8.0, 4.0))

    def test_truediv(self):
        m1 = Matrix(6.0, 1.0, 4.0, 2.0)
        m2 = m1 / 2.0
        self.assertEqual(m2, Matrix(3.0, 0.5, 2.0, 1.0))

    def test_multiply(self):
        m = Matrix(0.0, 1.0, 1.0, 0.0)
        p1 = Vector(0.0, 1.0)
        p2 = Vector(1.0, 0.0)
        self.assertTrue(m.multiply(p1).equals(p2, tolerance))

    def test_det(self):
        m = Matrix(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(m.det(), -2.0)

    def test_inverse(self):
        m = Matrix(1.0, 1.0, 1.0, 3.0)
        i = Matrix(1.5, -0.5, -0.5, 0.5)
        self.assertEqual(m.inverse(), i)


class RectangleTests(unittest.TestCase):
    def test_init(self):
        bl = Vector(-2.0, -3.0)
        tr = Vector(1.0, 4.0)
        r = Rectangle(bl, tr)
        self.assertTrue(r.bottom_left.equals(bl, tolerance))
        self.assertTrue(r.top_right.equals(tr, tolerance))
        self.assertTrue(r.bottom_right.equals(Vector(tr.x, bl.y), tolerance))
        self.assertTrue(r.top_left.equals(Vector(bl.x, tr.y), tolerance))

    def test_add(self):
        r = Rectangle(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        ofs = Vector(1.0, 2.0)
        r_add = r + ofs
        self.assertTrue(r_add.bottom_left.equals(r.bottom_left + ofs, tolerance))
        self.assertTrue(r_add.top_right.equals(r.top_right + ofs, tolerance))
        self.assertTrue(r_add.bottom_right.equals(r.bottom_right + ofs, tolerance))
        self.assertTrue(r_add.top_left.equals(r.top_left + ofs, tolerance))

    def test_sub(self):
        r = Rectangle(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        ofs = Vector(1.0, 2.0)
        r_sub = r - ofs
        self.assertTrue(r_sub.bottom_left.equals(r.bottom_left - ofs, tolerance))
        self.assertTrue(r_sub.top_right.equals(r.top_right - ofs, tolerance))
        self.assertTrue(r_sub.bottom_right.equals(r.bottom_right - ofs, tolerance))
        self.assertTrue(r_sub.top_left.equals(r.top_left - ofs, tolerance))

    def test_mul(self):
        r = Rectangle(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        factor = 3.0
        r_mul = r * factor
        self.assertTrue(r_mul.bottom_left.equals(r.bottom_left * factor, tolerance))
        self.assertTrue(r_mul.top_right.equals(r.top_right * factor, tolerance))
        self.assertTrue(r_mul.bottom_right.equals(r.bottom_right * factor, tolerance))
        self.assertTrue(r_mul.top_left.equals(r.top_left * factor, tolerance))

    def test_truediv(self):
        r = Rectangle(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        factor = 3.0
        r_mul = r / factor
        self.assertTrue(r_mul.bottom_left.equals(r.bottom_left / factor, tolerance))
        self.assertTrue(r_mul.top_right.equals(r.top_right / factor, tolerance))
        self.assertTrue(r_mul.bottom_right.equals(r.bottom_right / factor, tolerance))
        self.assertTrue(r_mul.top_left.equals(r.top_left / factor, tolerance))

    def test_equals(self):
        r1 = Rectangle(Vector(-2.0, -1.0), Vector(2.0, 3.0))
        r2 = Rectangle(Vector(-2.0, -1.0), Vector(2.0, 3.0))
        self.assertTrue(r1.equals(r2, tolerance))

    def test_contains(self):
        bl = Vector(-2.0, -3.0)
        tr = Vector(1.0, 4.0)
        r = Rectangle(bl, tr)
        # inside
        self.assertTrue(r.contains(Vector(0.0, 0.0), tolerance))
        # boundary
        self.assertTrue(r.contains(Vector(1.0, 0.0), tolerance))
        self.assertTrue(r.contains(Vector(0.0, 4.0), tolerance))
        self.assertTrue(r.contains(Vector(-2.0, 0.0), tolerance))
        self.assertTrue(r.contains(Vector(0.0, -3.0), tolerance))
        # outside
        self.assertFalse(r.contains(Vector(2.0, 0.0), tolerance))
        self.assertFalse(r.contains(Vector(0.0, 5.0), tolerance))
        self.assertFalse(r.contains(Vector(-3.0, 0.0), tolerance))
        self.assertFalse(r.contains(Vector(0.0, -4.0), tolerance))

    def test_intersections_with(self):
        a_bit = Vector(0.5, 0.5)
        r = Rectangle(Vector(-1.0, -1.0), Vector(1.0, 1.0))

        # line entirely within the rectangle
        l_inside = Line(r.bottom_left + a_bit, r.top_right - a_bit)
        self.assertEqual(len(r.intersections_with(l_inside, tolerance)), 0)

        # line from centre through left boundary
        l_left = Line(r.centre(), r.top_left - a_bit)
        self.assertEqual(len(r.intersections_with(l_left, tolerance)), 1)

        # line from centre through right boundary
        l_right = Line(r.centre(), r.bottom_right + a_bit)
        self.assertEqual(len(r.intersections_with(l_right, tolerance)), 1)

        # line from centre through top boundary
        l_top = Line(r.centre(), r.top_left - a_bit)
        self.assertEqual(len(r.intersections_with(l_top, tolerance)), 1)

        # line from centre through bottom boundary
        l_bottom = Line(r.centre(), r.bottom_right + a_bit)
        self.assertEqual(len(r.intersections_with(l_bottom, tolerance)), 1)

        # line through left and top boundary
        l_left_top = Line(r.top_left - a_bit, r.top_right + a_bit)
        self.assertEqual(len(r.intersections_with(l_left_top, tolerance)), 2)

        # line through bottom and left boundary
        l_bottom_left = Line(r.bottom_right - a_bit, r.top_left - a_bit)
        self.assertEqual(len(r.intersections_with(l_bottom_left, tolerance)), 2)

        # line through right and bottom boundary
        l_right_bottom = Line(r.top_right + a_bit, r.bottom_left + a_bit)
        self.assertEqual(len(r.intersections_with(l_right_bottom, tolerance)), 2)

        # line through top and right boundary
        l_top_right = Line(r.top_left + a_bit, r.bottom_right + a_bit)
        self.assertEqual(len(r.intersections_with(l_top_right, tolerance)), 2)

        # line through left and right boundary
        l_left_right = Line(r.top_left - a_bit, r.bottom_right + a_bit)
        self.assertEqual(len(r.intersections_with(l_left_right, tolerance)), 2)

        # line through top and bottom boundary
        l_top_bottom = Line(r.top_left + a_bit, r.bottom_right - a_bit)
        self.assertEqual(len(r.intersections_with(l_left_right, tolerance)), 2)


class LineTests(unittest.TestCase):
    def test_init(self):
        s = Vector(1.0, 2.0)
        e = Vector(3.0, 4.0)
        ln = Line(s, e)
        self.assertEqual(ln.start_point, s)
        self.assertEqual(ln.end_point, e)

    def test_add(self):
        l_before = Line(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        ofs = Vector(1.0, 2.0)
        l_add = l_before + ofs
        self.assertTrue(l_add.start_point.equals(l_before.start_point + ofs, tolerance))
        self.assertTrue(l_add.end_point.equals(l_before.end_point + ofs, tolerance))

    def test_sub(self):
        l_before = Line(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        ofs = Vector(1.0, 2.0)
        l_sub = l_before - ofs
        self.assertTrue(l_sub.start_point.equals(l_before.start_point - ofs, tolerance))
        self.assertTrue(l_sub.end_point.equals(l_before.end_point - ofs, tolerance))

    def test_mul(self):
        l_before = Line(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        factor = 3.0
        l_add = l_before * factor
        self.assertTrue(l_add.start_point.equals(l_before.start_point * factor, tolerance))
        self.assertTrue(l_add.end_point.equals(l_before.end_point * factor, tolerance))

    def test_truediv(self):
        l_before = Line(Vector(-2.0, -3.0), Vector(1.0, 4.0))
        factor = 3.0
        l_add = l_before / factor
        self.assertTrue(l_add.start_point.equals(l_before.start_point / factor, tolerance))
        self.assertTrue(l_add.end_point.equals(l_before.end_point / factor, tolerance))

    def test_contains(self):
        l1 = Line(Vector(0.0, 0.0), Vector(3.0, 4.0))
        self.assertTrue(l1.contains(Vector(1.5, 2.0), tolerance, True))
        self.assertFalse(l1.contains(Vector(2.0, 1.5), tolerance, True))
        self.assertFalse(l1.contains(Vector(4.5, 6.0), tolerance, True))
        self.assertFalse(l1.contains(Vector(6.0, 4.5), tolerance, True))
        self.assertTrue(l1.contains(Vector(4.5, 6.0), tolerance, False))
        self.assertFalse(l1.contains(Vector(6.0, 4.5), tolerance, False))

    def test_is_parallel_to(self):
        l1 = Line(Vector(3.0, 4.0), Vector(4.0, 6.0))
        l2 = Line(Vector(-1.0, 1.0), Vector(-0.5, 2.0))
        l3 = Line(Vector(3.0, 4.0), Vector(2.0, 2.0))
        self.assertTrue(l1.is_parallel_to(l2, tolerance))
        self.assertTrue(l2.is_parallel_to(l3, tolerance))

    def test_intersection_with(self):
        l1 = Line(Vector(0.0, 0.0), Vector(1.0, 1.0))
        l2 = Line(Vector(0.0, 1.0), Vector(1.0, 0.0))
        l3 = Line(Vector(1.0, 1.0), Vector(2.0, 0.0))
        l4 = Line(Vector(-2.0, 3.0), Vector(-1.0, 2.0))

        # lines intersecting between their end-points
        self.assertTrue(l1.intersection_with(l2, tolerance, True).equals(Vector(0.5, 0.5), tolerance))

        # parallel lines (not intersecting)
        self.assertIsNone(l2.intersection_with(l3, tolerance, False))

        # lines intersecting outside their end-points
        self.assertTrue(l1.intersection_with(l4, tolerance, False).equals(Vector(0.5, 0.5), tolerance))
        self.assertIsNone(l1.intersection_with(l4, tolerance, True))


if __name__ == '__main__':
    unittest.main()
