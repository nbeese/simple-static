#print("hello world")
from textnode import TextNode, TextType

def main():
    node = TextNode("this is dummy text",TextType.LINK_TEXT,"https://boot.dev")
    print(node)
    
main()
