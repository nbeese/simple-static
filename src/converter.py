from nodesplitter import split_nodes_delimiter,split_nodes_image,split_nodes_link
from textnode import TextNode,TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b",value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i",value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code",value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a",value=text_node.text, props= {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img",value ="",props={"src" : text_node.url, "alt":text_node.text})
    else:
        raise AttributeError()

def text_to_textnodes(text):
    nodes = [TextNode(text=text,text_type=TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(nodes,delimiter="**", text_type=TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes,delimiter="_", text_type=TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes,delimiter="`", text_type=TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    final_nodes = split_nodes_link(image_nodes)
    return final_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = list()

    for block in blocks:
        block = block.strip()
        if block != "":
            clean_blocks.append(block)

    return clean_blocks
