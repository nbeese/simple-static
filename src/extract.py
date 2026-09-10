import re

# Extract functions for links, images and title of the markdown page
# catch all bracket regex \((.*?)\) is discouraged for links:
# no separation, possible conflicts with brackets set for other things, like remarks or similar

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

def extract_title(markdown:str):
    # Reminder: slicing is safer than lstrip in this case since we know exactly which header we are looking for
    # expecting h1 header, extracting just the first instance by escaping the for loop when first instance is found
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# ") == True:
            title = line[2:]
            stripped_title = title.strip()
            return stripped_title

    raise Exception("no h1 header found")
