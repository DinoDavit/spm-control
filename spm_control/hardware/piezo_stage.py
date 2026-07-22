from pipython import GCSDevice, pitools

from spm_control.hardware.interfaces import StageInterface


class PIStage(StageInterface):
    def __init__(
        self,
        controller_name: str,
        serial_number: str,
        stage_models: list[str],
        autozero: bool = False
    ):
        self.controller_name = controller_name
        self.serial_number = serial_number
        self.stage_models = stage_models
        self.autozero = autozero
        self.device = None

    def connect(self) -> None:
        if self.device is not None:
            return
        
        # Initializing device if not initilized already
        self.device = GCSDevice(self.controller_name)

        try:
            self.device.ConnectUSB(serialnum=self.serial_number)
            # Connecting to device


            pitools.startup(
                self.device,
                stages=self.stage_models,
                refmodes=None
            )
            # Starting the piezo stages 

            if self.autozero:
                self.device.ATZ()
                pitools.waitonautozero(self.device)
            # Autozeroing potentially 

        except Exception:
            self.close()
            raise

    def move(self, position: dict[str, float]) -> None:
        self._require_connection()
        self.device.MOV(position)

    def position(self) -> dict[str, float]:
        self._require_connection()
        return self.device.qPOS()

    def close(self) -> None:
        if self.device is not None:
            self.device.CloseConnection()
            self.device = None

    def _require_connection(self) -> None:
        if self.device is None:
            raise RuntimeError("PI stage is not connected.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()