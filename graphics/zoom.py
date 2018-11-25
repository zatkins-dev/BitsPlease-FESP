class Zoom(object):
    """
    Utility class to manage zooming in and out of the rocket

    :param float base_zoom: The default level of zoom
    :param float min_zoom: The minumum magnification
    :param float max_zoom: The maximum magnification
    """

    #: The starting zoom level
    _base_zoom = 1
    #:  The minumum magnification
    _min_zoom = 2**-16
    #:  The maxumum magnification
    _max_zoom = 8
    #:  The current zoom level
    _zoom = _base_zoom

    def __init__(self, base_zoom=1, min_zoom=2**-16, max_zoom=8):
        """
        The initialization method sets the zoom variables for the class

        
        """
        self._base_zoom = base_zoom
        self._min_zoom = min_zoom
        self._max_zoom = max_zoom
        self._zoom = self._base_zoom

    @property
    def zoom(self):
        """
        Property storing the current value of :py:attr:`_zoom`, supports setting and getting.
        """
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        """
        Changes the zoom level to the desired amount
        """
        if self._min_zoom <= zoom <= self._max_zoom:
            self._zoom = zoom

    def zoom_in(self):
        """
        Sets the zoom level to twice the current level.
        """
        self.zoom = (self._zoom*2)

    def zoom_out(self):
        """
        Sets the zoom level to half the current level.
        """
        self.zoom = (self._zoom/2)

    def reset(self):
        """
        Resets the zoom level to the base zoom level
        """
        while self._zoom != self._base_zoom:
            if self._zoom > self._base_zoom:
                if not self.zoom_out(): return False
            else:
                if not self.zoom_in(): return False
        return True

    
