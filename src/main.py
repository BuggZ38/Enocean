# coding: UTF-8
"""
Script: EnoceanTest/main
Création: bstauss, le 24/01/2025
"""

# Imports

import struct
import time
from EnOceanSerialReader import EnOceanSerialReader
from enocean.protocol.packet import RadioPacket

from enocean.communicators.serialcommunicator import SerialCommunicator

# Fonctions

# Programme principal
def main():
    reader = EnOceanSerialReader("COM11", 57600)

    reader.connect()

    # reader = SerialCommunicator(port="COM11")
    #
    # reader.start()

    try:
        destination = [0x05, 0x13, 0x6A, 0x3E]
        senderID = [0x01, 0x93, 0x3E, 0x3F]

        # packet_on = RadioPacket.create(
        #     rorg=0xD2, rorg_func=0x01, rorg_type=0x0B,
        #     command=1,  # Actuator Set Output
        #     data=[0x00, 0x00, 0x00, 0x00,
        #           0x01, # CMD
        #           0x00, # DV
        #           0x1F, # IO
        #           0, # OV
        #           0x00], # padding
        #     destination=destination,
        #     sender=senderID
        # )

        packet_on = RadioPacket.create(
            rorg=0xD2, rorg_func=0x01, rorg_type=0x0B,
            command=1,  # Actuator Set Output
            data=[0x01,  # CMD
                  0x00,  # DV
                  0x1F,  # IO
                  0],  # OV
            destination=destination,
            sender=senderID
        )

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

        print(packet_on)

        if reader.send_data(packet_on):  # Envoi de la trame
            print("Trame envoyée !")

        # while True:
        #     time.sleep(1)  # Évite une surcharge CPU
    finally:
        reader.disconnect()
        # reader.stop()

    # reader.disconnect()


if __name__ == '__main__':
    main()
# Fin
