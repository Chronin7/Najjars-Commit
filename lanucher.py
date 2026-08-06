import os
import sys
import venv
import subprocess

def setup_and_run():
    # Define paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(project_dir, ".venv")
    
    # Determine the python executable path inside the venv
    if sys.platform == "win32":
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")

    # 1. Create venv if it doesn't exist
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        venv.create(venv_dir, with_pip=True)

    # 2. Install requirements using the venv's pip
    if os.path.exists("requirements.txt"):
        print("Installing/Updating requirements...")
        try:
            subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            return
    else:
        print("No requirements.txt found. Skipping installation.")

    # 3. Launch the game using the venv's python
    print("Launching Metroidvania...")
    if os.path.exists("tile_editer.py"):
        # os.execv replaces the current process with the venv python process
        os.execv(venv_python, [venv_python, "tile_editer.py"])
    else:
        print("Error: main.py not found.")

if __name__ == "__main__":
    setup_and_run()
