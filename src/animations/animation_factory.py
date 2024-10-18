# jetque/src/animations/animation_factory.py

from src.animations.animation import Animation
from src.animations.angled_animation import AngledAnimation
from src.animations.horizontal_animation import HorizontalAnimation
from src.animations.parabola_animation import ParabolaAnimation
from src.animations.pow_animation import PowAnimation
from src.animations.static_animation import StaticAnimation
from src.animations.straight_animation import StraightAnimation


class AnimationFactory:
    """Factory to create the appropriate animation object based on the config."""

    _registry = {}

    @classmethod
    def register_animation(cls, animation_type, animation_class):
        """Register a new animation class."""
        if not issubclass(animation_class, Animation):
            raise ValueError("animation_class must be a subclass of Animation")
        cls._registry[animation_type] = animation_class

    @classmethod
    def create_animation(cls, text_label, config):
        """Create an animation instance based on the config."""
        animation_type = config['text']['animation'].get('type')
        if not animation_type:
            raise ValueError("Animation type not specified in config.")

        animation_class = cls._registry.get(animation_type)
        if not animation_class:
            raise ValueError(f"Unknown animation type: {animation_type}")

        return animation_class(text_label, config)


# Register animations
AnimationFactory.register_animation('Pow', PowAnimation)
AnimationFactory.register_animation('Angled', AngledAnimation)
AnimationFactory.register_animation('Parabola', ParabolaAnimation)
AnimationFactory.register_animation('Horizontal', HorizontalAnimation)
AnimationFactory.register_animation('Straight', StraightAnimation)
AnimationFactory.register_animation('Static', StaticAnimation)
