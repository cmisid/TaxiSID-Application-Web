# Initialize a DigitalOcean droplet with a Ubuntu 14.04 image

# Login and change password
ssh root@46.101.234.224

# Add a new user "max" and give him a password
adduser max
# Give "max" sudo rights
gpasswd -a max sudo

# Change "PermitRootLogin yes" to "PermitRootLogin no"
nano /etc/ssh/sshd_config

# Restart SSH
service ssh restart

# Switch to user "max"
sudo su max

# Configure the timezone
sudo dpkg-reconfigure tzdata
# Configure NTP Synchronization
sudo apt-get update
sudo apt-get install ntp
# Create a Swap File
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo sh -c 'echo "/swapfile none swap sw 0 0" >> /etc/fstab'

# Setup Python and Apache
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install python3-pip python3-dev libapache2-mod-wsgi-py3

# Clone the repository containing the code
cd /var/www
sudo apt-get install git
sudo git clone https://github.com/TaxiSID/Production
# Rename the folder
sudo mv Production/ taxisid/
sudo chmod -R 777 taxisid/
cd taxisid

# Install the necessary Python libraries (can take some time)
sudo pip3 install -r setup/requirements.txt


# TO DO: install PostgreSQL and PostGis (EnterpriseDB ?)


# Configure and enable a virtual host
sudo cp setup/scripts/taxisid.conf /etc/apache2/sites-available/
sudo a2ensite taxisid
sudo service apache2 reload
sudo service apache2 restart

# Reboot the server and you should be done!
sudo reboot