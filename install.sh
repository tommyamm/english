#!/bin/bash

APP_NAME="eng"
APP_DIR="$(pwd)"
INSTALL_DIR="/usr/local/bin"
BASHRC="$HOME/.bashrc"

# Function to check if a command exists
command_exists () {
  type "$1" &> /dev/null ;
}

echo "Starting installation of $APP_NAME..."

# 1. Check for Python 3
if ! command_exists python3;
then
  echo "Python 3 is not installed. Please install it first."
  echo "For Debian/Ubuntu: sudo apt update && sudo apt install python3 -y"
  echo "For Fedora: sudo dnf install python3 -y"
  exit 1
fi

# 2. Check for pip
if ! command_exists pip3;
then
  echo "pip3 is not installed. Installing pip3..."
  sudo apt update
  sudo apt install python3-pip -y
  if [ $? -ne 0 ]; then
    echo "Failed to install pip3. Please install it manually."
    exit 1
  fi
fi

# 3. Install Python dependencies
if [ -f "$APP_DIR/requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  pip3 install -r "$APP_DIR/requirements.txt"
  if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies. Please check requirements.txt."
    exit 1
  fi
else
  echo "requirements.txt not found. Skipping dependency installation."
fi

# 4. Create a symlink to the main script
echo "Creating symlink for $APP_NAME..."
sudo ln -sf "$APP_DIR/source/main.py" "$INSTALL_DIR/$APP_NAME"
if [ $? -ne 0 ]; then
  echo "Failed to create symlink. Please check permissions."
  exit 1
fi

# # 5. Add alias to .bashrc
# ALIAS_LINE="alias $APP_NAME=\"$INSTALL_DIR/$APP_NAME\""
# if ! grep -q "$ALIAS_LINE" "$BASHRC"; then
#   echo "Adding alias to $BASHRC..."
#   echo "$ALIAS_LINE" >> "$BASHRC"
#   echo "Please run 'source $BASHRC' or restart your terminal to use the new alias."
# else
#   echo "Alias already exists in $BASHRC."
# fi

echo "Installation of $APP_NAME completed successfully!"


