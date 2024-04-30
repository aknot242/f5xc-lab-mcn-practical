#!/bin/bash

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Check for Python3 pip and install if it's missing
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found, updating repositories and installing..."
    sudo apt-get update --quiet
    sudo apt-get install --quiet --yes python3-pip
fi

# Variable Declarations
REPO_URL="https://github.com/f5devcentral/f5xc-lab-mcn-practical.git"
BRANCH="main"
APPDIR="/opt/mcn-practical-labapp/app"
SCRIPTDIR="/opt/mcn-practical-labapp/scripts"

# Create necessary directories
mkdir -p "$APPDIR" "$SCRIPTDIR"

# Create the start script
cat <<EOF >"$SCRIPTDIR/start_app.sh"
#!/bin/bash

# Navigate to the app directory
cd "$APPDIR"

# Check if the directory is a git repository and if not, clone it
if [ ! -d ".git" ]; then
    git clone --branch $BRANCH $REPO_URL .
else
    # Reset repository to match the remote repository
    git remote set-url origin $REPO_URL
    git fetch --prune
    git checkout $BRANCH
    git reset --hard "origin/$BRANCH"
    git clean -fdx
fi

# Install required Python packages
pip3 install -r requirements.txt

# Start the Gunicorn server
export UDF="true" && gunicorn --workers 4 --chdir labapp/app --bind 0.0.0.0:1337 app:app
EOF

chmod +x "$SCRIPTDIR/start_app.sh"

# Create systemd service file
cat <<EOF >"/etc/systemd/system/mcn-practical-labapp.service"
[Unit]
Description=MCN Practical Lab App
After=network.target

[Service]
WorkingDirectory=$APPDIR
ExecStart=/bin/bash $SCRIPTDIR/start_app.sh
Restart=always
Type=simple

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize new service, enable it
systemctl daemon-reload
systemctl enable mcn-practical-labapp.service

echo "mcn-practical-labapp.service has been installed."
