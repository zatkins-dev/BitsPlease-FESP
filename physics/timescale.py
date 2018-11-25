import pymunk as pm

class TimeScale(object):
    """
    Timescale manages how large the next time step is for the physics and graphics engines.
    """
    #: Base timescale
    _BASE_SCALE = 1
    #: Minimum timescale
    _MIN_SCALE = 0.125
    #: Maximum timescale    
    _MAX_SCALE = 512.0
    #: Current timescale
    scale = 1
    #: Base step size in seconds
    _BASE_STEP_SIZE = 1/64
    #: Current step size
    step_size = _BASE_STEP_SIZE

    @classmethod
    def faster(cls):
        """
        Doubles the current time scale.

        :returns: `True` if set, `False` otherwise
        :rtype: :py:class:`bool`
        """
        return cls._set_scale(cls.scale*2)

    @classmethod
    def slower(cls):
        """
        Halfs the current time scale.

        :returns: `True` if set, `False` otherwise
        :rtype: :py:class:`bool`
        """
        return cls._set_scale(cls.scale/2)

    @classmethod
    def reset(cls):
        """
        Resets the time scale to default

        :returns: `True` if reset, `False` otherwise
        :rtype: :py:class:`bool`
        """
        return cls._set_scale(cls._BASE_SCALE)

    @classmethod
    def _set_scale(cls, scale):
        """
        Sets the :py:attr:`scale` to `scale`, then updates :py:attr:`step_size`

        :param float scale: Value to set the step size to.
        :returns: `True` if set, `False` otherwise
        :rtype: :py:class:`bool`
        """
        if cls._MIN_SCALE <= scale <= cls._MAX_SCALE:
            cls.scale = scale
            cls._update_step_size()
            return True
        return False

    @classmethod
    def _update_step_size(cls):
        """
        Update the :py:attr:`step_size` variable.
        """
        cls.step_size = cls._BASE_STEP_SIZE*cls.scale
