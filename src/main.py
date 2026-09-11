from copystatic import recursive_copy
from generator import generate_pages_recursive
import os
import shutil
import sys

def main():
    # check and set base_path for deployment, set default to "/" aka root folder of the the project
    if len(sys.argv) == 1:
        base_path = "/"
    else:
        base_path = sys.argv[1]

    # check if doc exists and clean up if it does
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")

    # copy from static to doc and generate everything
    recursive_copy("./static", "./docs")
    generate_pages_recursive("./content","template.html","./docs",base_path)
main()
