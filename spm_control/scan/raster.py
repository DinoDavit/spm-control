import time

import numpy as np

import spm_control.config as config


def run_raster_scan(stop_event):
    scan_settings = config.load_named_settings(
        "scan",
        config.SCAN_CONFIG
    )

    x_min = scan_settings["x_min"]
    x_max = scan_settings["x_max"]
    y_min = scan_settings["y_min"]
    y_max = scan_settings["y_max"]
    z_focus = scan_settings["z_focus"]
    resolution = scan_settings["resolution"]

    x_nodes = np.linspace(x_min, x_max, int((x_max - x_min) / resolution) +1).round(3)

    y_nodes = np.linspace(y_min, y_max, int((y_max - y_min) / resolution)+1).round(3)

    x_grid, y_grid = np.meshgrid(x_nodes, y_nodes, indexing="ij")

    intensities = np.zeros((len(x_nodes), len(y_nodes)))
    channel_intensities = np.zeros((2, len(x_nodes), len(y_nodes)))

    for i, x_position in enumerate(x_nodes):
        for j, y_position in enumerate(y_nodes):
            if stop_event.is_set():
                return {
                    "stopped": True,
                    "x_grid": x_grid,
                    "y_grid": y_grid,
                    "intensities": intensities,
                    "channel_intensities": channel_intensities
                }

            print(
                f"Would scan point "
                f"({x_position}, {y_position}, {z_focus})"
            )

            time.sleep(0.1)

    return {
        "stopped": False,
        "x_grid": x_grid,
        "y_grid": y_grid,
        "intensities": intensities,
        "channel_intensities": channel_intensities
    }