import pymunk as pm

class TimeScale(object):
    """
    Timescale manages how large the next time step is for the physics and graphics engines.
    """
    # Minimum value of
    __BASE_SCALE = 1
    __MIN_SCALE = 0.125
    __MAX_SCALE = 512.0
    scale = 1
    __BASE_STEP_SIZE = 1/64
    step_size = __BASE_STEP_SIZE

    @classmethod
    def faster(cls):
        """
        Doubles the current step size.
        """
        return cls._set_scale(cls.scale*2)

    @classmethod
    def slower(cls):
        """
        Halfs the current step size.
        """
        return cls._set_scale(cls.scale/2)

    @classmethod
    def reset(cls):
        """
        Resets the step size to default size
        """
        return cls._set_scale(cls.__BASE_SCALE)

    @classmethod
    def _set_scale(cls, scale):
        """
        Sets the step size to the scale value.

        :param scale: Value to set the step size to.
        :type scale: double
        """
        if cls.__MIN_SCALE <= scale <= cls.__MAX_SCALE:
            cls.scale = scale
            cls._update_step_size()
            return True
        return False

    @classmethod
    def _update_step_size(cls):
        """
        Update the step size variable.
        """
        cls.step_size = cls.__BASE_STEP_SIZE*cls.scale
