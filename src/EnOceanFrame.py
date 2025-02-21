import utils
from constant import PACKET
from EnOceanDevice import EnOceanDevice

class EnOceanFrame:
    raw_data: bytes
    data_lenght: int
    opt_lenght: int
    type_packet: int
    crc_header: int
    data: bytes
    data_opt: bytes
    crc_data: int
    decoded_data: dict

    idDiscover = []

    def __init__(self):
        self.device = EnOceanDevice()

    def __str__(self):
        return  ""


    def decode(self) -> dict[str, str] | None:
        try:
            if self.raw_data[0] != 0x55:
                print("Trame invalide")
                return

            packetConst = PACKET

            self.data_lenght = (self.raw_data[1] << 8) | self.raw_data[2]
            self.opt_lenght = self.raw_data[3]
            self.type_packet = self.raw_data[4]
            self.crc_header = self.raw_data[5]

            dataStart = 6
            dataEnd = dataStart + self.data_lenght
            self.data = self.raw_data[dataStart:dataEnd]
            self.decoded_data = utils.dataDecode(self.data)

            optStart = dataEnd
            optEnd = optStart + self.opt_lenght
            self.data_opt = self.raw_data[optStart:optEnd] if self.opt_lenght > 0 else b""
            data_optDecode = utils.optionalDataDecode(self.data_opt)

            self.crc_data = self.raw_data[len(self.raw_data) - 1]

            dataUtils = {}

            self.device.sender_id = self.decoded_data['senderID']

            if self.validate_crc() and self.device.check_device():
                dataUtils = {'senderID': f'{self.decoded_data['senderID']}', 'data': f'{utils.to_hex_string(self.decoded_data['data'])}'}
            return dataUtils

        except IndexError:
            raise ValueError("Trame trop courte ou mal formée.")
        except Exception as e:
            raise ValueError(f"Erreur dans le décodage : {e}")

    def validate_crc(self) -> bool:
        if utils.calcCRC(self.data + self.data_opt) == self.crc_data:
            return True
        return False
