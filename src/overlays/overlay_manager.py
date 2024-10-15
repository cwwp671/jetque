# jetque/src/overlays/overlay_manager.py

import logging
from src.overlays.configure_overlay import ConfigureOverlay
from src.overlays.active_overlay import ActiveOverlay

class OverlayManager:
    def __init__(self):
        self.overlays = {}  # Store all overlays here (name -> overlay object)

    def create_overlay(self, name, overlay_data):
        """Create an overlay in configure mode"""
        configure_overlay = ConfigureOverlay(name, overlay_data)
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
        logging.debug("After current_overlay assignment")
        overlay_data = current_overlay.overlay_data
        logging.debug("after overlay_data assignment")

        if isinstance(current_overlay, ConfigureOverlay):
            logging.debug("in the if isinstance")
            # Hide and schedule for deletion
            current_overlay.hide()
            current_overlay.deleteLater()
            logging.debug("scheduled current_overlay for deletion")
            # Create active overlay
            active_overlay = ActiveOverlay(name, overlay_data)
            logging.debug("active_overlay declaration")
            self.overlays[name] = active_overlay
            logging.debug("name assigned")
            active_overlay.show()
            logging.debug("showing active overlay")
        elif isinstance(current_overlay, ActiveOverlay):
            logging.debug("in elif isinstance")
            # Hide and schedule for deletion
            current_overlay.hide()
            current_overlay.deleteLater()
            logging.debug("scheduled current_overlay for deletion")
            # Recreate configure overlay
            configure_overlay = ConfigureOverlay(name, overlay_data)
            logging.debug("configure_overlay declaration")
            self.overlays[name] = configure_overlay
            logging.debug("name assigned")
            configure_overlay.show()
            logging.debug("showing configuration overlay")

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
        """Save the current state of overlays to a file"""
        logging.debug("Save overlay data requested")
        # Implement JSON save logic here
        pass
