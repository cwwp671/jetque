"""
File: src.animations.animation_factory.py

    Class: AnimationFactory
        Attributes:
            position_map = {
				"Top-Left": QPointF(0.0, 0.0),
				"Top-Center": QPointF(overlay.width / 2.0, 0.0),
				"Top-Right": QPointF(overlay.width, 0.0),
				"Middle-Left": QPointF(0.0, overlay.height / 2.0),
				"Middle-Center": QPointF(overlay.width / 2.0, overlay.height / 2.0),
				"Middle-Right": QPointF(overlay.width, overlay.height / 2.0),
				"Bottom-Left": QPointF(0.0, overlay.height),
				"Bottom-Center": QPointF(overlay.width / 2.0, overlay.height),
				"Bottom-Right": QPointF(overlay.width, overlay.height)
			} # Maps user-friendly locations to mathematical positions
			direction_map = {
				"Left": -1,
				"Right": 1,
				"Up": -1,
				"Down": 1
			} # Maps user-friendly directions to their numerical representation
			easing_map = {
				"Linear": QEasingCurve.Type.Linear,
				"In-Quadratic": QEasingCurve.Type.InQuad,
				"Out-Quadratic": QEasingCurve.Type.OutQuad,
				"In-Out-Quadratic": QEasingCurve.Type.InOutQuad,
				"Out-In-Quadratic": QEasingCurve.Type.OutInQuad,
				"In-Cubic": QEasingCurve.Type.InCubic,
				"Out-Cubic": QEasingCurve.Type.OutCubic,
				"In-Out-Cubic": QEasingCurve.Type.InOutCubic,
				"Out-In-Cubic": QEasingCurve.Type.OutInCubic,
				"In-Quartic": QEasingCurve.Type.InQuart,
				"Out-Quartic": QEasingCurve.Type.OutQuart,
				"In-Out-Quartic": QEasingCurve.Type.InOutQuart,
				"Out-In-Quartic": QEasingCurve.Type.OutInQuart,
				"In-Quintic": QEasingCurve.Type.InQuint,
				"Out-Quintic": QEasingCurve.Type.OutQuint,
				"In-Out-Quintic": QEasingCurve.Type.InOutQuint,
				"Out-In-Quint": QEasingCurve.Type.OutInQuint,
				"In-Sinusoidal": QEasingCurve.Type.InSine,
				"Out-Sinusoidal": QEasingCurve.Type.OutSine,
				"In-Out-Sinusoidal": QEasingCurve.Type.InOutSine,
				"Out-In-Sinusoidal": QEasingCurve.Type.OutInSine,
				"In-Exponential": QEasingCurve.Type.InExpo,
				"Out-Exponential": QEasingCurve.Type.OutExpo,
				"In-Out-Exponential": QEasingCurve.Type.InOutExpo,
				"Out-In-Exponential": QEasingCurve.Type.OutInExpo,
				"In-Circular": QEasingCurve.Type.InCirc,
				"Out-Circular": QEasingCurve.Type.OutCirc,
				"In-Out-Circular": QEasingCurve.Type.InOutCirc,
				"Out-In-Circular": QEasingCurve.Type.OutInCirc,
				"In-Elastic": QEasingCurve.Type.InElastic,
				"Out-Elastic": QEasingCurve.Type.OutElastic,
				"In-Out-Elastic": QEasingCurve.Type.InOutElastic,
				"Out-In-Elastic": QEasingCurve.Type.OutInElastic,
				"In-Back": QEasingCurve.Type.InBack,
				"Out-Back": QEasingCurve.Type.OutBack,
				"In-Out-Back": QEasingCurve.Type.InOutBack,
				"Out-In-Back": QEasingCurve.Type.OutInBack,
				"In-Bounce": QEasingCurve.Type.InBounce,
				"Out-Bounce": QEasingCurve.Type.OutBounce,
				"In-Out-Bounce": QEasingCurve.Type.InOutBounce,
				"Out-In-Bounce": QEasingCurve.Type.OutInBounce
			} # Maps user-friendly easing styles to easing curves
			jiggle_map = {
				"Low": 0.075,
				"Medium": 0.050,
				"High": 0.025
			} # Maps user-friendly jiggle settings to their numerical representation
        Methods:
            create_animation(config)
				# The code that handles creating animations with the config file should be a shell for now and the specific logic will be implemented later
                # Parses configuration
                # Translates parameters using mappings
                # Converts positions and directions to numerical values
                # Instantiates the appropriate animation class with converted parameters
"""
