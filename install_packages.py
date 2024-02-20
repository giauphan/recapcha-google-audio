import subprocess

def install_packages():
    packages = [
        "playwright",
        "recognizer",  
        "python-dotenv",
        "google",
        "google-api-python-client"
    ]
    try:
        subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
        print("Successfully upgraded pip")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upgrade pip. Error: {e}")
    for package in packages:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")

if __name__ == "__main__":
    install_packages()
    