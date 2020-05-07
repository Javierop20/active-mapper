<img align="center" src="https://github.com/Javierop20/active-mapper/blob/master/TFG/images/logo.PNG">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![os](https://img.shields.io/badge/OS-Linux,%20macOS-yellow.svg)
![pythonver](https://img.shields.io/badge/python-3.6%2B-blue.svg)

Active-mapper is a tool for creating a CMDB of the actives detected in a PCAP, extract information of them and save them in a JSON Format and show them in a web browser report.
Also export the PCAP to GEXF for graphical representation of the communication between nodes.

It uses [Bro/Zeek](https://github.com/bro/bro) for the disection, [JA3](https://github.com/salesforce/ja3) for the detection of User-Agents, [p0f](https://github.com/p0f/p0f) for the OS Detection, [brassfork](https://github.com/mikkolehtisalo/brassfork) for the creation of nodes from PCAP and [CSVtoGEXF](https://github.com/oerpli/CSVtoGEXF) for creating the GEPHI graph.

Active-mapper is meant to be used in Ubuntu environments. It can be used in Debian 9, 10 and CentOS if you install Zeek manually. Developed by Javier Ortega for the final thesis in Telecommunications Engineering of the Universidad de Zaragoza.

### Features
- Support of multitude of protocols
- Quick creation of reports in HTML
- JSON Output
- GEXF Representation of the nodes and edges

## Getting Started

1. Clone this repository

```buildoutcfg
git clone https://github.com/Javierop20/active-mapper.git
```

2. Install the tool (sudo privileges needed)

```buildoutcfg
cd active-mapper/TFG/
python3 install.sh
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

## TODO
- Website for the GEXF
- Improve the performance of the tool in bigger PCAPs
- Add real-time analysis
