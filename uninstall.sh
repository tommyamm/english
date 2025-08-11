#!/bin/bash

APP_NAME="eng"
INSTALL_DIR="/usr/local/bin"
BASHRC="$HOME/.bashrc"

echo "Starting uninstallation of $APP_NAME..."

# 1. Remove the symlink
if [ -L "$INSTALL_DIR/$APP_NAME" ]; then
  echo "Removing symlink from $INSTALL_DIR/$APP_NAME..."
  sudo rm "$INSTALL_DIR/$APP_NAME"
  if [ $? -ne 0 ]; then
    echo "Failed to remove symlink. Please check permissions."
  fi
else
  echo "Symlink for $APP_NAME not found in $INSTALL_DIR."
fi

# # 2. Remove alias from .bashrc
# ALIAS_LINE="alias $APP_NAME=\"$INSTALL_DIR/$APP_NAME\""
# if grep -q "$ALIAS_LINE" "$BASHRC"; then
#   echo "Removing alias from $BASHRC..."
#   sed -i "\|$ALIAS_LINE|d" "$BASHRC"
#   echo "Please run 'source $BASHRC' or restart your terminal to apply changes."
# else
#   echo "Alias for $APP_NAME not found in $BASHRC."
# fi

echo "Uninstallation of $APP_NAME completed. Database has not been touched."


