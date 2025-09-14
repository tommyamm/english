#!/bin/bash

APP_NAME="eng"
INSTALL_DIR="/usr/local/bin"

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

echo "Uninstallation of $APP_NAME completed. Database has not been touched."


