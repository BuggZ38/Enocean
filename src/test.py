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
        destination = [0xFF, 0xFF, 0xFF, 0xFF]
        senderID = [0x00, 0x00, 0x00, 0x00]

        packet_on = RadioPacket.create(
            rorg=0xF6,
            rorg_func=0x02,    # dépend de l'EEP (ex : F6-02-01 = Push Button)
            rorg_type=0x01,
            EB=0,              # Example of data bits for button state
            R1=1,              # Suppose button R1 is pressed
            SA=0,              # Optional
            CMD=0              # Optional command field
        )

        #
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
