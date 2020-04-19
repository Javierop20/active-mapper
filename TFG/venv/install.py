import os
os.system("echo Welcome to the Active-mapper installation. This will require sudo privileges")
cwd = os.getcwd()
os.system("echo Installing Zeek and dependencies...")
os.system("sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev git figlet -y")
os.system("sudo apt-get install -y p0f")
os.system('sudo sh -c "echo deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_18.04/ / > /etc/apt/sources.list.d/security:zeek.list"')
os.system("wget -nv https://download.opensuse.org/repositories/security:zeek/xUbuntu_18.10/Release.key -O Release.key")
os.system("sudo apt-key add - < Release.key")
os.system("sudo apt-get update")
os.system("sudo apt-get install zeek -y")
os.system("sudo mkdir /opt/zeek/share/zeek/site/ja3/")
os.system("cd && git clone https://github.com/salesforce/ja3.git")
os.system("cd && cd ja3/ && sudo cp zeek/* /opt/zeek/share/zeek/site/ja3/")
os.system("cd && rm -rf ja3/")
os.system("cd && echo '@load tuning/json-logs' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek")
os.system("cd && echo '@load tuning/track-all-assets' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek")
os.system("cd && echo '@load ./ja3' | sudo tee -a /opt/zeek/share/zeek/site/local.zeek")

os.system("echo Configuring python env...")
os.system("sudo apt install python3-pip -y")
os.system("cd "+cwd+" && pip3 install -r requirements.txt")
decision=input("Finished! Do you want to run the program now?[y/n]")
if decision=='y':
    import app
else:
    exit()





