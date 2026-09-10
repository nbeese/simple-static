from copystatic import recursive_copy
from generator import generate_pages_recursive
import os
import shutil
import sys

def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        base_path = "/"
    else:
        base_path = sys.argv[1]
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    recursive_copy("./static", "./docs")
    generate_pages_recursive("./content","template.html","./docs",base_path)
    print(base_path)
main()
