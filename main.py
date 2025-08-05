import subprocess
import sys

# function to run a script based on it's name
def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        exit(1)

run_script("generate_name_artist_list.py")
run_script("download_from_youtube.py")