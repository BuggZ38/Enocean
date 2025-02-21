from constant import *

def calcCRC(msg):
    checksum = 0
    for byte in msg:
        checksum = CRC_TABLE[checksum & 0xFF ^ byte & 0xFF]
    return checksum


def extract_trames(buffer):
    """
    Recherche des trames complètes dans le buffer.
    """
    trames = []
    i = 0
    while i < len(buffer):
        # Vérifier la présence de l'octet de synchronisation
        if buffer[i] == 0x55:
            # Assurer qu'il y a assez d'octets pour lire la longueur
            if i + 6 > len(buffer):
                break  # Attendre plus de données

            # Lire la longueur des données et des options
            data_length = (buffer[i + 1] << 8) | buffer[i + 2]
            opt_length = buffer[i + 3]
            total_length = 6 + data_length + opt_length + 1

            # Vérifier si la trame complète est dans le buffer
            if i + total_length > len(buffer):
                break  # Attendre plus de données

            # Extraire la trame complète
            trame = buffer[i:i + total_length]
            trames.append(trame)
            i += total_length  # Avancer après la trame
        else:
            i += 1  # Avancer si l'octet n'est pas 0x55

    # Conserver les fragments restants dans le buffer
    buffer = buffer[i:]
    return trames, buffer


def optionalDataDecode(data):
    subTelNum = data[0]
    destID = '.'.join(f"{int(item)}" for item in data[1:5])
    dbm = data[5]
    securtyLVL = data[6]
    return {"subTelNum": subTelNum, "destID": destID, "dbm": dbm, "securtyLVL": f"0x{securtyLVL:02X}"}


def dataDecode(data):
    eep = data[0]
    r_org = RORG(eep)._name_ if eep in RORG else ""
    if r_org == "":
        print("Aucun profile trouver")
        return

    if r_org == "RPS" or r_org == "BS1":
        senderID = '.'.join(f"{int(item)}" for item in data[2:6])
        status = data[len(data) - 1]
        data = data[1]
        return  {'profile': r_org, 'data': data, 'senderID': senderID, 'status': status}

    if r_org == "BS4":
        senderID = '.'.join(f"{int(item)}" for item in data[5:9])
        status = data[len(data) - 1]
        data = data[1:5]
        return {'profile': r_org, 'data': data, 'senderID': senderID, 'status': status}

    if r_org == "VLD":
        senderID = '.'.join(f"{int(item)}" for item in data[len(data) - 5:len(data) - 1])
        status = data[len(data) - 1]
        data = data[1:len(data) - 5]
        print({'profile': r_org, 'data': data, 'senderID': senderID, 'status': status})
        return {'profile': r_org, 'data': data, 'senderID': senderID, 'status': status}


def combine_hex(data):
    ''' Combine list of integer values to one big integer '''
    output = 0x00
    for i, value in enumerate(reversed(data)):
        output |= (value << i * 8)
    return output


def to_hex_string(data):
    ''' Convert list of integers to a hex string, separated by ":" '''
    if isinstance(data, int):
        return '%02X' % data
    return ':'.join([('%02X' % o) for o in data])


def from_hex_string(hex_string):
    reval = [int(x, 16) for x in hex_string.split(':')]
    if len(reval) == 1:
        return reval[0]
    return reval
