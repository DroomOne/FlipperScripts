# dolphin_state.py

Reads the `DolphinStoreData` struct from `dolphin.state` files. 

## Usage

### Reading 

`python3 dolphin_state.py <path-to-dolphin.state>`

### Writing 

**icounter**: Contains the amount of EXP flipper has

**butthurt**: Level of happiness flipper has - `BUTTHURT_MAX = 14`

With the `--icounter` and `--butthurt` the output `dolphin.state` can be modified. The script will automaticly update the checksum for the file. The `--out` parameter must be set. 

#### Setting EXP
`python3 dolphin_state.py dolphin.state --icounter=1337 --out dolphin-new.state`

#### Setting the Mood (Butthurt)
`python3 dolphin_state.py dolphin.state --butthurt=14 --out dolphin-new.state`

#### Setting EXP and Mood 
`python3 dolphin_state.py dolphin.state --icounter=1337 --butthurt=14 --out dolphin-new.state`

## Output

```python 
[+] Read 40 bytes from dolphin.state
[+] Updating icounter to 1337
[+] Saving dolphin state to new-dolphin.state
[+] Calculated new checksum: 161
[+] Saved output to: new-dolphin.state
[+] SavedStructHeader
    magic:                       208
    version:                     1
    checksum:                    161
    flags:                       0
    timestamp:                   0

[+] DolphinStoreData
    DolphinAppSubGhz:		 0
    DolphinAppRfid:		 20
    DolphinAppNfc:		 20
    DolphinAppIr:		 0
    DolphinAppIbutton:		 0
    DolphinAppBadusb:		 0
    DolphinAppU2f:		 2
    butthurt_daily_limit:	 46

    flags:			 0
    icounter:			 1337
    butthurt:			 14
    timestamp:			 1678561214 (2023-03-11 14:00:14)

[+] Passport
    level:			 2
    mood:			 Angry enough to leave
    percent complete:		 69.13%
``` 


### Help

```python
> python3 dolphin_state.py -h 
usage: dolphin_state.py [-h] file

Read the contents of a flipper-zero's dolphin.state

positional arguments:
  file        Path of the dolphin.state file

optional arguments:
  -h, --help  show this help message and exit
``` 

#### Reading / Writing the dolphin.state

1. Use the file manager version of the qflipper software for PC. 
2. Open the `internal flash storage`
3. Drag and drop the `dolphin.state` file to read/write it to the flipper!


## Credits
Thanks to the FlipperZero team for developing this awsome product! 

- Lamp (Tarsad) : For the idea, and sharing his `dolphin.state` files. And explaining how one could read/write the `dolphin.state` file. 

