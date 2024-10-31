"""
File: src.animations.animation.py

    Class: Animation(QObject)
        Attributes:
            # ID (int) (Having this just incase it ever improves CPU effeciency, though if QObjects have it built it, we should utilize that instead)
            # Type (Animation Style)
            # Sound (Uploaded Sound File)
            # Label (instance of AnimationLabel)
            # Duration (Float)
            # Starting Position (QPointF From AnimationFactory position_map)
            # Fade In (Bool)
            # Fade In Percentage (Float) (Percentage of duration to apply Fade In)
            # Fade In Easing Style (QEasingCurve.Type From AnimationFactory easing_map)
            # Fade Out (Bool)
            # Fade Out Percentage (Float) (Percentage of duration to apply Fade Out)
            # Fade Out Easing Style (QEasingCurve.Type From AnimationFactory easing_map)
        Methods:
            __init__(parameters supplied from config / AnimationFactory)
				# Super the Parent Init
                # Initializes attributes
                # Creates AnimationLabel
            play()
                # Abstract class to be overridden by individual animations
            stop()
                # Abstract class to be overridden by individual animations
            setup_animations()
                # Abstract class to be overridden by individual animations
            connect_signals()
                # Connects any necessary animation signals to handlers
			connect_slots()
				# Connects any necessary animation slots to handlers
			initialize_sound()
                # Loads sound if enabled
			play_sound()
				# Plays sound
"""
