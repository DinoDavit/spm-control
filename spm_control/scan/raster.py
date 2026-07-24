import time
import numpy as np

import spm_control.config as config


def run_raster_scan(stage, detector, stop_event, output_path):
    scan = config.load_named_settings("scan", config.SCAN_CONFIG)
    motion = config.load_named_settings("piezo_scan_motion", config.HARDWARE_CONFIG)

    x_min, x_max = scan["x_min"], scan["x_max"]
    y_min, y_max = scan["y_min"], scan["y_max"]
    z_focus, resolution = scan["z_focus"], scan["resolution"]

    major_delay = motion["major_axis_delay"]
    minor_delay = motion["minor_axis_delay"]
    settle_time = motion["settle_time"]

    x_nodes = np.linspace(x_min, x_max, int((x_max - x_min) / resolution) + 1).round(3)
    y_nodes = np.linspace(y_min, y_max, int((y_max - y_min) / resolution) + 1).round(3)

    intensities = np.zeros((len(x_nodes), len(y_nodes)))
    split_intensities = np.zeros((2, len(x_nodes), len(y_nodes)))

    start_position = {"1": x_min, "2": y_min, "3": z_focus}
    stage.move(start_position)
    time.sleep(settle_time)

    completed_points = 0
    scan_start = time.time()
    stopped = False

    with open(output_path, "w", buffering=1) as scan_file:
        for i, x in enumerate(x_nodes):
            for j, y in enumerate(y_nodes):
                if stop_event.is_set():
                    stopped = True
                    break

                point_start = time.time()
                stage.move({"1": float(x), "2": float(y)})
                time.sleep(major_delay if j == 0 else minor_delay)

                real_position = stage.position()
                counts = detector.poll_counts()

                if len(counts) < 2:
                    raise RuntimeError(f"Expected two detector channels, received: {counts}")

                ch1, ch2 = int(counts[0]), int(counts[1])
                total = ch1 + ch2
                elapsed = time.time() - scan_start

                split_intensities[0, i, j] = ch1
                split_intensities[1, i, j] = ch2
                intensities[i, j] = total

                scan_file.write(
                    f"{real_position['1']},{real_position['2']},{real_position['3']},"
                    f"{ch1},{ch2},{elapsed}\n"
                )
                scan_file.flush()

                completed_points += 1
                print(
                    f"Point {completed_points}: "
                    f"x={real_position['1']}, y={real_position['2']}, "
                    f"ch1={ch1}, ch2={ch2}, time={time.time() - point_start:.3f}s"
                )

            if stopped:
                break

    stage.move(start_position)

    return {
        "stopped": stopped,
        "completed_points": completed_points,
        "output_path": output_path,
        "intensities": intensities,
        "split_intensities": split_intensities,
        "x_nodes": x_nodes,
        "y_nodes": y_nodes
    }