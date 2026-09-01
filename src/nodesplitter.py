from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = list()

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
                splitted = node.text.split(delimiter)
                if len(splitted) % 2 == 0:
                    raise Exception("unpaired delimiter")
                else:
                    for (i,piece) in enumerate(splitted):
                        if piece == "":
                            continue
                        elif i % 2 == 0:
                            new_node = TextNode(piece, text_type= TextType.TEXT)
                            new_nodes.append(new_node)
                        else:
                                new_node= TextNode(piece, text_type= text_type)
                                new_nodes.append(new_node)

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = list()

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
                #use extract function here
                extracted = extract_markdown_images(node.text)
                remaining = node.text

                for anchor, url in extracted:
                    delimiter = f"![{anchor}]({url})"
                    split_remain = remaining.split(delimiter,maxsplit=1)
                    if split_remain[0] !="":
                        new_node = TextNode(split_remain[0], text_type= TextType.TEXT)
                        new_nodes.append(new_node)
                    new_node = TextNode(anchor, text_type= TextType.IMAGE, url=url)
                    new_nodes.append(new_node)
                    remaining = split_remain[1]

                if remaining !="":
                    new_node = TextNode(remaining, text_type= TextType.TEXT)
                    new_nodes.append(new_node)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = list()

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
                #use extract function here
                extracted = extract_markdown_links(node.text)
                remaining = node.text

                for anchor, url in extracted:
                    delimiter = f"[{anchor}]({url})"
                    split_remain = remaining.split(delimiter,maxsplit=1)
                    if split_remain[0] !="":
                        new_node = TextNode(split_remain[0], text_type= TextType.TEXT)
                        new_nodes.append(new_node)
                    new_node = TextNode(anchor, text_type= TextType.LINK, url=url)
                    new_nodes.append(new_node)
                    remaining = split_remain[1]

                if remaining !="":
                    new_node = TextNode(remaining, text_type= TextType.TEXT)
                    new_nodes.append(new_node)

    return new_nodes
