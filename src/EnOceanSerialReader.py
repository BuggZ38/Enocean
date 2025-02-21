import threading
import datetime
import utils
from serial import Serial, SerialException
from enocean.communicators.communicator import Communicator

from EnOceanFrame import EnOceanFrame
from ApiSender import ApiSender


class EnOceanSerialReader:

    def __str__(self):
        return f"EnOceanDevice(port: str='{self.port}', baudrate: int={self.baudrate})"

    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        self.buffer = b""
        self.serial_connection = None
        self.reading = False  # Flag pour contrôler la lecture
        self.thread = None

        self.frame = EnOceanFrame()
        self.api = ApiSender()
        self.communicator = Communicator()

    def connect(self):
        """Ouvre le port série et démarre la lecture en arrière-plan."""
        try:
            self.serial_connection = Serial(self.port, self.baudrate, timeout=0.1)
            self.reading = True
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            print(f"Connecté au port {self.port} avec baudrate {self.baudrate}")
        except SerialException as e:
            print(f"Erreur de connexion : {e}")

    def _read_loop(self):
        """Boucle de lecture du port série exécutée dans un thread."""
        try:
            while self.reading:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.read(self.serial_connection.in_waiting)
                    self.buffer += data

                    trames, self.buffer = utils.extract_trames(self.buffer)
                    for trame in trames:
                        print("\n", datetime.datetime.now(), end="\t")
                        print(self.process_frame(trame))
        except SerialException as e:
            print(f"Erreur de lecture : {e}")

    def read_data(self):
        """Lecture manuelle des données (optionnel, si besoin d'une lecture ponctuelle)."""
        if self.serial_connection and self.serial_connection.in_waiting > 0:
            data = self.serial_connection.read(self.serial_connection.in_waiting)
            self.buffer += data
            trames, self.buffer = utils.extract_trames(self.buffer)
            for trame in trames:
                self.process_frame(trame)

    def send_data(self, packet):
        return self.communicator.send(packet)

    def process_frame(self, trame: bytes):
        """Traite une trame reçue."""
        self.frame.raw_data = trame
        return self.frame.decode()

    def disconnect(self):
        """Arrête la lecture et ferme le port série."""
        self.reading = False
        if self.thread:
            self.thread.join()  # Attendre la fin du thread
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        print("Déconnecté du port série.")

