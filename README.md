# home-projects

Requirements
Hardware 
- rasberry pi 4B
- 2x DHT22 sensors
- wire (optional)
- soldering iron (optional)

Rasberry Pi 4B 

Pi Pre-Setup
boot os 2020-05-27-raspios-buster-arm64.img
- downloaded from https://www.raspberrypi.org/forums/viewtopic.php?t=275370 (current in beta testing, might change by the time your reading)

Use rasberry pi imager to load os on to your ssd.
- https://www.raspberrypi.org/downloads/ 

insert sd card

attach sensors, by default the app uses pin 4 and pin 22 for data between sensor and pi.

turn on pi

Pi Setup

After normal setup:

sudo apt update
sudo apt upgrade

Install Docker and docker-compose
sudo apt install docker
sudo apt install docker-compose

Druid
Needs java 8 for druid, java 8 not realy supported for rasberry pi os 64/deb buster
This worked for me, however this may change.
- https://adoptopenjdk.net/installation.html#linux-pkg

Java 8 setup as above:
sudo wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -

sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/

sudo wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -

Note if you get "command not found", in some cases add-apt-repository command will be missing.
sudo apt-get install -y software-properties-common

wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -

sudo apt-get install adoptopenjdk-8-hotspot

java --version

should show
openjdk version "1.8.0_232"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_232-b09)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.232-b09, mixed mode)

If it shows a differnt version run <sudo update-alternatives --config java>, 
and follow instructions to set it to: 
  </usr/lib/jvm/adoptopenjdk-8-hotspot-arm64/bin/java>
  
Note before running druid, refer to https://druid.apache.org/docs/latest/operations/single-server.html
Druids minimum RAM requirements are 4GB + 1 core. 
Currently I am running a 4GB version of PI 4b, but a 8gb version has been released.
If you are running a 4gb version I recommend, detaching monitor output + keyboard + mouse and instead ssh in.
As my pi would freeze up otherwise when running druid. I would not recommend running druid on the 4gb pi. 

Instead ssh into your pi:

Note 'pi' here is the username/account your going to login with, you can also omit it from ssh.

From linux(mac should be the same) machine : 
- ssh XXX.XXX.XXX.XXX@pi
- ssh XXX.XXX.XXX.XXX

Note if you dont know your devices ip you can in a pi terminal run(might have to install but should be there)
- ifconfig
- Your device ip is here: <UP,BROADCAST,RUNNING,MULTICAST> inet XXX.XXX.XXX.XXX
 
From windows, download https://www.putty.org/
And use this app too ssh(this is what I use atm).

















random notes

test project-go-api DockerFile

sudo docker build -t michaeljohnwatters/project-go-api .
sudo docker run --publish 8080:8080 -t michaeljohnwatters/project-go-api



handy docker commands
stop all
docker container stop $(docker container ls -aq)
remove all
docker container rm $(docker container ls -aq)

stop and remove
docker container stop $(docker container ls -aq) && docker container rm $(docker container ls -aq)
