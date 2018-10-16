import pymunk as pm


class Component(pm.Poly):
    def __init__(self, body, vertices, transform=None, radius=0):
        super().__init__(body=body, vertices=vertices, transform=transform, radius=radius)
        self._key = None

    @property
    def key(self):
        if self._key is None:
            return None
        return self._key

    @key.setter
    def key(self, k):
        self._key = k
