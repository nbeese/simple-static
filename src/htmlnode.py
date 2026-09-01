from contextlib import closing
from typing import override


class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None or self.props == "":
            return ""
        else:
            formatted = str()
            for prop, content in self.props.items():
                formatted += f' {prop}="{content}"'

            return formatted


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)



    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("no tag provided")
        elif self.children == None:
            raise ValueError("parent children equals None")
        else:
            open_tags = f"<{self.tag}{super().props_to_html()}>"
            family = str()
            for child in self.children:
                family += child.to_html()

            closing = f"</{self.tag}>"

            return open_tags + family + closing
