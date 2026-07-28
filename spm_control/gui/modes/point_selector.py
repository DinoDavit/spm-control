class PointSelector:
    def __init__(self, canvas, axes, callback=None):
        self.canvas = canvas
        self.axes = axes
        self.callback = callback

        self.connection_id = None
        self.marker = None
        self.selected_point = None

    def enable(self):
        if self.connection_id is None:
            self.connection_id = self.canvas.mpl_connect(
                "button_press_event",
                self._on_click
            )

        self.canvas.get_tk_widget().configure(cursor="crosshair")

    def disable(self):
        if self.connection_id is not None:
            self.canvas.mpl_disconnect(self.connection_id)
            self.connection_id = None

        self.canvas.get_tk_widget().configure(cursor="")

    def clear(self):
        self.selected_point = None

        if self.marker is not None:
            self.marker.remove()
            self.marker = None
            self.canvas.draw_idle()

    def _on_click(self, event):
        if event.inaxes is not self.axes:
            return

        if event.xdata is None or event.ydata is None:
            return

        x = float(event.xdata)
        y = float(event.ydata)
        self.selected_point = (x, y)

        if self.marker is not None:
            self.marker.remove()

        self.marker, = self.axes.plot(
            x,
            y,
            marker="o",
            markersize=8,
            markerfacecolor="none",
            markeredgewidth=2
        )

        self.canvas.draw_idle()

        if self.callback:
            self.callback(self.selected_point)

        self.disable()