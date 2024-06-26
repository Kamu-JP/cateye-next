import json
import tarfile
import os
import shutil
from pathlib import Path
import subprocess
import pip
import sys

version = "10.1.0"

try:
    import requests
    from rich.progress import Progress
    from rich.console import Console
    from rich.theme import Theme
    from rich.prompt import Prompt
except ImportError as e:
    missing_package = str(e).split(" ")[-1].strip("'")
    print(f"Error: Missing package '{missing_package}'.")
    print("This script requires the 'requests' and 'rich' packages.")
    print("Please set up a virtual environment and install the required packages:")
    print("""
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install requests rich
    """)
    sys.exit(1)

home_directory = os.path.expanduser('~')

# Theme
custom_theme = Theme({
    "error": "bold red",
    "success": "bold green",
    "normal": "blue"
})

console = Console(theme=custom_theme)

def start():

    print("Please select action")
    print("( install: Install Package from Official API | exit: Quit Cateye-next )")
    action = Prompt.ask("action", choices=["install", "exit"])
    print("")

    if action == "install":

        package_source = input("Select a package source (pip/npm/cateye): ")
        
        if package_source == "pip" or package_source == "npm":
            package_name = input("Enter the package name: ")
            install_package(package_source, package_name)

        if package_source == "cateye":
            print("Please enter Package URL")
            url = input("url> ")
            print("")
            Package_Install(url)

    elif action == "exit":

        exit(0)

def install_package(package_source, package_name):
    if package_source == "pip":
        try:
            # Install Python package using pip
            subprocess.check_call(["pip", "install", package_name])
            print(f"Installed {package_name} successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")
    elif package_source == "npm":
        try:
            # Install Node.js package using npm
            subprocess.check_call(["npm", "install", package_name])
            print(f"Installed {package_name} successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")
    else:
        pass

def language_prompt():
    language = Prompt.ask("lang", choices=["EN", "JP"])
    return language

def download_file(url, destination):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as f, Progress() as progress:
        task = progress.add_task(f"Downloading ( {url} )", total=total_size)
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
            progress.update(task, advance=len(chunk))

def extract_tar_gz(file_path, extract_path):
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(path=extract_path)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def delete_directory(directory):
    try:
        os.rmdir(directory)
    except OSError as e:
        pass

def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)
    except:
        console.print_exception()

def copy_or_move(source_file, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)
    
    destination_file = os.path.join(destination_dir, os.path.basename(source_file))
    
    if os.path.exists(destination_file):
        with open(source_file, 'rb') as fsrc, open(destination_file, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)
    else:
        shutil.move(source_file, destination_file)

def Package_Install(url):

    download_file(f"{url}", f"install_info.json")

    with open("install_info.json", "r") as file:
        data = json.load(file)

    pkgname = data["name"]

    if "version" in data:

        if data["version"] == "legacy":

            # Not supported
            exit(f"Package named '{pkgname}' is not supported.")

        elif data["version"] == "10":
            # Supported
            pass
            
    else:

        # Not supported
        exit(f"Package named '{pkgname}' is not supported.")
 
    console.print(f"[normal] > [/]Display information about package '{pkgname}'.")

    pkgfile = data["url"]

    console.print(f"[normal] - [/]Main file: {pkgfile}")

    pkgfolder: str = data["folder"]
    pkgfolder = pkgfolder.replace("HOME",home_directory)

    console.print(f"[normal] - [/]Install folder: {pkgfolder}")

    files = data["files"]

    console.print(f"[normal] - [/]Files: {' '.join(files)}")

    dependencies = data["dependencies"]

    if len(dependencies) > 0:

        console.print(f"[normal] - [/]Dependencies: {' '.join(dependencies)}")

    scripts = data["script"]

    if len(dependencies) > 0:

        with Progress() as progress1:

            task1 = progress1.add_task("Install dependencies", total=len(dependencies))

            for dependencie in dependencies:

                Package_Install(dependencie)

                progress1.update(task1, advance=1)

        print("")

        console.print("[normal] > [/]Installed dependencies: ")
        print(f"{' '.join(dependencies)}")

        print("")

    download_file(pkgfile,"cateye-installing.tar.gz")
    create_directory(pkgfolder)
    extract_tar_gz("cateye-installing.tar.gz", pkgfolder)
    os.remove("install_info.json")
    os.remove("cateye-installing.tar.gz")

    if len(scripts) > 0:

        with Progress() as progress2:

            task2 = progress2.add_task("Run scripts", total=len(scripts))

            for script in scripts:

                exec(script)

                progress2.update(task2, advance=1)

    print("")

    console.print(f"[normal] > [/]Installed package: '{pkgname}'")

    print("")

try:

    print(f"Cateye-next {version}")
    print("")

    start()

except:

    console.print_exception()
