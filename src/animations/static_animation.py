"""
File: src.animations.static_animation.py

    Class: StaticAnimation(Animation)
        Attributes:
            # Jiggle (Bool)
            # Jiggle Intensity (float From AnimationFactory jiggle_map)
        Methods:
		    __init__(parameters supplied from config / AnimationFactory)
				# Super the Parent Init
                # Initializes any static specific attributes
            play()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
            stop()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
            setup_animations()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
			apply_jiggle()
				# Manipulates the position with jiggle effect
            connect_signals()
				# Supers the Parent
                # Connects any necessary static animation signals to handlers
			connect_slots()
				# Supers the Parent
				# Connects any necessary static animation slots to handlers
"""
