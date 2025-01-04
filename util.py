import string
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

# mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

# if comply to vehicle format
def license_complies_format_vehicle(text):
    if len(text) != 7:
        return False

    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[4] in dict_char_to_int.keys()) and \
       (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[5] in dict_char_to_int.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()):
        return True
    
    else:
        return False

# if comply to motor type 1 format
def license_complies_format_motor1(text):
    if len(text) != 6:
        return False
    
    if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[0] in dict_char_to_int.keys()) and \
       (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[1] in dict_char_to_int.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in string.ascii_uppercase or text[3] in dict_int_to_char.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()):
        return True
    
    else:
        return False

# if comply to motor type 2 format
def license_complies_format_motor2(text):
    if len(text) != 6:
        return False
    
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[1] in dict_char_to_int.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()):
        return True
    
    else:
        return False

# format license properly for vehicle
def format_license_vehicle(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_int_to_char, 
               3: dict_char_to_int, 4:dict_char_to_int, 5: dict_char_to_int, 6:dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

# format license properly for motor type 1
def format_license_motor1(text):
    license_plate_ = ''
    mapping = {0: dict_char_to_int, 1: dict_char_to_int, 2: dict_char_to_int, 
               3: dict_int_to_char, 4:dict_int_to_char, 5: dict_int_to_char}
    for j in [0, 1, 2, 3, 4, 5]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

# format license properly for motor type 2
def format_license_motor2(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 
               1: dict_char_to_int, 2: dict_char_to_int, 3: dict_char_to_int,
               4:dict_int_to_char, 5: dict_int_to_char}
    for j in [0, 1, 2, 3, 4, 5]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

# check license plate
def read_license_plate(text):
    text = text.upper().replace(' ', '')

    if license_complies_format_vehicle(text):
        return format_license_vehicle(text)
    
    if license_complies_format_motor1(text):
        return format_license_motor1(text)
    
    if license_complies_format_motor2(text):
        return format_license_motor2(text)

    return None
