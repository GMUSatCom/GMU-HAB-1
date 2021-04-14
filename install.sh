#!/bin/bash
#Base Install DIR
base=$HOME/HAB

echo "**Starting to install HAB packages...**"

read -p "Install GMU HAB software bundle? a = All, y = continue, n = exit " install

case $install in
	#All
	a|A )
		echo "Making the directories..."
		sudo mkdir -p $base
		sudo mkdir -p $base/git

		echo "Cloning all necessary software libraries..."
		sudo git clone --single-branch --branch main https://github.com/GMUSatCom/GMU-HAB-1.git $base/git
		echo "Copying source files..."
		sudo cp -a $base/git/SRC/. $base
		echo "Cleaning..." 
		sudo rm -rf $base/git
		echo "Creating PATH reference for LoRaAirService Radio Driver" 
		sudo chmod +x $base/LoRaAirService
		sudo ln $base/LoRaAirService /bin/LoRaAirService
		echo "Making the startup scrip executable"
		sudo chmod +x $base/startup.sh

		
		#Start python installs
		echo "Installing Blinka module..."
		sudo pip3 install adafruit-blinka

		echo "Installing pynmea2 module..."
		sudo pip3 install pynmea2
		
		echo "Installing mpl3115a2 module..."
		sudo pip3 install adafruit-circuitpython-mpl3115a2
		
		echo "Installing circuitpython for lsm9ds1 module..."
		sudo pip3 install adafruit-circuitpython-lsm9ds1
		
		#Enable I2C
		echo "Enabling I2C"
		if sudo grep -q "i2c-bcm2708" /etc/modules;then
			echo "Seems i2c-bcm2708 module already exists, skip this step."
		else
			echo "i2c-bcm2708" >> /etc/modules
		fi

		if sudo grep -q "i2c-dev" /etc/modules;then
			echo "Seems i2c-dev module already exists, skip this step."
		else
			echo "i2c-dev" >> /etc/modules
		fi

		if sudo grep -q "dtparam=i2c1=on" /boot/config.txt;then
			echo "Seems i2c1 parameter already set, skip this step."
		else
			echo "dtparam=i2c1=on" >> /boot/config.txt
		fi

		if sudo grep -q "dtparam=i2c_arm=on" /boot/config.txt;then
			echo "Seems i2c_arm parameter already set, skip this step."
		else
			echo "dtparam=i2c_arm=on" >> /boot/config.txt
		fi

		if [ -f /etc/modprobe.d/raspi-blacklist.conf ];then
			sudo sed -i "s/^blacklist spi-bcm2708/#blacklist spi-bcm2708/" /etc/modprobe.d/raspi-blacklist.conf
			sudo sed -i "s/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/" /etc/modprobe.d/raspi-blacklist.conf
			else
		echo "File raspi-blacklist.conf does not exist, skip this step."
		fi

		echo "I2C enabled!"
		echo "Installing i2c-tools"
		if hash i2cget 2>/dev/null;then
			echo "I2c-tools is installed already"
		else
			sudo apt-get install -y i2c-tools
		fi

		#Display i2c detect on screen
		echo "**Using the command 'sudo i2cdetect -y 1' will show you if your I2C device is properly connected and available, like this:" 
		sudo i2cdetect -y 1
		
		#Enable SPI
		echo "Enabling SPI"
		if sudo grep -q "dtparam=spi=on" /boot/config.txt;then 
			echo "SPI is already enabled"
		else 
			echo "dtparam=spi=on" >> /boot/config.txt
			echo "SPI enabled"
		fi
		
		#Start PYCAM
		if sudo grep -q "start_x=1" /boot/config.txt;then
			echo "PI-CAM is already enabled"
		else
			sudo sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
			echo "DONT FORGET TO REBOOT FOR PI-CAM"
		fi
		
		echo "**Completed installation!**"
		read -p "Show files installed? [y\n] " cdls
		case $cdls in
			y|Y)
				dir $base
			;;
		esac
		echo "******************************************************************************************************"
		echo "The file RadioServerTestInfo contains all the info on running and debugging the radio server."
		echo "Now the startup scrip should be executable. You can start the entire system by typing 'bash startup.sh'"
		echo "The installation is complete. Enjoy collecting data! - From GMU SATCOM"
		echo "******************************************************************************************************"
		exit 1
	;; 
	#End Case ALL
	y|Y )	
		echo "Making the directories..."
		sudo mkdir -p $base
		sudo mkdir -p $base/git

		echo "Cloning all necessary software libraries..."
		sudo git clone --single-branch --branch main https://github.com/GMUSatCom/GMU-HAB-1.git $base/git
		echo "Copying source files..."
		sudo cp -a $base/git/SRC/. $base
		echo "Cleaning..." 
		sudo rm -rf $base/git
		echo "Creating PATH reference for LoRaAirService Radio Driver" 
		sudo chmod +x $base/LoRaAirService
		sudo ln $base/LoRaAirService /bin/LoRaAirService
		echo "Making the startup scrip executable"
		sudo chmod +x $base/startup.sh
		

		read -p "Install Blinka module for busio? [y/n] " blinka		
		case $blinka in 
			y|Y)
				echo "Installing Blinka module..."
				sudo pip3 install adafruit-blinka
				;;
		esac

		read -p "Install pynmea2 for gps? [y\n] " pynmea2
		case $pynmea2 in
			y|Y)
				echo "Installing pynmea2 module..."
				sudo pip3 install pynmea2
				;;
		esac

		read -p "Install circuitpython for altimiter? [y\n] " mpl3115a2
		case $mpl3115a2 in
			y|Y)
				echo "Installing mpl3115a2 module..."
				sudo pip3 install adafruit-circuitpython-mpl3115a2
				;;
		esac
		
		read -p "Install circuitpython for imu? [y\n] " imu
		case $imu in
			y|Y)
				echo "Installing circuitpython for lsm9ds1 module..."
				sudo pip3 install adafruit-circuitpython-lsm9ds1
				;;
		esac

		# enable I2C on Raspberry Pi
		read -p "Enable I2C Interface for devices? [y\n] " i2c
		case $i2c in
			y|Y)
				echo "Enabling I2C"
				if sudo grep -q "i2c-bcm2708" /etc/modules;then
					echo "Seems i2c-bcm2708 module already exists, skip this step."
				else
					sudo echo "i2c-bcm2708" >> /etc/modules
				fi

				if sudo grep -q "i2c-dev" /etc/modules;then
					echo "Seems i2c-dev module already exists, skip this step."
				else
					sudo echo "i2c-dev" >> /etc/modules
				fi

				if sudo grep -q "dtparam=i2c1=on" /boot/config.txt;then
					echo "Seems i2c1 parameter already set, skip this step."
				else
					sudo echo "dtparam=i2c1=on" >> /boot/config.txt
				fi

				if sudo grep -q "dtparam=i2c_arm=on" /boot/config.txt;then
					echo "Seems i2c_arm parameter already set, skip this step."
				else
					sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt
				fi

				if [ -f /etc/modprobe.d/raspi-blacklist.conf ];then
					sudo sed -i "s/^blacklist spi-bcm2708/#blacklist spi-bcm2708/" /etc/modprobe.d/raspi-blacklist.conf
					sudo sed -i "s/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/" /etc/modprobe.d/raspi-blacklist.conf
					else
				echo "File raspi-blacklist.conf does not exist, skip this step."
				fi

				echo "I2C enabled!"
				echo "Installing i2c-tools"
				if hash i2cget 2>/dev/null;then
					echo "I2c-tools is installed already"
				else
					sudo apt-get install -y i2c-tools
				fi

				#Display i2c detect on screen
				echo "**Using the command 'sudo i2cdetect -y 1' will show you if your I2C device is properly connected and available, like this:" 
				sudo i2cdetect -y 1
			;;
		esac

		#Enable spi in config for radio
		read -p "Enable SPI for radio? [y\n] " spi
		case $spi in
			y|Y)
				echo "Enabling SPI"
				if sudo grep -q "dtparam=spi=on" /boot/config.txt;then 
					echo "SPI is already enabled"
				else 
					sudo echo "dtparam=spi=on" >> /boot/config.txt
					echo "SPI enabled"
				fi
			;;
		esac

		#Enable Pi CAM
		read -p "Start and install PI-CAM? (Requires reboot!) [y\n] " pycam
		case $pycam in 
			y|Y)
				if sudo grep -q "start_x=1" /boot/config.txt;then
					echo "Pycam already enabled, no need to restart!"

				else
					sudo sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
					echo "DONT FORGET TO REBOOT FOR PI-CAM"
				fi					
					
			;;
		esac
		
		echo "**Completed installation!**"
		read -p "Show files installed? [y\n] " cdls
		case $cdls in
			y|Y)
				dir $base
			;;
		esac
		echo "******************************************************************************************************"
		echo "The file RadioServerTestInfo contains all the info on running and debugging the radio server."
		echo "Now the startup scrip should be executable. You can start the entire system by typing 'bash startup.sh'"
		echo "The installation is complete. Enjoy collecting data! - From GMU SATCOM"
		echo "******************************************************************************************************"
		exit 1		
	;; 
	#End yes 
	
esac #End Case

echo "Goodbye!"
exit 1