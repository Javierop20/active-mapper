FROM ubuntu:18.04
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections &&\ 
    apt-get install -y -q

RUN mkdir /etc/dma/
RUN echo 'user@example.org|smtp.example.org:password' | tee -a /etc/dma/auth.conf &&\
    echo 'MAILNAME /etc/mailname' | tee -a /etc/dma/dma.conf &&\
    echo 'example@example.org' | tee -a /etc/mailname

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install git sudo gnupg -y

RUN apt-get install -y dma --option=Dpkg::Options::=--force-confdef 

RUN useradd --create-home --shell /bin/bash ubuntu && \
    echo 'ubuntu:ubuntu' | chpasswd
RUN usermod -aG sudo ubuntu
ADD TFG/ /home/ubuntu/

RUN sudo sh /home/ubuntu/install.sh

RUN pip3 install -r /home/ubuntu/requirements.txt

RUN sudo chmod +x /home/ubuntu/brassfork && \
	chown -R ubuntu:ubuntu /home/ubuntu/
EXPOSE 5000

ENTRYPOINT ["/bin/bash"]
