import pymunk
from pymunk.vec2d import Vec2d


# Exports
#__all__ = ["CT_COMPONENT", 
        #    "CT_THRUSTER", 
        #    "CT_CONSTRAINT", 
        #    "CT_CELESTIAL_BODY", 
        #    "CT_STRUCTURE",
        #    "pre_solve_component_celestialbody",
        #    "post_solve_component_celestialbody",
        #    "collision_debug_mode"]


# NOTE: The following callback functions are used for handling collisions
# 1. begin 
#       Two shapes just started touching for the first time this step.
#       func(arbiter, space, data) -> bool
#
# 2. pre_solve
#       Two shapes are touching during this step.
#       func(arbiter, space, data) -> bool
#
# 3. post_solve
#       Two shapes are touching and their collision response has been processed.
#       func(arbiter, space, data)
# 4. separate
#       Two shapes have just stopped touching for the first time this step.
#       func(arbiter, space, data)


collision_debug_mode = False


# TODO: Make these thresholds component specific or calculated
# Maximum post-collision force a component can withstand without breaking off rocket
_threshold_for_detach = 10000 # kg*m/s^2
# Maximum post-collision force a component can withstand without being destroyed
_threshold_for_failure = 10000 # kg*m/s^2


# Components that have broken from a collision
# Used as a queue to process in post-collision
_failed_components = []


# Collision Types
CT_COMPONENT = 2
CT_CELESTIAL_BODY = 1


# Collision Post-Solver: Component, Celestial Body
def post_solve_component_celestialbody(arbiter, space, data):
    component = None
    if arbiter.total_impulse.length/50 > _threshold_for_detach:
        print(arbiter.total_impulse.length/50, arbiter.shapes)
    for shape in arbiter.shapes:
        if shape.collision_type == CT_COMPONENT:
            component = shape
    if component is not None and arbiter.total_impulse.length/50 > _threshold_for_failure:
        component.body.destroyed = True
    return True


        

        