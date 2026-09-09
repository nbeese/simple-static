from copystatic import recursive_copy
from generator import generate_page
import os
import shutil


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    recursive_copy("./static", "./public")
    generate_page("content/index.md","template.html","public/index.html")

main()
