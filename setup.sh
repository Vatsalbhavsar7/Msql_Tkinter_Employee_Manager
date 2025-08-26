#!/bin/bash
echo "=========================="
echo " Employee Manager Installer"
echo "=========================="

# --- Check Python ---
if ! command -v python3 &> /dev/null
then
    echo "Python not found. Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
else
    echo "Python is already installed."
fi

# --- Check MySQL ---
if ! command -v mysql &> /dev/null
then
    echo "MySQL not found. Installing..."
    sudo apt install -y mysql-server
    sudo systemctl start mysql
    sudo systemctl enable mysql
else
    echo "MySQL is already installed."
fi

# --- Create virtual environment ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# --- Activate venv ---
source venv/bin/activate

# --- Install requirements ---
echo "Installing Python dependencies inside virtual environment..."
pip install --upgrade pip
pip install -r requirements.txt

# --- Final Status ---
echo "=========================="
echo " All requirements installed in venv!"
echo "=========================="

# Run main script inside venv
python main.py
