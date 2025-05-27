import subprocess

# List of packages to install
packages = [
    "pandas",
    "networkx",
    "matplotlib",
    "requests"
]

# Install each package
for package in packages:
    subprocess.run(["pip", "install", package], check=True)