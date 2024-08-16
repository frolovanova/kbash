import os
import subprocess

def main():
    user = os.getenv("USER", "defaultuser")
    home_dir = f"/home/user/{user}"
    
    # Ensure the home directory exists
    os.makedirs(home_dir, exist_ok=True)
    
    # Switch to user's home directory
    os.chdir(home_dir)
    
    # Launch a shell
    subprocess.run(["/bin/bash"])

if __name__ == "__main__":
    main()

