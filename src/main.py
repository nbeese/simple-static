from copystatic import recursive_copy
import os
import shutil


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    recursive_copy("./static", "./public")


main()
