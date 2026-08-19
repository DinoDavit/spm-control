from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
import time


class ML_Page:
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
        }

        self.panels = app.panels
        page_helpers.reload_panels(self.panels, MAIN_LAYOUT, required_panels, notMain=True)
        time.sleep(0.05)
        page_helpers.load_required_panels(self, self.panels, required_panels)
        
        # Future integration will probably consist of:
        # Autofocus where user will center on a 'bright' region and then piezo will move in z direction
        # Could be an optimizing algorithm on a 'intensity' vs 'z-positoin' graph
        