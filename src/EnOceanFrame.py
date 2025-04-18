import utils
from constant import PACKET
from EnOceanDevice import EnOceanDevice
from src.constant import KNOWN_ID
from src.constant import ID_Manager

import time


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

    def __init__(self, id_mana: ID_Manager):
        self.device = id_mana

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

            sender_id = self.decoded_data['senderID']

            if self.validate_crc() and self.device.check_ID(sender_id):
                dataUtils = {'sender_id': int(self.device.get_ID_by_IP(sender_id)[0]), 'data': f'{utils.to_hex_string(self.decoded_data['data'])}', 'timestamp': f'{time.time()}'}

            elif self.validate_crc() and not self.device.check_ID(sender_id):
                data = self.decoded_data['data']

                if utils.to_hex_string(data) == "18:08:0D:80" and self.decoded_data['profile'] == "BS4":
                    self.device.add(sender_id)
                    message = "Device Added"
                else:
                    message = "Unknow device"

                if self.decoded_data['profile'] in ["BS1", "RPS", "VLD"]:
                    self.device.add(sender_id)
                    message = "Device Added"

                dataUtils = {'info': message, 'profile': f"{self.decoded_data['profile']}"}
            else:
                dataUtils = {'info': 'Wrong Data'}


            return dataUtils

        except IndexError:
            raise ValueError("Trame trop courte ou mal formée.")
        except Exception as e:
            raise ValueError(f"Erreur dans le décodage : {e}")

    def validate_crc(self) -> bool:
        if utils.calcCRC(self.data + self.data_opt) == self.crc_data:
            return True
        return False
