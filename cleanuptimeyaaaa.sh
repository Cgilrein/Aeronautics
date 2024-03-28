#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CIRCUIT_DATA_DIR="$SCRIPT_DIR/circuit_data"
GPS_DATA_DIR="$SCRIPT_DIR/gps_data"

# Check if the directory exists
if [ -d "$CIRCUIT_DATA_DIR" ]; then
    # Remove all files in the directory
    sudo rm -f "$CIRCUIT_DATA_DIR"/*
    echo "All files in circuit_data directory have been removed."
else
    echo "Error: circuit_data 0 directory not found."
fi

# Check if the directory exists
if [ -d "$GPS_DATA_DIR" ]; then
    # Remove all files in the directory
    sudo rm -f "$GPS_DATA_DIR"/*
    echo "All files in gps_data directory have been removed."
else
    echo "Error: gps_data 0 directory not found."
fi


CIRCUIT_DATA_DIR="../circuit_data"
GPS_DATA_DIR="../gps_data"

# Check if the directory exists
if [ -d "$CIRCUIT_DATA_DIR" ]; then
    # Remove all files in the directory
    sudo rm -f "$CIRCUIT_DATA_DIR"/*
    echo "All files in circuit_data directory have been removed."
else
    echo "Error: circuit_data 1 directory not found."
fi

# Check if the directory exists
if [ -d "$GPS_DATA_DIR" ]; then
    # Remove all files in the directory
    sudo rm -f "$GPS_DATA_DIR"/*
    echo "All files in gps_data directory have been removed."
else
    echo "Error: gps_data 1 directory not found."
fi