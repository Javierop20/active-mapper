import os
os.system("echo Welcome to the Active-mapper installation. This will require sudo privileges")
cwd = os.getcwd()
os.system("echo Installing Zeek...")
os.system("sudo su")
os.system("apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev git figlet -y")
os.system("cd /tmp")
os.system("git clone --recursive https://github.com/zeek/zeek")
os.system("cd zeek")
os.system("./configure --prefix=/opt/bro/")
os.system("make")
os.system("make install")
os.system("echo '$PATH:/opt/bro/bin' >/etc/environment")
os.system("export PATH=/opt/bro/bin:$PATH")
os.system("echo Configuring Zeek...")
os.system("cat @load tuning/json-logs.zeek>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("cat @load tuning/track-all-assets>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("cat @load ./ja3>>/usr/local/zeek/share/zeek/site/local.conf")
os.system("git clone https://github.com/salesforce/ja3.git")
os.system("cd ja3/")
os.system("mkdir /usr/local/zeek/share/zeek/site/ja3/")
os.system("cp zeek/* /usr/local/zeek/share/zeek/site/ja3/")
os.system("cd .. && rm -rf ja3/")
os.system("cd "+cwd)
os.system("echo Configuring python env...")
os.system("pip install -r requirements.txt")
decision=input("Finished! Do you want to run the program now?[y/n]")
if decision=='y' or 'Y' or 'yes' or 's' or 'S' or 'si':
    import app
else:
    exit()





