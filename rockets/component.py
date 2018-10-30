import pymunk as pm


class Component(pm.Poly):
    """Extention of pymunk Poly class with properties for activation keys.

    Args:
        body (Body): Body to attach component to
        vertices (List(Vec2d)): Vertices of Poly shape
        transform (Transform): Transformation to apply to shape
        radius (Float): Edge radius of shape for smoothing

    Attributes:
        _key (Int): Activation key for component (default: None)

    """

    def __init__(self, body, vertices, transform=None, radius=0):
        super().__init__(body, vertices, transform, radius)
        self._key = None

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
        if self._sprite is None:
            return None
        else
            return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        """Setter for {sprite} property

        Args:
            sprite (surface): New Surface to use as component sprite
        """
        self._sprite = sprite