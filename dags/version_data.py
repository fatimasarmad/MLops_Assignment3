#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command):
    """
    Execute a shell command and print output
    
    Args:
        command (str): Command to execute
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False

def version_with_dvc(data_file='processed_data.csv'):
    """
    Track the data file with DVC
    
    Args:
        data_file (str): Path to the data file to track
        
    Returns:
        bool: True if versioning succeeded, False otherwise
    """
    print(f"\n{'='*50}")
    print("STARTING DVC VERSIONING")
    print(f"{'='*50}")
    
    # Check if DVC is installed
    if not run_command("dvc --version"):
        print("DVC is not installed. Please install it with: pip install dvc")
        return False
    
    # Check if the data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file {data_file} not found")
        return False
    
    # Initialize DVC if not already initialized
    if not os.path.exists(".dvc"):
        print("Initializing DVC...")
        if not run_command("dvc init"):
            return False
        print("DVC initialized successfully")
    else:
        print("DVC already initialized")
    
    # Add the data file to DVC
    if not run_command(f"dvc add {data_file}"):
        return False
    
    # Add the .dvc file to git
    dvc_file = f"{data_file}.dvc"
    if os.path.exists(dvc_file):
        if not run_command(f"git add {dvc_file}"):
            # This might fail if git is not initialized
            print("Warning: Could not add .dvc file to git. Make sure git is initialized.")
    
    print(f"\nSuccessfully versioned {data_file} with DVC")
    print(f"{'='*50}")
    return True

if __name__ == "__main__":
    data_file = 'processed_data.csv'
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    
    version_with_dvc(data_file)