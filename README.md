# FortiGate Address Adder 1.0
## Description
Generates script for importing IPv4 addresses to FortiGate firewalls configuration
* Input file must contain one address per line. Script tries to create address ranges for subsequent addresses for more condensed configuration (please sort the lines alphabetically in your text editor to make it work)
* Keep in mind that amount of address objects in FortiGate groups are limited.

## Requirements
* Python 3.6 or newer 
* *argparse*
* *ipaddress* 

This code is ready to build as Windows console app using *auto-py-to-exe*
```
pyinstaller --noconfirm --onefile --console "fg_addr_adder.py"
```

## Usage
Help text:
```
usage: fg_addr_adder.py [-h] [-s SUFFIX] [-c COMMENT] [-g GROUP] -i INPUT
                        [-o OUTPUT]

Generates script for importing IPv4 addresses to FortiGate firewalls
configuration

optional arguments:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix SUFFIX
                        Text at the end of the created addresses (default        
                        "_block")
  -c COMMENT, --comment COMMENT
                        Comment for new addresses
  -g GROUP, --group GROUP
                        Group name for created addresses

input & output files:
  -i INPUT, --input INPUT
                        Input file with IPv4 addresses list
  -o OUTPUT, --output OUTPUT
                        Output file with generated script
```

*addrs.txt*
```
1.1.1.1
1.1.1.2
1.1.1.3
192.168.10.1
192.168.12.3
```

Run command:
```
python fg_addr_adder.py -i addrs.txt -c 'Some comment' -g 'Test group' -o 'myoutput.txt'
```

*myoutput.txt:*
```
config firewall address
edit 1.1.1.1_1.1.1.3_block
set range 1.1.1.1-1.1.1.3
set comment "Some comment"
next
edit 192.168.10.1_block
set subnet 192.168.10.1/32
set comment "Some comment"
next
end
config firewall addrgrp
edit Test_group
set member 1.1.1.1_1.1.1.3_block 192.168.10.1_block
next
end
```