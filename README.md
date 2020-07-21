
https://druid.apache.org/docs/latest/tutorials/tutorial-batch.html#loading-data-with-a-spec-via-command-linebnnmjbnmj

TO RUN

chmod a+x ./run.sh
chmod a+x ./run druid.sh
./run.sh


remote development
https://medium.com/@pythonpow/remote-development-on-a-raspberry-pi-with-ssh-and-vscode-a23388e24bc7


add - pip install flask-restful
add pip3 install flask-restful

I think a bunch of stuff needs to be installed in docker files, cause it seems to need to be downloaded, and i guess ut looks localy? if you dont say where to get it.


# home-projects

DISCLAIMER might break your pi.


Requirements
Hardware 
- rasberry pi 4B 4GB version, 8GB is recommened.
- 2x DHT22 sensors
- micro sd card
- SSD (pi does not support some ssds) TODO LINK HERE
- USB to SATA connector (some connects do not work find compatible) TODO LINK HERE
- wire (optional)
- soldering iron (optional)

Software
RasberryPi OS 64 bit

SSD SETUP

1. Installation of RasberryPi OS 64 bit

Follow the guide here : https://www.jeffgeerling.com/blog/2020/im-booting-my-raspberry-pi-4-usb-ssd

Summary of Guide above :

On your other device:
1. Download rasberry pi imager (https://www.raspberrypi.org/downloads/)

2. Download Rasberry Pi OS 64 bit Image (currently a BETA build, as of 21/07/2020)
  - https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2020-05-28/2020-05-27-raspios-buster-arm64.zip

3. Flash SD Card with (the above imager), using the rasberry pi imager.

4. Insert SD card, and boot rasberry pi.

5. In Terminal :
                - sudo apt update
                - sudo apt full-upgrade

6. In Terminal :
                - sudo nano /etc/default/rpi-eeprom-update
                - change 'critical' to 'stable' then (write, exit) => (ctrl o, ctrl x) 
                
7. Update eeprom(in terminal) :
                - sudo rpi-eeprom-update -d -f /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-06-15.bin

Reboot your pi and check the bootloader version(in terminal):
                                        - vcgencmd bootloader_version


8. While your pi is running, plug your SSD into the pi (if the pi can detect the ssd you should see a notifcation on screen).
   If you dont you can run in the Terminal:
        - lsusb (before and after plugging in your ssd), to see if it has been detected(many usb to sata/ssds dont work for pi's)
        
8. If SSD is detected, unplug the SSD.

9. On your other device plug the ssd in and flash the same image above using the rasberry pi imager (dont unplug after finshing).

As of 21/07/2020, setup 10,11 may or may not be required in future, once rpi OS 64 has a stable build.
10. Once complete download/clone (This next part might be easier to do on linux or mac):
- https://github.com/raspberrypi/firmware

11. Navitage to your recently flashed SSD's boot folder and boot folder of the downloaded firmware above,
    Replace all the files on the SSD boot file ending in .elf or .dat, with the downloaded versions above.
    
12. Unplug your SSD, turn off your Rasberry PI and plug in the flashed SSD into a 3.0 USB port, removing the SD card.

13. Boot the rasberry pi, if it loads to the desktop it was sucessfuly :)

14. If 13 failed. Turn off and unplug the pi from the mains power. Go make a cup of tea and comeback and re-boot the pi.


SOFTWARE SETUP 

Update
- sudo apt update
- sudo apt upgrade

Install Docker and docker-compose
- sudo apt install docker
- sudo apt install docker-compose

Java8 (required by apache-druid)
Guide: https://adoptopenjdk.net/installation.html#linux-pkg
Summary of Guide:
- sudo apt-get install -y software-properties-common
- sudo wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
- sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
- sudo apt-get install adoptopenjdk-8-hotspot
- java --version

openjdk version "1.8.0_262"
OpenJDK Runtime Environment (build 1.8.0_262-b10)
OpenJDK 64-Bit Server VM (build 25.262-b10, mixed mode)

If your java version is wrong/not working uses(normally if you have mutiple java versions installed): 
- sudo update-alternatives --config java
- and follow instructions to set it to: </usr/lib/jvm/adoptopenjdk-8-hotspot-arm64/bin/java>
 
CLONE PROJECT

cd <your repo>

git clone https://github.com/MichaelJohnWatters/home-projects.git

CLONE DRUID

cd home-projects

git clone https://github.com/apache/druid.git
 



Currently I am running a 4GB version of PI 4b, but a 8gb version has been released.

If you are running a 4gb version I recommend, detaching monitor output + keyboard + mouse and instead ssh in or boot in commandline mode(look about in pi settings), As my pi would freeze up/crash.


Instead ssh into your pi:

Note 'pi' here is the username/account your going to login with.

From linux(mac should be the same) machine : 
- ssh XXX.XXX.XXX.XXX@pi
- ssh XXX.XXX.XXX.XXX

Note if you dont know your devices ip you can in a pi terminal run(might have to install but should be there)
- ifconfig
- Your device ip is here: <UP,BROADCAST,RUNNING,MULTICAST> inet XXX.XXX.XXX.XXX
 
From windows, download https://www.putty.org/
And use this app too ssh(this is what I use atm).

Finally run druid (only use nano-quick-start, pi wont be able to cope with anything else).

Running Druid:
cd into where ever you installed apache druid.
- cd /repo/apache-druid-0.18.1./
Finally run nano quick start 
- ./bin/start-nano-quickstart

Navigate to (your pi's device ip)
http://XXX.XXX.XXX.XXX:8888

DONE!

now refer to druid docs on how druid works https://druid.apache.org/docs/latest/tutorials/index.html
















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
