import logging
from src.overlays.configure_overlay import ConfigureOverlay
from src.overlays.active_overlay import ActiveOverlay
from config.config_loader import load_config, save_config


class OverlayManager:
    def __init__(self):
        self.overlays = {}  # Store all overlays here (name -> overlay object)

    def create_overlay(self, name, overlay_data):
        """Create an overlay in configure mode"""
        configure_overlay = ConfigureOverlay(name, overlay_data, self)
        self.overlays[name] = configure_overlay
        configure_overlay.show()

    def delete_overlay(self, name):
        """Delete an overlay"""
        if name in self.overlays:
            self.overlays[name].close()
            del self.overlays[name]
        else:
            logging.debug(f"Overlay '{name}' does not exist!")

    def toggle_mode(self, name):
        logging.debug("Mode Toggle Requested")
        if name not in self.overlays:
            logging.debug(f"Overlay '{name}' does not exist!")
            return

        current_overlay = self.overlays[name]
        overlay_data = current_overlay.overlay_data

        if isinstance(current_overlay, ConfigureOverlay):
            # Hide and schedule for deletion
            current_overlay.hide()
            current_overlay.deleteLater()
            # Create active overlay
            active_overlay = ActiveOverlay(name, overlay_data, self)
            self.overlays[name] = active_overlay
            active_overlay.show()
        elif isinstance(current_overlay, ActiveOverlay):
            # Hide and schedule for deletion
            current_overlay.hide()
            current_overlay.deleteLater()
            # Recreate configure overlay
            configure_overlay = ConfigureOverlay(name, overlay_data, self)
            self.overlays[name] = configure_overlay
            configure_overlay.show()

    def display_event(self, overlay_name, event):
        if overlay_name in self.overlays:
            overlay = self.overlays[overlay_name]
            if isinstance(overlay, ActiveOverlay):
                overlay.display_event(event)
            else:
                logging.debug(f"Overlay '{overlay_name}' is not in active mode.")
        else:
            logging.warning(f"Overlay '{overlay_name}' does not exist.")

    def save_overlay_data(self):
        """Save the current state of all overlays to the config file."""
        logging.debug("Saving overlay data")
        updated_overlays = {}

        for name, overlay in self.overlays.items():
            updated_overlays[name] = overlay.overlay_data

        # Load the current config and update the overlays section
        config_data = load_config()
        config_data['overlays'] = updated_overlays
        save_config(config_data)
