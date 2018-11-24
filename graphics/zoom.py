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
        while self.zoom != self.__base_zoom:
            if self.zoom > self.__base_zoom:
                if not self.zoom_out(): return False
            else:
                if not self.zoom_in(): return False
        return True

    def _set_zoom(self, zoom):
        if self.__min_zoom <= zoom <= self.__max_zoom:
            self.zoom = zoom
            return True
        return False