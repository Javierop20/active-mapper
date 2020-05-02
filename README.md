<img align="center" src="https://github.com/Javierop20/active-mapper/blob/master/images/logo.PNG">
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
Active-mapper is a tool for creating a CMDB of the actives detected in a PCAP, extract information of them and save them in a JSON Format and show them in a web browser report.
Also export the PCAP to GEXF for graphical representation of the communication between nodes.

It uses [Bro/Zeek](https://github.com/bro/bro) for the disection, [JA3](https://github.com/salesforce/ja3) for the detection of User-Agents and [p0f](https://github.com/p0f/p0f) for the OS Detection.

Active-mapper is meant to be used in Ubuntu environments or in WSL of Windows.

### Features
- Support of multitude of protocols
- Quick creation of reports
- JSON Output
- GEXF Representation of the nodes and edges
- To be added: Website for the GEXF, improvement for analysis performance, real-time analysis.

## Getting Started

1. Clone this repository

```buildoutcfg
git clone https://github.com/Javierop20/active-mapper.git
```

2. Install the tool (sudo privileges needed)

```buildoutcfg
cd active-mapper/TFG/
python3 install.py
```

3. Exectute the tool

```buildoutcfg
python3 app.py
```

## Usage

```buildoutcfg
$ python3 app.py
    _        _   _
   / \   ___| |_(_)_   _____       _ __ ___   __ _ _ __  _ __   ___ _ __
  / _ \ / __| __| \ \ / / _ \_____| '_ ` _ \ / _` | '_ \| '_ \ / _ \ '__|
 / ___ \ (__| |_| |\ V /  __/_____| | | | | | (_| | |_) | |_) |  __/ |
/_/   \_\___|\__|_| \_/ \___|     |_| |_| |_|\__,_| .__/| .__/ \___|_|
                                                  |_|   |_|
Introduce the base directory where the pcap is located:
<----Introduce here the directory with only the .pcap in it--->

```