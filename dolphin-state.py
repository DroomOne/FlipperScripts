import argparse
import struct
import os 
from datetime import datetime 

parser = argparse.ArgumentParser(description="Read the contents of a flipper-zero's dolphin.state")
parser.add_argument("file", type=str, help="Path of the dolphin.state file")
parser.add_argument("--out", type=str, nargs='?', help="Output path of the dolphin.state file")
parser.add_argument("--icounter", type=int, nargs='?', help="Overwrite the icounter value in dolphin.state")
parser.add_argument("--butthurt", type=int, nargs='?', help="Overwrite the butthurt value in dolphin.state")
args = parser.parse_args()

HEADER_SIZE = 8 
DolphinAppMAX = 7
BUTTHURT_MAX = 14

# https://github.com/flipperdevices/flipperzero-firmware/blob/3c77ae2eb88db05e4bc8a51c7a0dbd64943c0f9f/applications/dolphin/helpers/dolphin_state.c
LEVEL2_THRESHOLD = 300
LEVEL3_THRESHOLD = 1800

# https://github.com/flipperdevices/flipperzero-firmware/blob/3c77ae2eb88db05e4bc8a51c7a0dbd64943c0f9f/applications/dolphin/passport/passport.c
moods = [{"name": "Happy", "max_butthurt": 4}, {"name": "Ok", "max_butthurt": 9}, {"name": "Angry", "max_butthurt": BUTTHURT_MAX}]


# https://github.com/flipperdevices/flipperzero-firmware/blob/3c77ae2eb88db05e4bc8a51c7a0dbd64943c0f9f/lib/toolbox/saved_struct.c
def unpack_header(buffer):
    (magic, version, checksum, flags, timestamp) = struct.unpack('BBBBI', buffer[0:HEADER_SIZE])
    print("[+] SavedStructHeader")
    print("    magic:\t\t\t", magic)
    print("    version:\t\t\t" , version)
    print("    checksum:\t\t\t", checksum)
    print("    flags:\t\t\t", flags)
    print("    timestamp:\t\t\t", timestamp)
    print()

 
# https://github.com/flipperdevices/flipperzero-firmware/blob/3c77ae2eb88db05e4bc8a51c7a0dbd64943c0f9f/applications/dolphin/helpers/dolphin_state.h 
def unpack_state(buffer):
    (DolphinAppSubGhz, DolphinAppRfid, DolphinAppNfc, DolphinAppIr, DolphinAppIbutton, DolphinAppBadusb, DolphinAppU2f, butthurt_daily_limit) = struct.unpack('BBBBBBBB', buffer[HEADER_SIZE:HEADER_SIZE+8])
    print("[+] DolphinStoreData")
    print("    DolphinAppSubGhz:\t\t", DolphinAppSubGhz)
    print("    DolphinAppRfid:\t\t" , DolphinAppRfid)
    print("    DolphinAppNfc:\t\t", DolphinAppNfc)
    print("    DolphinAppIr:\t\t", DolphinAppIr)
    print("    DolphinAppIbutton:\t\t", DolphinAppIbutton)
    print("    DolphinAppBadusb:\t\t", DolphinAppBadusb)
    print("    DolphinAppU2f:\t\t", DolphinAppU2f)
    print("    butthurt_daily_limit:\t", butthurt_daily_limit)
    print()
    
    (flags, icounter, butthurt, timestamp) = struct.unpack("IIIQ", buffer[HEADER_SIZE+8:])

    print("    flags:\t\t\t", flags)
    print("    icounter:\t\t\t", icounter)
    print("    butthurt:\t\t\t", butthurt)
    print("    timestamp:\t\t\t", timestamp, '(' + str(datetime.fromtimestamp(timestamp)) + ')')
    print()

    if icounter >= LEVEL3_THRESHOLD:
      # There's only 3 levels, so percentage is at 100% once we hit level 3
      passport_pct = 100
      passport_level = 3
    elif icounter >= LEVEL2_THRESHOLD:
      passport_pct = ((icounter - LEVEL2_THRESHOLD) / (LEVEL3_THRESHOLD - LEVEL2_THRESHOLD)) * 100
      passport_level = 2
    else:
      passport_pct = (icounter / LEVEL2_THRESHOLD) * 100
      passport_level = 1

    for mood in reversed(moods):
      if (butthurt <= mood["max_butthurt"]): passport_mood = mood["name"]

    # https://github.com/flipperdevices/flipperzero-firmware/tree/c97d9a633ebf94af2365c6e17760b44cd8c88c60/assets/dolphin/external/L1_Leaving_sad_128x64
    # and
    # https://github.com/flipperdevices/flipperzero-firmware/blob/c97d9a633ebf94af2365c6e17760b44cd8c88c60/assets/dolphin/external/manifest.txt
    # If butthurt == BUTTHURT_MAX, there's a chance the L1_Leaving_sad animation will play
    if (butthurt == BUTTHURT_MAX): passport_mood += " enough to leave"

    print("[+] Passport")
    print("    level:\t\t\t", passport_level)
    print("    mood:\t\t\t", passport_mood)
    print("    percent complete:\t\t %.2f%%" % passport_pct)

def update_icounter(buffer, value): 
    print("[+] Updating icounter to", value)
    return buffer[:HEADER_SIZE+12] + struct.pack("I", value) + buffer[HEADER_SIZE+16:]

def update_butthurt(buffer, value):
    if value > BUTTHURT_MAX:
        print('[-]', value, 'is way too much butthurt for Flipper to handle (Max=14). Try decreasing it.') 
        print('[-] Skipping update_butthurt')
        return buffer 
        
    print("[+] Updating butthurt to", value)
    return buffer[:HEADER_SIZE+16] + struct.pack("I", value) + buffer[HEADER_SIZE+20:]

# https://github.com/flipperdevices/flipperzero-firmware/blob/3c77ae2eb88db05e4bc8a51c7a0dbd64943c0f9f/lib/toolbox/saved_struct.c
def dolphin_state_save(buffer, path):
    print('[+] Saving dolphin state to', path)
    checksum = 0
    for byte in buffer[HEADER_SIZE:]:
        checksum += byte
    
    print("[+] Calculated new checksum:", checksum % 256)
    buffer = buffer[:2] + struct.pack("B", checksum % 256) + buffer[3:] 
    with open(path, 'wb') as writer:
        writer.write(buffer)

    print("[+] Saved output to:", path)
    return buffer 


if (args.icounter is not None or args.butthurt is not None) and args.out is None: 
    print('--icounter and --butthurt requires a output path --out <path>')
    exit()

if not os.path.exists(args.file):
    print('[-]', args.file, 'does not exists. Exiting.')
    exit() 

with open(args.file, 'rb') as reader: 
    buffer = reader.read()

print("[+] Read", len(buffer), "bytes from", args.file)

if args.icounter is not None:
    buffer = update_icounter(buffer, args.icounter)

if args.butthurt is not None:
    buffer = update_butthurt(buffer, args.butthurt)

if args.out: 
    buffer = dolphin_state_save(buffer, args.out)

unpack_header(buffer)
unpack_state(buffer)
