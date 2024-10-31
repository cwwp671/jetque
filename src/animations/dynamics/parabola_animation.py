"""
File: src.animations.dynamics.parabola_animation.py

    Class: ParabolaAnimation(DynamicAnimation)
        Attributes:
            # Vertex Position (QPointF: x = halfway between Starting and Ending Position, y = depends on direction of up/down. will be one unit of position_map up or down without going out of bounds, but there will be checks in the animationfactory before this gets passed its assignment to make sure its within bounds)
        Methods:
			__init__(parameters supplied from config / AnimationFactory)
				# Super the Parent Init
                # Initializes any parabola specific attributes
            play()
                # Plays the animations involved
            stop()
                # Stops the animations involved
            setup_animations()
                # Sets up any necessary parabola animation settings and groups
            connect_signals()
				# Supers the Parent
                # Connects any necessary parabola animation signals to handlers
			connect_slots()
				# Supers the Parent
				# Connects any necessary parabola animation slots to handlers

"""
