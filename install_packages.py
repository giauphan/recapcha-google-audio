import subprocess

def install_packages():
    packages = [
        "playwright",
        "recaptcha-challenger",  # Assuming this is the correct package name, please adjust if needed
        "python-dotenv",
    ]

    for package in packages:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")

if __name__ == "__main__":
    install_packages()
    