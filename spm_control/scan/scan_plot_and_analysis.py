import numpy as np
from copy import copy
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.colors import Normalize


def create_live_raster_plot(xlim, ylim, shape, vmin=None, vmax=None):
    fig = Figure(dpi=100)
    ax = fig.add_subplot(111)

    cmap = copy(cm.viridis)
    cmap.set_bad(color="#303030")

    initial_data = np.ma.masked_invalid(np.full(shape, np.nan))

    image = ax.imshow(
        initial_data.T,
        origin="lower",
        extent=(*xlim, *ylim),
        cmap=cmap,
        norm=Normalize(vmin=vmin, vmax=vmax),
        interpolation="none",
        aspect="equal"
    )

    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")
    ax.set_title("Combined Channels")

    colorbar = fig.colorbar(image, ax=ax, label="Intensity (counts/s)")
    fig.tight_layout()

    return fig, image, colorbar

def update_live_raster_plot(fig, image, colorbar, intensities):
    displayed = np.asarray(intensities, dtype=float)
    image.set_data(displayed.T)

    valid = displayed[np.isfinite(displayed)]

    if valid.size:
        new_min = float(valid.min())
        new_max = float(valid.max())

        if new_min == new_max:
            new_min = 0
            new_max = max(new_max, 1)

        image.set_clim(new_min, new_max)
        colorbar.update_normal(image)

    fig.canvas.draw_idle()

def save_raster_plot(intensities, x_nodes, y_nodes, output_path, title):
    fig = Figure(figsize=(7, 7), dpi=100)
    ax = fig.add_subplot(111)

    valid = intensities[np.isfinite(intensities)]
    vmax = max(float(valid.max()), 1) if valid.size else 1

    image = ax.imshow(
        intensities.T,
        origin="lower",
        extent=(x_nodes[0], x_nodes[-1], y_nodes[0], y_nodes[-1]),
        vmin=0,
        vmax=vmax,
        interpolation="none",
        aspect="equal"
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(title)

    fig.colorbar(image, ax=ax, label="Intensity")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")