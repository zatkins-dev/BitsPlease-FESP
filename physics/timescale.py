import pymunk as pm 

class TimeScale(object):
    # Minimum value of 
    __BASE_SCALE = 1
    __MIN_SCALE = 0.125
    __MAX_SCALE = 64.0
    scale = 1
    __BASE_STEP_SIZE = 1/64
    step_size = __BASE_STEP_SIZE
    

    @classmethod
    def scale_speed(cls, scale):
        if cls.__MIN_SCALE <= scale <= cls.__MAX_SCALE:
            cls.scale = scale
            cls._update_step_size()
            return True
        return False
    
    @classmethod
    def reset(cls):
        cls.scale_speed(cls.__BASE_SCALE)

    @classmethod
    def _update_step_size(cls):
        cls.step_size = cls.__BASE_STEP_SIZE/cls.scale