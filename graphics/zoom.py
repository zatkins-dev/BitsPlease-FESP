class Zoom(object):
    """
    Utility class to manage zooming in and out of the rocket
    """
    def __init__(self, base_zoom=1, min_zoom=2**-16, max_zoom=8):
        """
        The initialization method sets the zoom variables for the class

        :param base_zoom: The default level of zoom
        :type base_zoom: integer
        :param min_zoom: The minumum magnification
        :type base_zoom: double
        :param max_zoom: The maximum magnification
        :type max_zoom: double
        """
        self.__base_zoom = base_zoom
        self.__min_zoom = min_zoom
        self.__max_zoom = max_zoom
        self.zoom = self.__base_zoom

    def zoom_in(self):
        """
        Sets the zoom level to twice the current level.
        """
        return self._set_zoom(self.zoom*2)

    def zoom_out(self):
        """
        Sets the zoom level to half the current level.
        """
        return self._set_zoom(self.zoom/2)

    def reset(self):
        """
        Resets the zoom level to the base zoom level
        """
        while self.zoom != self.__base_zoom:
            if self.zoom > self.__base_zoom:
                if not self.zoom_out(): return False
            else:
                if not self.zoom_in(): return False
        return True

    def _set_zoom(self, zoom):
        """
        Changes the zoom level to the desired amount
        """
        if self.__min_zoom <= zoom <= self.__max_zoom:
            self.zoom = zoom
            return True
        return False
