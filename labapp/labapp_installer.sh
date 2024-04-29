#!/bin/bash

# Check if Docker is installed, install it if it's not
if ! command -v pip &> /dev/null
then
    # Update apt
    sudo DEBIAN_FRONTEND=noninteractive apt-get update --yes
    echo "pip could not be found, installing..."
    sudo apt-get install -y python3-pip
fi

# Variable Declarations
IMAGE=ghcr.io/f5devcentral/f5xc-lab-mcn-practical/labapp:latest
SERVICE=mcn-practical-labapp.service
APPDIR=/opt/mcn-practical-labapp/app
SCRIPTDIR=/opt/mcn-practical-labapp/script
REPO_URL=https://github.com/f5devcentral/f5xc-lab-mcn-practical.git
BRANCH=dev

# Create directories
mkdir -p $SCRIPTDIR
mkdir -p $APPDIR

# Create the start_labapp.sh script
cat <<EOF >$SCRIPTDIR/start_app.sh
#!/bin/bash

if [ ! -d "$APPDIR/.git" ]; then
    git clone -b $BRANCH $REPO_URL $APPDIR
else
    cd $APPDIR
    # Ensure that the local repository is tracking the correct remote and branch
    git remote set-url origin $REPO_URL
    git fetch --all
    # Reset to the specified branch forcefully
    git checkout $BRANCH
    git reset --hard origin/$BRANCH
    git clean -fdx
    git pull origin $BRANCH
fi

# Install required Python packages
cd $APPDIR/labapp/app 
pip install -r requirements.txt

# Start the Gunicorn server
gunicorn --workers 4 --bind 0.0.0.0:1337 app:app
EOF

# Make the script executable
chmod +x $SCRIPTDIR/start_app.sh

# Create systemd service file
cat <<EOF >/etc/systemd/system/$SERVICE
[Unit]
Description=MCN Practical Lab App
After=network.target

[Service]
WorkingDirectory=$APPDIR
ExecStart=/bin/bash $SCRIPTDIR/start_app.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
systemctl daemon-reload
systemctl enable $SERVICE
systemctl start $SERVICE

echo "$SERVICE has been installed and started as a systemd service."
