from copystatic import recursive_copy
from generator import generate_page, generate_pages_recursive
import os
import shutil


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    recursive_copy("./static", "./public")
    generate_pages_recursive("./content","template.html","./public")

main()
