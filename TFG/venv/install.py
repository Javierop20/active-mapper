import os
os.system("echo Welcome to the Active-mapper installation. This will require sudo privileges")
cwd = os.getcwd()
os.system("echo Installing Zeek...")
os.system("sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev git figlet -y")
os.system("sudo apt-get install -y p0f")
os.system("cd /tmp && git clone --recursive https://github.com/zeek/zeek && cd zeek && ./configure --prefix=/opt/zeek/")
os.system("cd /opt/zeek && make && make install")
os.system("cat @load tuning/json-logs.zeek>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("cat @load tuning/track-all-assets>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("cat @load ./ja3>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("cd && git clone https://github.com/salesforce/ja3.git")
os.system("mkdir /usr/local/zeek/share/zeek/site/ja3/")
os.system("cd && cd ja3/ && cp zeek/* /usr/local/zeek/share/zeek/site/ja3/")
os.system("cd && rm -rf ja3/")
os.system("echo Configuring python env...")
os.system("cd "+cwd+" && pip install -r requirements.txt")
decision=input("Finished! Do you want to run the program now?[y/n]")
if decision=='y' or 'Y' or 'yes' or 's' or 'S' or 'si':
    import app
else:
    exit()





