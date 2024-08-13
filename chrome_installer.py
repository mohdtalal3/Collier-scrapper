import os
import subprocess
def is_chrome_installed():
    """Check if Google Chrome is installed."""
    try:
        subprocess.run(["google-chrome", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_chrome():
    """Install Google Chrome on Debian-based systems."""
    print("Google Chrome is not installed. Installing now...")
    try:
        # Download the Google Chrome .deb package
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], check=True)
        # Install the downloaded package
        subprocess.run(["sudo", "apt", "install", "./google-chrome-stable_current_amd64.deb", "-y"], check=True)
        # Clean up the .deb file after installation
        subprocess.run(["rm", "google-chrome-stable_current_amd64.deb"], check=True)
        print("Google Chrome has been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the installation of Google Chrome: {e}")
        exit(1)

def main():
    # Step 1: Check if Google Chrome is installed
    if not is_chrome_installed():
        install_chrome()
if __name__ == "__main__":
    main()
