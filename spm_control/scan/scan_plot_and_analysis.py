import numpy as np
from copy import copy
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.colors import Normalize


def create_live_raster_plot(xlim, ylim, shape, vmin=None, vmax=None, channel=0):
    fig = Figure(dpi=100)
    ax = fig.add_subplot(111)

    cmap = copy(cm.viridis)
    cmap.set_bad(color="#303030")

    initial_data = np.ma.masked_invalid(
        np.full(shape, np.nan)
    )

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
    ax.set_title(
        "Combined Channels" if channel == 0 else f"Channel {channel}"
    )

    fig.colorbar(image, ax=ax, label="Intensity (counts/s)")
    fig.tight_layout()

    return fig, image


def update_live_raster_plot(fig, image, intensities):
    displayed = np.ma.masked_invalid(
        np.asarray(intensities)
    )

    image.set_data(displayed.T)
    fig.canvas.draw_idle()