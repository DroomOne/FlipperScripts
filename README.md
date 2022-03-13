# read_state.py

Reads the `DolphinStoreData` struct from `dolphin.state` files. 

## Usage

`python3 read_state.py <path-to-dolphine.state>`

## Output

```python 
[+] Read buffer of 40 bytes
[+] SavedStructHeader
    magic:                       208
    version:                     1
    checksum:                    230
    flags:                       0
    timestamp:                   0

[+] DolphinStoreData
    DolphinAppSubGhz:            0
    DolphinAppRfid:              0
    DolphinAppNfc:               6
    DolphinAppIr:                0
    DolphinAppIbutton:           0
    DolphinAppBadusb:            0
    DolphinAppU2f:               0
    butthurt_daily_limit:        6

    flags:                       0
    icounter:                    106
    butthurt:                    0
    timestamp:                   1647147878 (2022-03-13 06:04:38)
``` 


### Help

```python
> python3 read_state.py -h 
usage: read_state.py [-h] file

Read the contents of a flipper-zero's dolphin.state

positional arguments:
  file        Path of the dolphin.state file

optional arguments:
  -h, --help  show this help message and exit
``` 

## Credits
Thanks to the FlipperZero team for developing this awsome product! 

- Lamp (Tarsad) : For the idea, and sharing his `dolphin.state` files. 

## TODO
- Write a custom `dolphin.state` file
