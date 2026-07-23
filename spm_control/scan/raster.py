import time
import numpy as np

from spm_control.gui.modes import config


def run_raster_scan(stage, detector, stop_event):
    scan = config.load_named_settings("scan", config.SCAN_CONFIG)
    motion = config.load_named_settings("piezo_scan_motion", config.HARDWARE_CONFIG)

    x_min, x_max = scan["x_min"], scan["x_max"]
    y_min, y_max = scan["y_min"], scan["y_max"]
    z_focus = scan["z_focus"]
    resolution = scan["resolution"]

    major_delay = motion["major_axis_delay"]
    minor_delay = motion["minor_axis_delay"]
    settle_time = motion["settle_time"]

    x_nodes = np.linspace(x_min, x_max, int((x_max - x_min) / resolution) + 1).round(3)
    y_nodes = np.linspace(y_min, y_max, int((y_max - y_min) / resolution) + 1).round(3)

    x_grid, y_grid = np.meshgrid(x_nodes, y_nodes, indexing="ij")
    intensities = np.zeros((len(x_nodes), len(y_nodes)))
    split_intensities = np.zeros((2, len(x_nodes), len(y_nodes)))

    print("Moving to starting position...")
    stage.move({"1": x_min, "2": y_min, "3": z_focus})
    time.sleep(settle_time)

    completed_points = 0

    for i, x_position in enumerate(x_nodes):
        for j, y_position in enumerate(y_nodes):
            # Safe stopping point: before beginning another complete measurement.
            if stop_event.is_set():
                return {
                    "stopped": True,
                    "x_grid": x_grid,
                    "y_grid": y_grid,
                    "intensities": intensities,
                    "split_intensities": split_intensities,
                    "completed_points": completed_points
                }

            point_start = time.time()

            stage.move({"1": float(x_position), "2": float(y_position)})
            time.sleep(major_delay if j == 0 else minor_delay)

            real_position = stage.position()
            counts = detector.poll_counts()

            if len(counts) < 2:
                raise RuntimeError(f"HydraHarp returned fewer than two channels: {counts}")

            split_intensities[0, i, j] = counts[0]
            split_intensities[1, i, j] = counts[1]
            intensities[i, j] = np.sum(counts)
            completed_points += 1

            print(
                f"Position: ({real_position['1']:.3f}, {real_position['2']:.3f}, "
                f"{real_position['3']:.3f}); counts: {counts}; "
                f"time: {time.time() - point_start:.3f}s"
            )

    print("Returning to starting position...")
    stage.move({"1": x_min, "2": y_min, "3": z_focus})

    return {
        "stopped": False,
        "x_grid": x_grid,
        "y_grid": y_grid,
        "intensities": intensities,
        "split_intensities": split_intensities,
        "completed_points": completed_points
    }