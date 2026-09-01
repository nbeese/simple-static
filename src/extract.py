import re

# catch all bracket regex \((.*?)\) is discouraged for links:
# no separation, possible conflicts with brackets set for other reasons

def extract_markdown_images(text:str)-> tuple:
    #lazy alt text regex !\[(.*?)\] and lazy url regex \((.*?)\)
    #complete image regex !\[([^\[\]]*)\]\(([^\(\)]*)\)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text:str)-> tuple:
    #lazy hyperlink text regex \[(.*?)\] and lazy url regex \((.*?)\)
    #lazy complete link regex \[([^\[\]]*)\]\(([^\(\)]*)\) - useful when image as link is preferred
    #complete link regex (?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\) - negative lookbehind to avoid conflicts with image alt text
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches
