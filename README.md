# MAC Addresss Changer
Changes MAC Address of the specified interface

## Requirements
Language Used = Python3<br />
Modules/Packages used:
* re
* os
* datetime
* random
* scapy
* optparse
* time
* subprocess
* colorama
<!-- -->
Install the dependencies:
```bash
pip install -r requirements.txt
```

## Input
The mac_address_changer.py takes the following arguments through the command that is used to run the Python Program:
* '-i', "--iface" : interface to chance MAC Address of
* '-m', "--mac" : MAC Address to set

## Working
It uses 'ipconfig' command to change the MAC Address of the System.<br />
If no MAC Address is specified, it will randomly generate a MAC Address.

### Note
This would only work on Linux Operating Systems, because this Program uses 'ipconfig' command which is supported by the Linux Command Line Interface.