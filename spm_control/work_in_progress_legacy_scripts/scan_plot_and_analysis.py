import numpy as np
from matplotlib.figure import Figure
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable


def create_scan_figure(Xs, Ys, intensities, size=(7, 7), vmin=None, vmax=None, log_scale=False):
    Xs = np.asarray(Xs)
    Ys = np.asarray(Ys)
    intensities = np.asarray(intensities)

    if Xs.shape != Ys.shape or Xs.shape != intensities.shape:
        raise ValueError("Xs, Ys, and intensities must have matching shapes.")

    fig = Figure(figsize=size, dpi=100)
    ax = fig.add_subplot(111)

    norm = None
    if log_scale:
        positive = intensities[intensities > 0]
        if positive.size:
            vmin = vmin if vmin is not None else positive.min()
            vmax = vmax if vmax is not None else positive.max()
            if vmax > vmin:
                norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    elif vmin is not None or vmax is not None:
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    heatmap = ax.pcolormesh(Xs, Ys, intensities, cmap="viridis", shading="auto", norm=norm)
    ax.set_aspect("equal")
    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")

    divider = make_axes_locatable(ax)
    colorbar_ax = divider.append_axes("right", size="5%", pad=0.10)
    colorbar = fig.colorbar(heatmap, cax=colorbar_ax)
    colorbar.set_label("Intensity (counts/s)")

    fig.tight_layout()
    return fig
#import diptest

#warnings.filterwarnings('ignore')

def load_scan_data(scan_data_file):
    xs, ys, zs, ch1_ints, ch2_ints, ts = np.loadtxt(
        scan_data_file,
        dtype=float,
        delimiter=",",
        unpack=True
    )

    y_resets = np.where(np.diff(ys) < 0)[0]

    if len(y_resets) > 0:
        len_y = y_resets[0] + 1
    else:
        len_y = len(ys)

    if len(xs) % len_y != 0:
        raise ValueError(
            f"Cannot determine scan shape from {len(xs)} points. "
            f"Detected {len_y} Y positions per row."
        )

    len_x = len(xs) // len_y
    shape = (len_x, len_y)

    Xs = xs.reshape(shape)
    Ys = ys.reshape(shape)
    Ts = ts.reshape(shape)
    CH1_ints = ch1_ints.reshape(shape)
    CH2_ints = ch2_ints.reshape(shape)

    return Xs, Ys, Ts, CH1_ints, CH2_ints

def plot_int_heatmap(Xs, Ys, channel_ints, size=(8, 8), save=False, save_name='scan.png', vmin=None, vmax=None):
    """Plot intensity heatmap of 2D scan."""

    axis_label_size = 26
    axis_tick_size = 22
    cb_label_size = 26
    cb_tick_size = 16
    
    fig, ax = plt.subplots(1, 1, figsize=size)

    plot = ax.pcolor(Xs, Ys, channel_ints, cmap='viridis', shading='auto', vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.10)
    cb = plt.colorbar(plot, cax=cax, orientation='vertical')
    cb.ax.tick_params(labelsize=cb_tick_size)
    cb.set_label(label='Intensity (counts/100ms)', fontsize=cb_label_size)
    
    # ax.autoscale(tight=True)
    ax.set_xlabel('X (µm)', fontsize=axis_label_size)
    ax.set_ylabel('Y (µm)', fontsize=axis_label_size)
    ax.tick_params(axis='both', which='major', labelsize=axis_tick_size)
    # ax.set_title(title, fontsize=26, pad=20)
    plt.tight_layout()

    if save:
        fig.savefig(save_name, dpi=300, bbox_inches="tight")


    return fig, ax, plot

def plot_positions_and_error(Xs,Ys, res, xlim = (0, 100), ylim = (0, 100), ticks = 2):
    # Xs and Ys are Meshgrids; res is float; xlim and ylim are length 2 tuples
    # ticks is an int describing relative number of ticks per resolution unit

    xnodes = np.linspace(xlim[0], xlim[1], int((xlim[1]-xlim[0])/res) + 1).round(decimals=3) # x coordinates [0, distx] (um)
    ynodes = np.linspace(ylim[0], ylim[1], int((ylim[1]-ylim[0])/res) + 1).round(decimals=3)

    Xs_ideal, Ys_ideal = np.meshgrid(xnodes, ynodes, indexing='ij')

    Xs_error = Xs_ideal - Xs
    Ys_error = Ys_ideal - Ys
    total_error = np.sqrt(np.square(Xs_error) + np.square(Ys_error))

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].scatter(Xs, Ys, marker='o')
    ax[0].set_xticks(np.arange(xlim[0], xlim[1] + ticks*res, ticks*res))
    ax[0].set_yticks(np.arange(ylim[0], ylim[1] + ticks*res, ticks*res))
    ax[0].set_xlabel('X (µm)')
    ax[0].set_ylabel('Y (µm)')
    ax[0].grid(True, which='both')
    ax[0].set_title('Piezo Position On Grid (µm)')

    plot = ax[1].pcolor(Xs, Ys, total_error, cmap='Spectral', shading='auto')
    ax[1].set_xlabel('X (µm)')
    ax[1].set_ylabel('Y (µm)')
    ax[1].set_title('Total Positional Error (µm)')
    # ax[1].set_aspect('equal')
    plt.colorbar(plot, ax=ax[1], label=r'$\sqrt{(X_{ideal} - X_{exp})^2 + (Y_{ideal} - Y_{exp})^2}$' + ' (µm)')
    plt.tight_layout()
    plt.show()

    return None

def plot_timespent(Xs, Ys, Ts):
    # Xs, Ys, and ideal positions are all Meshgrids
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    heatmap_time = ax[0].pcolormesh(Xs, Ys, Ts, cmap='coolwarm')
    plt.colorbar(heatmap_time, ax=ax[0])
    ax[0].set_xlabel('x (µm)')
    ax[0].set_ylabel('y (µm)')
    ax[0].set_title('Time Spent at Each Grid Point heatmap')

    ax[1].hist(Ts.flatten(), bins=50)
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Counts')
    ax[1].set_title('Time Spent at Points Distribution')
    plt.tight_layout()
    plt.show()

def pos_error_stats(Xs, Ys, res, xlim, ylim):
    xnodes = np.linspace(xlim[0], xlim[1], int((xlim[1]-xlim[0])/res) + 1).round(decimals=3)
    ynodes = np.linspace(ylim[0], ylim[1], int((ylim[1]-ylim[0])/res) + 1).round(decimals=3)
    print(len(xnodes), len(ynodes))
    Xs_ideal, Ys_ideal = np.meshgrid(xnodes, ynodes, indexing='ij')

    X_err = Xs_ideal - Xs
    Y_err = Ys_ideal - Ys

    combined_errors = np.array([X_err, Y_err]).flatten()

    mean = np.mean(combined_errors)
    stdev = np.std(combined_errors)

    return mean, stdev

def plot_channel_hists(Xs, Ys, Ch1_ints, Ch2_ints, normalize=False):

    fig, ax = plt.subplots(1,2,figsize=(10,5))

    if not normalize:
        ax[0].hist(Ch1_ints.flatten(), bins=50, alpha=0.5,  density=True, label='Ch1')
        ax[0].hist(Ch2_ints.flatten(), bins=50, alpha=0.5,  density=True ,label='Ch2')
        ax[0].set_xlabel('Pixel Intensity (photons/100ms)')
        ax[0].set_title('Absolute Channel Int Hists')
    else:
        norm_ch = lambda x: x/np.max(x)
        norm_ch1 = norm_ch(Ch1_ints)
        norm_ch2 = norm_ch(Ch2_ints)

        ax[0].hist(norm_ch1.flatten(), bins=50, alpha=0.5,  density=True, label='Ch1')
        ax[0].hist(norm_ch2.flatten(), bins=50, alpha=0.5,  density=True ,label='Ch2')
        ax[0].set_xlabel('Normed Pixel Intensity (normed photons/100ms)')
        ax[0].set_title('Norm Channel Int Hists')
    ax[0].legend()
    ax[0].set_ylabel('Counts')

    channel_dif_ints = np.abs(Ch2_ints - Ch1_ints)
    sigma = np.std(channel_dif_ints)
    xbar = np.mean(channel_dif_ints)

    ax[1].hist(channel_dif_ints.flatten(), bins=50, density=True)
    ax[1].text(0.7, 0.8, r"$\sigma =$ {}".format(round(sigma, 2)), transform = ax[1].transAxes)
    ax[1].text(0.7, 0.7, r"$\mu =$ {}".format(round(xbar, 2)), transform = ax[1].transAxes)
    ax[1].set_xlabel(r"Absolute pixel intensity difference $|Ch2-Ch1|$")
    ax[1].set_title('Differential Channel Int Hist: ')
    ax[1].set_ylabel('Counts')

    plt.show()



def hartigans_diptest(data):
    # https://gist.github.com/larsmans/3153330
    # https://stackoverflow.com/questions/38420847/how-to-test-if-a-distribution-is-unimodal-or-not-in-python
    #
    # Hartigan's dip test for unimodality / multimodality.
    # This tests the null hypothesis that the data are unimodal.
    # Parameters
    # ----------
    # data : ndarray
    #     One-dimensional array of data, of length n.
    # Returns
    # -------
    # p : float
    #     The p-value, interpreted as follows:
    #     p > 0.1: data are likely unimodal
    #     p <= 0.1: data are likely multimodal
    # References
    # ----------
    # Hartigan, J. A.; Hartigan, P. M. (1985), "The Dip Test of Unimodality", The Annals of Statistics 13 (1): 70–84, doi:10.1214/aos/1176346577, JSTOR 2240974.
    # Examples
    # --------

    return diptest.diptest(data)
    

def create_live_scan_plot(intensities, xlim, ylim, vmin=None, vmax=None, parent=None, norm="linear"):
    if norm == "log":
        norm_scale = mpl.colors.LogNorm(vmin=max(vmin or 1, 1), vmax=vmax)
    else:
        norm_scale = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    if parent is None:
        figure, axes = plt.subplots(figsize=(10, 7))
        canvas = figure.canvas
    else:
        figure = Figure(figsize=(10, 7), dpi=100)
        axes = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=parent)

    image = axes.imshow(
        intensities.T,
        origin="lower",
        norm=norm_scale,
        extent=(*xlim, *ylim),
        interpolation="none",
        cmap="viridis",
        aspect="equal"
    )

    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    axes.set_xlabel("X (µm)")
    axes.set_ylabel("Y (µm)")

    figure.colorbar(image, ax=axes, label="Intensity")

    canvas.draw()

    if parent is None:
        plt.show(block=False)
    else:
        canvas.get_tk_widget().pack(fill="both", expand=True)

    return figure, axes, image, canvas


def update_live_scan_plot(live_plot, intensities):
    figure, axes, image, canvas = live_plot
    image.set_data(intensities.T)
    canvas.draw_idle()

def create_live_file_plot(file_path, x_nodes, y_nodes, parent, vmin=None, vmax=None, norm="linear"):
    x_nodes = np.asarray(x_nodes)
    y_nodes = np.asarray(y_nodes)
    intensities = np.full((len(x_nodes), len(y_nodes)), np.nan)

    return {
        "file_path": Path(file_path),
        "x_nodes": x_nodes,
        "y_nodes": y_nodes,
        "intensities": intensities,
        "last_position": 0,
        "latest_counts": None,
        "plot": create_live_scan_plot(
            intensities,
            (x_nodes[0], x_nodes[-1]),
            (y_nodes[0], y_nodes[-1]),
            vmin,
            vmax,
            parent,
            norm
        )
    }


def update_live_file_plot(live_scan):
    changed = False

    try:
        with live_scan["file_path"].open("r") as file:
            file.seek(live_scan["last_position"])

            while True:
                line_start = file.tell()
                line = file.readline()

                if not line:
                    break

                if not line.endswith("\n"):
                    file.seek(line_start)
                    break

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                values = line.split(",")

                if len(values) != 6:
                    continue

                x, y, z, ch1, ch2, elapsed = map(float, values)

                i = int(np.argmin(np.abs(live_scan["x_nodes"] - x)))
                j = int(np.argmin(np.abs(live_scan["y_nodes"] - y)))

                live_scan["intensities"][i, j] = ch1 + ch2
                live_scan["latest_counts"] = {
                    "ch1": int(ch1),
                    "ch2": int(ch2),
                    "total": int(ch1 + ch2),
                    "x": x,
                    "y": y,
                    "z": z,
                    "elapsed": elapsed
                }

                changed = True

            live_scan["last_position"] = file.tell()

    except FileNotFoundError:
        return False

    if changed:
        update_live_scan_plot(live_scan["plot"], live_scan["intensities"])

    return changed


def save_live_file_plot(live_scan, save_path):
    live_scan["plot"][0].savefig(save_path, dpi=300, bbox_inches="tight")