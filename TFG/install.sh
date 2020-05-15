#!/bin/sh
echo Welcome to the Active-mapper installation. This will require sudo privileges
dir=$PWD
echo Installing Zeek and dependencies...
sudo apt-get install wget p0f flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev git figlet -y
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_18.04/ /' > /etc/apt/sources.list.d/security:zeek.list"
wget -nv https://download.opensuse.org/repositories/security:zeek/xUbuntu_18.04/Release.key -O Release.key
sudo apt-key add - < Release.key
sudo apt-get update
sudo apt-get install zeek -y
sudo mkdir /opt/zeek/share/zeek/site/ja3/
cd && git clone https://github.com/salesforce/ja3.git
cd ja3/
sudo cp zeek/* /opt/zeek/share/zeek/site/ja3/
cd $dir
sudo chmod +x brassfork
rm -rf ja3/
echo '@load tuning/json-logs' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek
echo '@load tuning/track-all-assets' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek
echo '@load ./ja3' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek
echo Configuring python env...
sudo apt install python3-pip -y
cd $dir
pip3 install -r requirements.txt
clear
echo 'Instalation finished! For running the program you have to write in this console: python3 app.py'
echo 'Hope you like it! - Created by Javier Ortega - Universidad de Zaragoza'

