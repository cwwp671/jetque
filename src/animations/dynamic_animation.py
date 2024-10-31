"""
File: src.animations.dynamic_animation.py

    Class: DynamicAnimation(Animation)
        Attributes:
            # Horizontal Direction (int From AnimationFactory direction_map)
            # Vertical Direction (int From AnimationFactory direction_map)
            # Ending Position (QPointF From AnimationFactory position_map)
            # Easing Style (QEasingCurve.Type From AnimationFactory easing_map)
        Methods:
		    __init__(parameters supplied from config / AnimationFactory)
				# Super the Parent Init
                # Initializes any dynamic specific attributes
            play()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
            stop()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
            setup_animations()
                # Possibility this is an Abstract method to be overridden by individual animations
				# Possibility this is not an Abstract method and houses common logic
            connect_signals()
				# Supers the Parent
                # Connects any necessary dynamic animation signals to handlers
			connect_slots()
				# Supers the Parent
				# Connects any necessary dynamic animation slots to handlers
"""
