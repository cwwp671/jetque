"""
File: src.animations.dynamics.swivel_animation.py

    Class: SwivelAnimation(DynamicAnimation)
        Attributes:
            # Phase 1 Percentage (percentage of the animation duration)
			# Phase 2 Percentage (percentage of the animation duration)
			# Phase 1 Swivel Position (QPointF)
        Methods:
			__init__(parameters supplied from config / AnimationFactory)
				# Super the Parent Init
                # Initializes any swivel specific attributes
            play()
                # Plays the animations involved
            stop()
                # Stops the animations involved
            setup_animations()
                # Sets up any necessary swivel animation settings and groups
			setup_swivel_position()
				# Sets up the swivel position, which will end up being the ending position of phase 1 and the starting position of phase 2
				# The swivel position will be located at whatever percentage of the animation Phase 1 is. So if Phase 1 is 50% of the duration it will be halfway between Starting Position and Ending Position, etc.
            connect_signals()
				# Supers the Parent
                # Connects any necessary swivel animation signals to handlers
			connect_slots()
				# Supers the Parent
				# Connects any necessary swivel animation slots to handlers

"""
