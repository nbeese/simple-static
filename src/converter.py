from nodesplitter import split_nodes_delimiter,split_nodes_image,split_nodes_link
from textnode import TextNode,TextType
from htmlnode import LeafNode, ParentNode
from block import BlockType

# Converter functions needed to convert texts and blocks
# Ultimately converts the contents of a markdown file to html, the whole purposes of this course

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
    # convert text into nodes, one splitting function and delimiter after the other
    # note: final_nodes are after splitting for links
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

# less of a converter function, more a type determinator
def block_to_block_type(block):
    lines = block.split("\n")
    stripped = block.lstrip("#")
    if block.startswith("#") and stripped.startswith(" ") and len(block)-len(stripped) in range(1,7):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED
    elif all(line.startswith(f"{index+1}. ") for index,line in enumerate(lines)):
        return BlockType.ORDERED
    else:
        return BlockType.PLAIN

def text_to_children(text):
    children = list()
    nodes = text_to_textnodes(text)

    for node in nodes :
        child = text_node_to_html_node(node)
        children.append(child)

    return children

def heading_level_detector(block):
    # helper function for HEADING, to make sure it is the right heading level
    stripped_block = block.lstrip("#")
    heading_level = len(block) - len(stripped_block)

    if heading_level not in range(1,7):
        raise Exception("invalid heading level. blocktype assignment might be wrong!")
    else:
        return heading_level

def list_wrapper(block,block_type):
    # helper function for UNORDERED and ORDERED
    # wraps the contents into the needed <li> </li> pairings
    # determines stripping mode via given block_type argument
    lines = block.split("\n")
    wrapped_list = list()

    for line in lines:
        if block_type == BlockType.UNORDERED:
            stripped_line = line[2:]
        elif block_type == BlockType.ORDERED:
            stripped_line = line.split(". ", 1)[1]
        else:
            raise Exception("tried to use list_wrapper function on a block that is not a list type!")

        child = ParentNode(tag="li", children=text_to_children(stripped_line))
        wrapped_list.append(child)
    return wrapped_list

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = list()

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PLAIN:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)
            child = ParentNode(tag="p", children=text_to_children(paragraph_text))
            children.append(child)

        elif block_type == BlockType.HEADING:
            # use helper function to determine heading level
            level = heading_level_detector(block)
            # level+1 makes sure that the required leading whitespace after the # is removed as well.
            child = ParentNode(tag=f"h{level}", children=text_to_children(block[level+1:]))
            children.append(child)

        elif block_type == BlockType.CODE:
            # start is 4 because of the backticks and newline, -3 because of the end backticks
            # could be done more programmatically and less magic numbery, but that also has some caveats
            raw_text_node = TextNode(block[4:-3], TextType.TEXT)
            code_content = text_node_to_html_node(raw_text_node)
            child = ParentNode(tag="code", children=[code_content])
            outer_child = ParentNode(tag="pre", children=[child])
            children.append(outer_child)

        elif block_type == BlockType.UNORDERED or block_type == BlockType.ORDERED:
            # determine if unordered or ordered
            # list item surrounder function might be a good idea
            if block_type==BlockType.UNORDERED:
                child = ParentNode(tag="ul", children=(list_wrapper(block, block_type)))
                children.append(child)
            else:
                child = ParentNode(tag="ol", children=(list_wrapper(block, block_type)))
                children.append(child)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = list()
            for line in lines:
                cleaned = line.lstrip(">").strip()
                cleaned_lines.append(cleaned)

            result: str = " ".join(cleaned_lines)
            child = ParentNode(tag="blockquote", children=text_to_children(result))
            children.append(child)
        else:
            raise Exception("invalid BlockType")

    parent = ParentNode(tag="div",children=children)

    return parent
