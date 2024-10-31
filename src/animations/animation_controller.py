"""
File: src.animations.animation_controller.py

Class: AnimationController(QObject)
Attributes:
dynamic_animations[
    [directional_animations],
    [parabola_animations],
    [swivel_animations]
]: List of active dynamic animations
static_animations[
    [stationary_animations],
    [pow_animations]
] # List of active static animations which contains lists of each type
detect_intersections_timer # A timer to loop intersection detection if needed
Methods:
__init__(self, overlay(the parent widget), config)

setup_animation(animation creation attributes) # If this method makes sense in the controller, this will trigger the creation of the animation through the AnimationFactory as well as setup any signals or slots that are necessary

start_animation(animation) # Start the animation and add it to its given active animation list as well as utilize any signals or slots that are necessary

stop_animation(animation) # Might not be necessary to have this method

handle_animation_finished(animation) # Utilizes any signals or slots that are necessary in order to clear up animations from memory after they finish. Utilizes clean_up_animation()

detect_intersections() # Detects intersecting animations of the same type as well as utilize any signals or slots that are necessary

are_intersecting(animation_label_1, animation_label_2) # Determine if two animations are intersecting based on their label geometry as well as utilize any signals or slots that are necessary

handle_intersection() # Handles what should happen on an intersection of an animation and hands it off to the animation to adjust as well as utilize any signals or slots that are necessary. For now don't implement individual collision logic, but instead setup the structure that allows individual collisions based on type of animation

clean_up_animation(animation) # Handles cleanup in a safe way after an animation finishes as well as utilize any signals or slots that are necessary
"""
