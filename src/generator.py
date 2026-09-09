from posixpath import dirname

from converter import markdown_to_html_node
from extract import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path, "r")
    md = file.read()
    file.close()
    print(f"md: {md!r}")

    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()
    print(f"template_content: {template_content!r}")

    html_node = markdown_to_html_node(md)
    title = extract_title(md)
    print(f"title: {title!r}")

    html_content = html_node.to_html()
    print(f"html_content: {html_content!r}")

    updated_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    print(f"The contents of the html:\n {updated_content}")

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(updated_content)
