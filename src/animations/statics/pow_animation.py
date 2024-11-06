"""
File: src.animations.statics.pow_animation.py

    Class: PowAnimation(StaticAnimation)
        Attributes:
            # Scale Amount (percentage the font scales up to)
			# Scale Easing Style (QEasingCurve.Type From AnimationFactory easing_map)
            # Phase 1 Percentage (percentage of the animation duration)
			# Phase 2 Percentage (percentage of the animation duration)

        Methods:
			__init__(parameters supplied from config / AnimationFactory)
                # Initializes any pow specific attributes before the super
				# Super the Parent Init

            play()
                # Plays the animations involved
            stop()
                # Stops the animations involved
            setup_animations()
                # Sets up any necessary pow animation settings and groups
            connect_signals()
				# Supers the Parent
                # Connects any necessary pow animation signals to handlers
			connect_slots()
				# Supers the Parent
				# Connects any necessary pow animation slots to handlers
"""
