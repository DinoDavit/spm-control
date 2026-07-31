from pathlib import Path
import csv
import subprocess

import numpy as np


T2_TIME_MASK = 0x1FFFFFF
T2_CHANNEL_MASK = 0x3F
T2_OVERFLOW_CHANNEL = 0x3F
T2_WRAPAROUND = 0x2000000


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def windows_to_cygwin_path(path: str | Path, cygwin_bash: str | Path) -> str:
    result = subprocess.run(
        [
            str(cygwin_bash),
            "-lc",
            f"cygpath -u {shell_quote(str(Path(path).resolve()))}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def decode_t2_to_csv(
    input_file: str | Path,
    output_file: str | Path,
    resolution_ps: float = 1.0,
) -> Path:
    input_file = Path(input_file)
    output_file = Path(output_file)

    overflow_correction = 0

    with input_file.open("rb") as binary_file, output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        while True:
            records = np.fromfile(
                binary_file,
                dtype="<u4",
                count=1_000_000
            )

            if records.size == 0:
                break

            for record in records:
                record = int(record)

                special = (record >> 31) & 0x1
                channel = (record >> 25) & T2_CHANNEL_MASK
                timetag = record & T2_TIME_MASK

                if special:
                    if channel == T2_OVERFLOW_CHANNEL:
                        overflow_count = timetag if timetag > 0 else 1
                        overflow_correction += overflow_count * T2_WRAPAROUND

                    continue

                absolute_ticks = overflow_correction + timetag
                arrival_time_ps = absolute_ticks * resolution_ps

                writer.writerow((channel, arrival_time_ps))

    return output_file


def run_t2_correlation(
    input_file: str | Path,
    output_file: str | Path,
    delay_min_ps: int,
    bin_width_ps: int,
    delay_max_ps: int,
    cygwin_bash: str | Path,
    photon_gn: str,
) -> subprocess.CompletedProcess:
    input_cygwin = windows_to_cygwin_path(input_file, cygwin_bash)
    output_cygwin = windows_to_cygwin_path(output_file, cygwin_bash)

    command = (
        f"cat {shell_quote(input_cygwin)} | "
        f"{shell_quote(photon_gn)} "
        f"--mode t2 "
        f"--channels 2 "
        f"--order 2 "
        f"--time {int(delay_min_ps)},{int(bin_width_ps)},{int(delay_max_ps)} "
        f"--file-out {shell_quote(output_cygwin)}"
    )

    return subprocess.run(
        [str(cygwin_bash), "-lc", command],
        capture_output=True,
        text=True,
        check=True,
    )