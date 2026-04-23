#!/bin/bash

# Troubleshooting script for subtitle-burner project

echo "Running troubleshooting script..."

# Make all .sh scripts executable
echo "Making all .sh files executable..."
chmod +x *.sh
for dir in */; do
    if [ -d "$dir" ]; then
        cd "$dir"
        chmod +x *.sh 2>/dev/null
        cd ..
    fi
done

echo "Troubleshooting complete."