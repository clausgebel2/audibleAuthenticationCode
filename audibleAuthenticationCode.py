import sys
import subprocess
import re
import shutil
import os


def ffprobe_exists():
    path = shutil.which("ffprobe")

    if path is None:
        return False
    else:
        return True


def get_activation_bytes(aax_file):
    if ffprobe_exists():
        program = "ffprobe"
        args = [aax_file]
        try:
            completed_process = subprocess.run([program] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               text=True)

            # ffprobe exits with an error -> output is in stderr
            output = completed_process.stderr

        except subprocess.CalledProcessError as e:
            print("Error:", e)

        pattern = r'\bfile checksum ==\s*([a-fA-F0-9]+)'
        match = re.search(pattern, output)

        if match:
            # Save pattern element in brackets
            activation_bytes = match.group(1)
            print("Audible activation bytes: " + activation_bytes)
            return activation_bytes
        else:
            print("Error: no activation bytes found.")
            return "Error: no activation bytes found."
    else:
        print("Please install 'ffmpeg'.")


def get_authentication_code(aax_name):
    authentication_code = get_activation_bytes(aax_name)
    if authentication_code == -1:
        print("Error: could not read activation byte.")
        exit(-1)

    os.chdir("tables")
    program = "./rcrack"
    args = [".", "-h", authentication_code]
    try:
        completed_process = subprocess.run([program] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = completed_process.stdout

    except subprocess.CalledProcessError as e:
        print("Error:", e)

    pattern = r'hex:([0-9]+)'
    match = re.search(pattern, output)
    os.chdir("..")

    if match:
        # Save pattern element in brackets
        authentication_code = match.group(1)
        print("Audible authentication code: " + authentication_code)
        return(authentication_code)
    else:
        print("Error: no authentication code found.")
        return "Error: no authentication code found."


if len(sys.argv) < 2:
    print("Please add the name of the aax files as argument.")
    sys.exit(1)
file_name = sys.argv[1]
get_authentication_code(file_name)




