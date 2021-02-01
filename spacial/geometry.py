from typing import Iterable
from math import sqrt


# represents an 2-dimensional vector
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector'):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, factor: float):
        return Vector(self.x * factor, self.y * factor)

    def __truediv__(self, factor: float):
        return Vector(self.x / factor, self.y / factor)

    def equals(self, other: 'Vector', tolerance: float):
        return abs(self.x - other.x) <= tolerance and abs(self.y - other.y) < tolerance

    def dot(self, other: 'Vector'):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return sqrt(self.dot(self))


# represents a matrix with two rows (i, j) and two columns
class Matrix:
    def __init__(self, ix: float, iy: float, jx: float, jy: float):
        self.ix = ix
        self.iy = iy
        self.jx = jx
        self.jy = jy

    def __eq__(self, other: 'Matrix'):
        return self.ix == other.ix and self.iy == other.iy and self.jx == other.jx and self.jy == other.jy

    def __add__(self, other: 'Matrix'):
        return Matrix(self.ix + other.ix, self.iy + other.iy, self.jx + other.jx, self.jy + other.jy)

    def __sub__(self, other: 'Matrix'):
        return Matrix(self.ix - other.ix, self.iy - other.iy, self.jx - other.jx, self.jy - other.jy)

    def __neg__(self):
        return Matrix(-self.ix, -self.iy, -self.jx, -self.jy)

    def __mul__(self, factor: float):
        return Matrix(self.ix * factor, self.iy * factor, self.jx * factor, self.jy * factor)

    def __truediv__(self, factor: float):
        return Matrix(self.ix / factor, self.iy / factor, self.jx / factor, self.jy / factor)

    def multiply_i(self, v: Vector):
        return self.ix * v.x + self.iy * v.y

    def multiply_j(self, v: Vector):
        return self.jx * v.x + self.jy * v.y

    def multiply(self, v: Vector):
        return Vector(self.multiply_i(v), self.multiply_j(v))

    def det(self):
        return self.ix * self.jy - self.iy * self.jx

    def inverse(self):
        d = self.det()
        return Matrix(self.jy / d, -self.iy / d, -self.jx / d, self.ix / d)


# represents an 2-dimensional rectangle
class Rectangle:
    def __init__(self, from_point: Vector, to_point: Vector):
        self.bottom_left = Vector(min(from_point.x, to_point.x), min(from_point.y, to_point.y))
        self.top_right = Vector(max(from_point.x, to_point.x), max(from_point.y, to_point.y))
        self.bottom_right = Vector(self.top_right.x, self.bottom_left.y)
        self.top_left = Vector(self.bottom_left.x, self.top_right.y)

    def __add__(self, other: Vector):
        return Rectangle(self.bottom_left + other, self.top_right + other)

    def __sub__(self, other: Vector):
        return Rectangle(self.bottom_left - other, self.top_right - other)

    def __mul__(self, factor: float):
        return Rectangle(self.bottom_left * factor, self.top_right * factor)

    def __truediv__(self, factor: float):
        return Rectangle(self.bottom_left / factor, self.top_right / factor)

    def equals(self, other: 'Rectangle', tolerance: float):
        return (self.bottom_left.equals(other.bottom_left, tolerance) and
                self.top_right.equals(other.top_right, tolerance))

    # centre point of the rectangle
    def centre(self):
        return Vector((self.bottom_left.x + self.top_right.x) / 2.0,
                      (self.bottom_left.y + self.top_right.y) / 2.0)

    # point is on or within the boundary
    def contains(self, point: Vector, tolerance: float):
        return (self.bottom_left.x - tolerance <= point.x <= self.top_right.x + tolerance and
                self.bottom_left.y - tolerance <= point.y <= self.top_right.y + tolerance)

    # list of intersections with the rectangle boundary
    def intersections_with(self, line: 'Line', tolerance: float):
        boundaries = [
            Line(self.bottom_left, self.top_left),
            Line(self.bottom_right, self.top_right),
            Line(self.bottom_left, self.bottom_right),
            Line(self.top_left, self.top_right)]
        return [intersection
                for intersection in [boundary.intersection_with(line, tolerance, True) for boundary in boundaries]
                if intersection is not None]


# represents a line between two 2-dimensional points
class Line:
    def __init__(self, start_point: Vector, end_point: Vector):
        self.start_point = start_point
        self.end_point = end_point
        self.bounds = Rectangle(start_point, end_point)
        direction = end_point - start_point
        self.unit_direction = direction / direction.magnitude()

    def __add__(self, other: Vector):
        return Line(self.start_point + other, self.end_point + other)

    def __sub__(self, other: Vector):
        return Line(self.start_point - other, self.end_point - other)

    def __mul__(self, factor: float):
        return Line(self.start_point * factor, self.end_point * factor)

    def __truediv__(self, factor: float):
        return Line(self.start_point / factor, self.end_point / factor)

    def contains(self, point: Vector, tolerance: float, bounded: bool):
        return self.is_parallel_to(Line(self.start_point, point), tolerance) and (
                not bounded or self.bounds.contains(point, tolerance))

    def is_parallel_to(self, other: 'Line', tolerance: float):
        return 1.0 - abs(self.unit_direction.dot(other.unit_direction)) < tolerance

    def intersection_with(self, other: 'Line', tolerance: float, bounded: bool):
        if self.is_parallel_to(other, tolerance):
            return None
        d = Matrix(self.unit_direction.x, other.unit_direction.x, self.unit_direction.y, other.unit_direction.y)
        lamb = d.inverse().multiply_i(other.start_point - self.start_point)
        intersection = self.start_point + self.unit_direction * lamb
        return (
            intersection
            if not bounded or (
                            self.bounds.contains(intersection, tolerance) and
                            other.bounds.contains(intersection, tolerance))
            else None)
