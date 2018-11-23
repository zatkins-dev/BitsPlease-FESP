class Zoom(object):
    def __init__(self, base_zoom=1, min_zoom=2**-16, max_zoom=8):
        self.__base_zoom = base_zoom
        self.__min_zoom = min_zoom
        self.__max_zoom = max_zoom
        self.zoom = self.__base_zoom

    def zoom_in(self):
        return self._set_zoom(self.zoom*2)

    def zoom_out(self):
        return self._set_zoom(self.zoom/2)
    
    def reset(self):
        return self._set_zoom(self.__base_zoom)

    def _set_zoom(self, zoom):
        if self.__min_zoom <= zoom <= self.__max_zoom:
            self.zoom = zoom
            return True
        return False