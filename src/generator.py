from posix import mkdir
from posixpath import dirname

from converter import markdown_to_html_node
from extract import extract_title
import os
import pathlib

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path, "r")
    md = file.read()
    file.close()

    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(md)
    title = extract_title(md)

    html_content = html_node.to_html()

    updated_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(updated_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # for loop to traverse the directory tree
    for name in os.listdir(dir_path_content):
        # construct the complete paths at the current level
        full_content_path = os.path.join(dir_path_content, name)
        full_dest_path = os.path.join(dest_dir_path, name)

        # check if the content path resolves to a file
        if os.path.isfile(full_content_path) == True:

            # make sure the markdown files are handled appropriately
            if pathlib.Path(full_content_path).suffix == ".md":

                # construct the full destination path with the correct file extension
                # make sure the parent directory exists by creating if
                # then generate the html page and bob's your uncle
                full_dest_html_path = pathlib.Path(full_dest_path).with_suffix(".html")
                pathlib.Path(full_dest_html_path).parent.mkdir(parents=True, exist_ok=True)
                generate_page(full_content_path,template_path, full_dest_html_path)
        else:
            # the recursive part of it all
            generate_pages_recursive(full_content_path,template_path, full_dest_path)
