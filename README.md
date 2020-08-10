
https://druid.apache.org/docs/latest/tutorials/tutorial-batch.html#loading-data-with-a-spec-via-command-linebnnmjbnmj

Remote development
https://medium.com/@pythonpow/remote-development-on-a-raspberry-pi-with-ssh-and-vscode-a23388e24bc7


# home-projects

DISCLAIMER might break your pi, lol.

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

Install vue dependencies (https://cli.vuejs.org/guide/installation.html)
- curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
- sudo apt install nodejs
- sudo npm install -g @vue/cli
- sudo npm update -g @vue/cli

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
 
 Install Adafruit Library (for reading sensors)
 - sudo pip3 install Adafruit_DHT
 
 Install Flask and flask-resful
 - sudo pip3 install flask-restful
 
CLONE PROJECT

cd <your repo>
- sudo git clone https://github.com/MichaelJohnWatters/home-projects.git

Install DRUID(into the home-projects folder, from website or command line)
- From: https://www.apache.org/dyn/closer.cgi?path=/druid/0.19.0/apache-druid-0.19.0-bin.tar.gz
- cd repo/home-projects
- tar -xzf apache-druid-0.19.0-bin.tar.gz
- sudo rm -r apache-druid-0.19.0-bin.tar.gz

OR

Naviate to your repo/home-projects
Get full path
- pwd (/home/pi/repo/home-projects/)
Then run with YOUR path:
- sudo wget -P /home/pi/repo/home-projects/ "http://apache.mirror.anlx.net/druid/0.19.0/apache-druid-0.19.0-bin.tar.gz"
- sudo tar -xzf apache-druid-0.19.0-bin.tar.gz
- sudo rm -r apache-druid-0.19.0-bin.tar.gz

Test it works:
Currently I am running a 4GB version of PI 4b, but a 8gb version has been released.
If you are running a 4gb version I recommend, detaching monitor output + keyboard + mouse and instead ssh in or boot in commandline mode(look about in pi settings), As my pi would freeze up/crash.
- cd apache-druid-0.19.0
- ./bin/start-nano-quickstart

Navigate to, to check it works.
192.168.1.218:8888/unified-console.html

In /repo/home-projects/
chmod a+x ./run.sh
chmod a+x ./run-druid.sh
chmod a+x ./drun.sh

INSTALL FIREWALL (https://www.raspberrypi.org/documentation/configuration/security.md)

- sudo apt install ufw
- sudo ufw enable
- sudo ufw allow 8080/tcp
- sudo ufw allow 5000/tcp

fail2ban
- sudo apt install fail2ban
- sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
- sudo nano /etc/fail2ban/jail.local            (for config)

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
