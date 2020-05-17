<img align="center" src="https://github.com/Javierop20/active-mapper/blob/master/TFG/images/logo.PNG">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![os](https://img.shields.io/badge/OS-Linux,%20macOS-yellow.svg)
![pythonver](https://img.shields.io/badge/python-3.6%2B-blue.svg)

Active-mapper is a tool for creating a CMDB of the actives detected in a PCAP, extract information of them and save them in a JSON Format and show them in a web browser report.
Also export the PCAP to GEXF for graphical representation of the communication between nodes.

It uses [Bro/Zeek](https://github.com/bro/bro) for the disection, [JA3](https://github.com/salesforce/ja3) for the detection of User-Agents, [p0f](https://github.com/p0f/p0f) for the OS Detection, [brassfork](https://github.com/mikkolehtisalo/brassfork) for the creation of nodes from PCAP and [CSVtoGEXF](https://github.com/oerpli/CSVtoGEXF) for creating the GEPHI graph.

Active-mapper is meant to be used in Ubuntu environments. It can be used in Debian 9, 10 and CentOS if you install Zeek manually. In the folder TFG there is a Dockerfile for configuring directly a docker image for active-mapper.

Developed by Javier Ortega for the final thesis in Telecommunications Engineering of the Universidad de Zaragoza.

### Features
- Support of multitude of protocols
- Quick creation of reports in HTML
- JSON Output
- GEXF Representation of the nodes and edges
- Docker implementation for multi-plattform usage

## Getting Started

1. Clone this repository

```buildoutcfg
git clone https://github.com/Javierop20/active-mapper.git
```

2. Install the tool (sudo privileges needed)

```buildoutcfg
cd active-mapper/TFG/
./install.sh
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

## Usage with Docker

1. Clone this repository

```buildoutcfg
git clone https://github.com/Javierop20/active-mapper.git
```

2. Create the Docker image for Active-mapper

```buildoutcfg
cd active-mapper/
docker build --tag active-mapper .
```

3. Once the creation of the image is finished, you'll be able to see it using docker image ls

```buildoutcfg
$ docker image ls
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
active-mapper                  latest              74089d2d20cd        2 minutes ago       798MB
```

4. For launching the instance just run the following command

```buildoutcfg
docker run -it --net=host -u ubuntu active-mapper:latest
```

5. If you want to mount a folder with a pcap directly to the Docker container run

```buildoutcfg
docker run -it --net=host -u ubuntu -v <Path-to-your-pcap-file>:/home/ubuntu/<name-of-folder-in-container>/ active-mapper:latest
```

6. Another option is to copy the pcap file using docker cp once the container is running

```buildoutcfg
docker cp <Path-to-your-pcap>.pcap <Container-ID>:/home/ubuntu/<name-of-folder-in-container>/
```

7. Once inside the container, just run the app like in a normal Ubuntu. The app is in /home/ubuntu/

```buildoutcfg
$ cd /home/ubuntu/
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

8. The generated files will be in the path /home/ubuntu/name-of-folder-in-container/ and the HTML report will be in localhost:5000


## TODO
- Website for the GEXF
- Improve the performance of the tool in bigger PCAPs
- Add real-time analysis
- Merge and analyse multiple pcaps in the same folder
