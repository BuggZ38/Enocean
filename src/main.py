# coding: UTF-8
"""
Script: EnoceanTest/main
Création: bstauss, le 24/01/2025
"""

# Imports

import time
from EnOceanSerialReader import EnOceanSerialReader
from enocean.protocol.packet import RadioPacket

from enocean.communicators.serialcommunicator import SerialCommunicator

from constant import ID_Manager

# Fonctions

# Programme principal
def main():
    base_url = "http://172.16.25.22:57400/api"

    IDs_manager = ID_Manager(base_url)

    reader = EnOceanSerialReader("COM11", 57600, IDs_manager, base_url)

    reader.connect()

    # reader = SerialCommunicator(port="COM11")
    #
    # reader.start()

    try:
        destination = [0x05, 0x13, 0x6A, 0x3E]
        senderID = [0x01, 0x93, 0x3E, 0x3F]

        # packet_on = RadioPacket.create(
        #     rorg=0xD2, rorg_func=0x01, rorg_type=0x0A,
        #     command=1,  # Actuator Set Output
        #     data=[0x04,
        #           0x60,
        #           0x80], # padding
        #     destination=destination,
        #     sender=senderID
        # )

        # packet_on = RadioPacket.create(
        #     rorg=0xD2, rorg_func=0x01, rorg_type=0x0B,
        #     command=1,  # Actuator Set Output
        #     data=[0x01,  # CMD
        #           0x00,  # DV
        #           0x1F,  # IO
        #           0],  # OV
        #     destination=destination,
        #     sender=senderID
        # )

        # packet_off = RadioPacket.create(
        #     rorg=0xD2, rorg_func=0x01, rorg_type=0x01,
        #     command=1,
        #     data=[0x00, 0x00, 0x00, 0x00,  # Remplissage
        #           0x01,  # CMD = 1 (Set Output)
        #           0x00,  # DV = 0
        #           0x00,  # IO = 0
        #           0x00,  # OV = 0% (OFF)
        #           0x00],  # Padding
        #     destination=destination
        # )

        # print(packet_on)
        #
        # if reader.send(packet_on):  # Envoi de la trame
        #     print("Trame envoyée !")

        while True:
            time.sleep(1)  # Évite une surcharge CPU
    finally:
        reader.disconnect()
        # reader.stop()

    # reader.disconnect()


if __name__ == '__main__':
    main()
# Fin
