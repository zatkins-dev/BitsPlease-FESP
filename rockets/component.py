import pymunk as pm
from physics.collision import CT_COMPONENT

class Component(pm.Poly):
    """Extention of pymunk Poly class with properties for sprites/textures.

    Args:
        body (Body): Body to attach component to
        vertices (List(Vec2d)): Vertices of Poly shape
        transform (Transform): Transformation to apply to shape
        radius (Float): Edge radius of shape for smoothing

    Attributes:
        _sprite (Surface): pygame Surface holding image of component

    """
    def __init__(self, body, vertices, transform=None, radius=0):
        super().__init__(body, vertices, transform, radius)
        self.collision_type = CT_COMPONENT
        self._key = None
        self.destroyed = False

    @property
    def key(self):
        """Activation key for component

        Returns:
            Int: Key value

        """
        if self._key is None:
            return None
        return self._key

    @key.setter
    def key(self, k):
        """Setter for {key} property

        Args:
            k (Int): New key value.

        """
        self._key = k

    @property
    def sprite(self):
        """Image Sprite for the component

        Returns:
            Surface: Component Sprite
        """
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        """Setter for {sprite} property

        Args:
            sprite (surface): New Surface to use as component sprite
        """
        self._sprite = sprite