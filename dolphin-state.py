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
