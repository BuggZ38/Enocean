from constant import KNOWN_ID

class EnOceanDevice:
    sender_id: str
    knowing_device: bool

    def __str__(self):
        return f"EnOceanDevice(sender_id='{self.sender_id}', knowing_device={self.check_device()})"

    def check_device(self) -> bool:
        self.knowing_device = False
        if self.sender_id in KNOWN_ID:
            self.knowing_device = True
        return self.knowing_device
