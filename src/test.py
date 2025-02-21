trame = "55:00:0A:07:01:EB:A5:03:0C:30:0E:01:A4:D9:C7:00:01:FF:FF:FF:FF:34:00:8C"


trame = bytes.fromhex(trame.replace(":", ""))

from EnOceanSerialReader import EnOceanSerialReader

reader = EnOceanSerialReader("", 0)

print(reader.process_frame(trame))