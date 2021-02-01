import unittest
from spacial.geometry import Rectangle, Vector
from spacial.world import Entity, World


tolerance: float = 1e-7


class EntityTest(unittest.TestCase):
    def test_init(self):
        name = "I"
        bounds = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer = 1
        e = Entity(name, bounds, layer)
        self.assertEqual(e.name, name)
        self.assertEqual(e.bounds, bounds)
        self.assertEqual(e.layer, layer)

    def test_equals(self):
        name1 = "I"
        bounds1 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer1 = 1
        e1 = Entity(name1, bounds1, layer1)
        name2 = "I"
        bounds2 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer2 = 1
        e2 = Entity(name2, bounds2, layer2)
        self.assertTrue(e1.equals(e2, tolerance))


class WorldTest(unittest.TestCase):
    def test_init(self):
        name = "I"
        e = Entity(name, Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0)), 0)
        w = World([e, e])
        self.assertEqual(len(w.entities), 1)
        self.assertIn(name, w.entities)
        self.assertTrue(w.entities[name].equals(e, tolerance))

    def test_equals(self):
        name1 = "I"
        bounds1 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer1 = 1
        e1 = Entity(name1, bounds1, layer1)
        name2 = "Thing"
        bounds2 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer2 = 1
        e2 = Entity(name2, bounds2, layer2)
        name3 = "I"
        bounds3 = Rectangle(Vector(0.0, 0.0), Vector(2.0, 2.0))
        layer3 = 1
        e3 = Entity(name3, bounds3, layer3)
        name4 = "I"
        bounds4 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer4 = 2
        e4 = Entity(name4, bounds4, layer4)

        w1 = World([e1, e2, e3, e4])
        w2 = World([e1, e2, e3, e4])
        w3 = World([e1])

        self.assertTrue(w1.equals(w2, tolerance))
        self.assertFalse(w1.equals(w3, tolerance))

    def test_find(self):
        name1 = "I"
        bounds1 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer1 = 1
        e1 = Entity(name1, bounds1, layer1)
        name2 = "Thing"
        bounds2 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer2 = 1
        e2 = Entity(name2, bounds2, layer2)
        w = World([e1, e2])
        self.assertIsNotNone(w.find("I"))
        self.assertTrue(w.find("I").equals(e1, tolerance))
        self.assertIsNotNone(w.find("Thing"))
        self.assertTrue(w.find("Thing").equals(e2, tolerance))

    def test_find_near_to(self):
        name1 = "I"
        bounds1 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer1 = 1
        e1 = Entity(name1, bounds1, layer1)
        name2 = "Thing"
        bounds2 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer2 = 1
        e2 = Entity(name2, bounds2, layer2)
        w = World([e1, e2])
        near = w.find_near_to(e1, tolerance)
        self.assertEqual(len(near), 1)
        for n in near:
            self.assertTrue(n.equals(e2, tolerance))

    def test_remove(self):
        name1 = "I"
        bounds1 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer1 = 1
        e1 = Entity(name1, bounds1, layer1)
        name2 = "Thing"
        bounds2 = Rectangle(Vector(0.0, 0.0), Vector(1.0, 1.0))
        layer2 = 1
        e2 = Entity(name2, bounds2, layer2)
        w = World([e1, e2])
        w.remove("Thing")
        self.assertIsNone(w.find("Thing"))
        self.assertIsNotNone(w.find("I"))
        self.assertTrue(w.find("I").equals(e1, tolerance))


if __name__ == '__main__':
    unittest.main()
