from copystatic import recursive_copy
from generator import generate_page
import os
import shutil


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    recursive_copy("./static", "./public")
    generate_page("content/index.md","template.html","public/index.html")
    generate_page("content/blog/glorfindel/index.md","template.html","public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md","template.html","public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md","template.html","public/blog/majesty/index.html")
    generate_page("content/contact/index.md","template.html","public/contact/index.html")

main()
