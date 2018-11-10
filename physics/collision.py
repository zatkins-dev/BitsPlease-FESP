import pymunk
from rockets import Component, Thruster, Rocket
from physics import Physics
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
_threshold_for_failure = 300000 # kg*m/s^2


# Components that have broken from a collision
# Used as a queue to process in post-collision
_failed_components = []


# Collision Types
CT_COMPONENT = 1
CT_THRUSTER = 2
CT_CONSTRAINT = 3
CT_CELESTIAL_BODY = 4
CT_STRUCTURE = 5


# Collision Pre-Solver: Component, Celestial Body
def pre_solve_component_celestialbody(arbiter, space, _):
    component = None
    if arbiter.total_impulse.length/50 > _threshold_for_detach:
        print(arbiter.total_impulse.length/50, arbiter.shapes)
    for shape in arbiter.shapes:
        if isinstance(shape, Component):
            component = shape
    # if component is not None and arbiter.total_impulse.length/50 > _threshold_for_detach:
    #     detached_body = pymunk.Body()
    #     old_body = component.body
    #     detached_body.position = old_body.position
    #     space.remove(component)
    #     component.body = detached_body
    #     space.reindex_shapes_for_body(old_body)
    #     space.add(detached_body, component)
    #     detached_body.apply_impulse_at_local_point(arbiter.impulse)
    #     print ("Detached component: ", component)
    if component is not None and arbiter.total_impulse.length/50 > _threshold_for_failure:
        _failed_components.append(component)
        print ("Marked failed component for removal: ", component)
    return True


def post_solve_component_celestialbody(arbiter, space, _):
    # component = None
    # planet = None
    # for shape in arbiter.shapes:
    #     if isinstance(shape, Component):
    #         component = shape
    #     else:
    #         planet = shape
    # print(arbiter.shapes)
    # component.body.apply_force_at_local_point(10*component.body.mass*planet.friction*9.8 * component.body.velocity.normalized(), component.body.center_of_gravity)
    for component in _failed_components:
        space.remove(component)
        component.body.components.remove(component)
        component.body.apply_impulse_at_local_point(arbiter.total_impulse)
        print ("Removed failed component: ", component)
        _failed_components.remove(component)
    return True


        

        