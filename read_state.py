import argparse
import struct
import os 
from datetime import datetime 

#   saved_struct.c
# typedef struct {
#     uint8_t magic;
#     uint8_t version;
#     uint8_t checksum;
#     uint8_t flags;
#     uint32_t timestamp;
# } SavedStructHeader;

HEADER_SIZE = 8 
def unpack_header(buffer):
    (magic, version, checksum, flags, timestamp) = struct.unpack('BBBBI', buffer[0:HEADER_SIZE])
    print("[+] SavedStructHeader")
    print("    magic:\t\t\t", magic)
    print("    version:\t\t\t" , version)
    print("    checksum:\t\t\t", checksum)
    print("    flags:\t\t\t", flags)
    print("    timestamp:\t\t\t", timestamp)
    print()


# typedef struct {
#     uint8_t icounter_daily_limit[DolphinAppMAX];
#     uint8_t butthurt_daily_limit;
#     uint32_t flags;
#     uint32_t icounter;
#     uint32_t butthurt;
#     uint64_t timestamp;
# } DolphinStoreData;

DolphinAppMAX = 7 
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



parser = argparse.ArgumentParser(description="Read the contents of a flipper-zero's dolphin.state")
parser.add_argument("file", type=str, help="Path of the dolphin.state file")
args = parser.parse_args()

if not os.path.exists(args.file):
    print('[-]', args.file, 'does not exists. Exiting.')
    exit() 
    
with open(args.file, 'rb') as reader: 
    buffer = reader.read()

print("[+] Read buffer of", len(buffer), "bytes")

unpack_header(buffer)
unpack_state(buffer)