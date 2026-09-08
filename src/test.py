from platform import node
from pydoc import html
from enum import Enum
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode,TextType
from block import BlockType
from converter import text_node_to_html_node,text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from nodesplitter import split_nodes_delimiter,split_nodes_image,split_nodes_link
from extract import extract_markdown_images,extract_markdown_links
import unittest

#Unittests


class OtherType(Enum):
    UNSUPPORTED = "unsupported"

class TestStaticGen(unittest.TestCase):
    def test_repr(self):
        html = HTMLNode(tag="p",value="This is gonna be text.",children=None, props=None)
        self.assertEqual(html.__repr__(), "HTMLNode(p, This is gonna be text., None, None)")

    def test_props(self):
        html = HTMLNode(props={"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(html.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_none_props(self):
        html = HTMLNode(props=None)
        self.assertEqual(html.props_to_html(), "")

    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, HTMLNode().to_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
            node = LeafNode("a", "Click this!", props={"href": "https://www.google.com"})
            self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click this!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_props(self):
        great_grandchild_node = LeafNode("b", "grandchild link")
        grandchild_node = ParentNode("p", [great_grandchild_node])
        child_node = ParentNode("a", [grandchild_node],{"class": "greeting", "href": "https://boot.dev"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a class="greeting" href="https://boot.dev"><p><b>grandchild link</b></p></a></div>'
        )

    def test_to_html_empty_children(self):
        parent_node = ParentNode("p", children=[])
        self.assertEqual(
            parent_node.to_html(),
            "<p></p>"
        )

    def test_to_html_value_error_tag(self):
        child_node = LeafNode("b","child")
        parent_node = ParentNode(None,[child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_value_error_child(self):
        parent_node = ParentNode("p",children=None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_deeper_nesting(self):
        great_grandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("p", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
                      parent_node.to_html(),
                      '<div><span><p><b>grandchild</b></p></span></div>'
                  )

    def test_to_html_with_mixed_siblings(self):
        great_grandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("p", [great_grandchild_node])
        child_node2 = LeafNode(None, "text")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node,child_node2])
        self.assertEqual(
                  parent_node.to_html(),
                  '<div><span><p><b>grandchild</b></p></span>text</div>'
              )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props,{'href': 'https://boot.dev'})

    def test_image(self):
        node = TextNode("This is an image alt text node", TextType.IMAGE, url="src/some_image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "src/some_image.jpg","alt": "This is an image alt text node"})

    def test_error_type(self) -> None:
        node = TextNode("This is an error text node", "swerved", url="")
        self.assertRaises(AttributeError, text_node_to_html_node, node)

    def test_unsupported_enum(self):
        node = TextNode("Invalid enum type", OtherType.UNSUPPORTED)
        self.assertRaises(AttributeError, text_node_to_html_node, node)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node,node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)

    def test_uneq_all(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC,"https://example.com")
        self.assertNotEqual(node,node2)

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_unchanged(self):
       node = TextNode("This is italic already", TextType.ITALIC)
       new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
       self.assertEqual(new_nodes, [
           TextNode("This is italic already", TextType.ITALIC)
           ])

    def test_split_no_delimiter(self):
        node = TextNode("This is text with a word", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter,[node],delimiter="", text_type=TextType.TEXT)

    def test_split_unpaired_delimiter(self):
        node = TextNode("This is _text with a word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter,[node],delimiter="_", text_type=TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_error(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with [a link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_images_nobefore(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_nobefore(self):
        node = TextNode(
            "[a link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )



    def test_split_images_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a little bit of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a little bit of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_after(self):
        node = TextNode(
            "This is text with [a link](https://boot.dev) and another [second link](https://google.com) and a little bit of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
                TextNode(" and a little bit of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_nobefore_butafter(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a little bit of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a little bit of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_nobefore_butafter(self):
        node = TextNode(
            "[a link](https://boot.dev) and another [second link](https://google.com) and a little bit of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
                TextNode(" and a little bit of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_short(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_short(self):
        node = TextNode(
            "[a link](https://boot.dev)[second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a link", TextType.LINK, "https://boot.dev"),
                TextNode("second link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(nodes)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_onlytext(self):
            nodes = "This is text with nothing else"
            new_nodes = text_to_textnodes(nodes)
            self.assertListEqual(
                [
                    TextNode("This is text with nothing else", TextType.TEXT),
                ],
                new_nodes
            )

    def test_text_to_textnodes_single_inst(self):
             nodes = "This is text with just **some bold text** nothing else"
             new_nodes = text_to_textnodes(nodes)
             self.assertListEqual(
                 [
                     TextNode("This is text with just ", TextType.TEXT),
                     TextNode("some bold text", TextType.BOLD),
                     TextNode(" nothing else", TextType.TEXT),
                 ],
                 new_nodes
             )

    def test_text_to_textnodes_dj_khaled(self):
            nodes = "This is text with **some bold text**, **another instance** and **another one** and **another one** and **another one**"
            new_nodes = text_to_textnodes(nodes)
            self.assertListEqual(
                     [
                         TextNode("This is text with ", TextType.TEXT),
                         TextNode("some bold text", TextType.BOLD),
                         TextNode(", ", TextType.TEXT),
                         TextNode("another instance", TextType.BOLD),
                         TextNode(" and ", TextType.TEXT),
                         TextNode("another one", TextType.BOLD),
                         TextNode(" and ", TextType.TEXT),
                         TextNode("another one", TextType.BOLD),
                         TextNode(" and ", TextType.TEXT),
                         TextNode("another one", TextType.BOLD),
                     ],
                     new_nodes
                 )

    def test_text_to_textnodes_multikill(self):
            nodes = "This is text with **some bold text**_another instance_[link text](http://boot.dev)"
            new_nodes = text_to_textnodes(nodes)
            self.assertListEqual(
                     [
                         TextNode("This is text with ", TextType.TEXT),
                         TextNode("some bold text", TextType.BOLD),
                         TextNode("another instance", TextType.ITALIC),
                         TextNode("link text", TextType.LINK, url="http://boot.dev"),
                     ],
                     new_nodes
                 )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_both(self):
        md = """




This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraph(self):
        block = "This is just a normal sentence with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PLAIN)

    def test_heading(self):
        block = "### This is just a normal sentence with a heading."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_codeblock(self):
        block = "```\nThis is just a code block.```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is just a normal sentence in a quote.\n>And this is the second sentence in that quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- This is just a normal sentence in an unordered list.\n- This is the second sentence in an unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)

    def test_ordered_list(self):
        block = "1. This is just a normal sentence in an ordered list.\n2. This is the second sentence in the ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

    def test_fallback(self):
        block = "####### This is just a normal sentence in an ordered list.\n2. This is the second sentence in the ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.PLAIN)

    def test_fallback_2(self):
        block = "#######This is just a normal sentence."
        self.assertEqual(block_to_block_type(block), BlockType.PLAIN)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock_markdown_html(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

    def test_unordered_list_md_html(self):
            md ="""
- List item one
- List item still goes on
- and onto the next one
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>List item one</li><li>List item still goes on</li><li>and onto the next one</li></ul></div>",
            )

    def test_ordered_list_md_html(self):
              md ="""
1. First item
2. Second item
3. Third item
  """
              node = markdown_to_html_node(md)
              html = node.to_html()
              self.assertEqual(
                  html,
                  "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
              )

    def test_unordered_list_md_html_link(self):
            md ="""
- List item one
- List item still goes on [to google](https://google.com)
- and onto the next one
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                '<div><ul><li>List item one</li><li>List item still goes on <a href="https://google.com">to google</a></li><li>and onto the next one</li></ul></div>',
            )

    def test_blockquote(self):
            md ="""
> He says
> She says
> crap
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>He says She says crap</blockquote></div>",
            )

    def test_heading_md_html(self):
            md ="""
### He says

She says crap
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h3>He says</h3><p>She says crap</p></div>",
                )

if __name__ == "__main__":
    unittest.main()
