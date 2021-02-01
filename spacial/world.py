from typing import Iterable
from spacial.geometry import Rectangle, Vector


# represents a named entity
class Entity:
    def __init__(self, name: str, bounds: Rectangle, layer: int):
        self.name = name
        self.bounds = bounds
        self.layer = layer

    def equals(self, other: 'Entity', tolerance: float):
        return self.name == other.name and self.bounds.equals(other.bounds, tolerance) and self.layer == other.layer


# represents world containing many entities
class World:
    def __init__(self, entities: Iterable[Entity]):
        self.entities = {}
        for e in entities:
            self.entities[e.name] = e

    # whether world is same as other world
    def equals(self, other: 'World', tolerance: float):
        return len(set(self.entities.keys()).difference(other.entities.keys())) == 0 and all(
            [self.entities[k].equals(other.entities[k], tolerance) for k in self.entities.keys()])

    # found named entity or None if not found
    def find(self, name: str):
        return self.entities[name] if name in self.entities else None

    # entities whose centres are at the specified point
    def find_near_to(self, target: Entity, tolerance: float):
        return [entity
                for name, entity in self.entities.items()
                if entity.bounds.centre().equals(target.bounds.centre(), tolerance) and name != target.name]

    # remove the named entity
    def remove(self, name: str):
        del self.entities[name]
