from spm_control.work_in_progress_legacy_scripts.hydraharp_intensities import HH400_Histo_Manager


class HydraHarpDetector:
    def __init__(self, hydraharp_settings, sync_settings):
        self.hydraharp_settings = hydraharp_settings
        self.sync_settings = sync_settings
        self.manager = None

    def connect(self):
        if self.manager is not None:
            return

        mode_name = self.hydraharp_settings.get("default_mode", "hist").lower()
        mode_map = {"hist": 0, "t2": 2, "t3": 3}

        if mode_name not in mode_map:
            raise ValueError(f"Unsupported HydraHarp mode: {mode_name}")

        self.manager = HH400_Histo_Manager(mode=mode_map[mode_name], send_error_email=False)

        self.manager.binning = self.sync_settings["binning"]
        self.manager.syncDivider = self.sync_settings["syncDivider"]
        self.manager.syncCFDLevel = self.sync_settings["syncCFDLevel"]
        self.manager.syncCFDZeroCross = self.sync_settings["syncCFDZeroCross"]
        self.manager.syncChannelOffset = self.sync_settings["syncChannelOffset"]
        self.manager.inputCFDLevel = self.sync_settings["inputCFDLevel"]
        self.manager.inputCFDZeroCross = self.sync_settings["inputCFDZeroCross"]
        self.manager.inputChannelOffset = self.sync_settings["inputChannelOffset"]

        try:
            self.manager.connect_device()
            self.manager.prep_measurements()
        except Exception:
            self.close()
            raise

    def poll_counts(self):
        self._require_connection()
        return self.manager.poll_intensity()

    def integrate_counts(self, acquisition_ms):
        self._require_connection()
        return self.manager.integrate_intensity(tacq=int(acquisition_ms))

    def close(self):
        if self.manager is not None:
            self.manager.closeDevices()
            self.manager = None

    def _require_connection(self):
        if self.manager is None:
            raise RuntimeError("HydraHarp is not connected.")