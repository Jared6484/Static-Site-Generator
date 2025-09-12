import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type for transforming to HTML")

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    node_list = []

    for node in old_nodes:
        text = node.text
        d_len = len(delimeter)
        i = 0
        end_of_cutout =0
        while i < len(text):
            if text[i:i+d_len]  == delimeter:
                end_of_cutout = text.find(delimeter, i+d_len) # find del starting at index past len of deli
                if end_of_cutout == -1:
                    raise Exception("Invalid Markdown syntax. ")

                if i >0:
                    node_list.append(TextNode(text[:i], TextType.TEXT))
                
                content = text[i + d_len:end_of_cutout]
                node_list.append(TextNode(content, text_type))

                text = text[end_of_cutout + d_len:]
                i=0

            else:
                i+=1

        if text:
            node_list.append(TextNode(text, TextType.TEXT))
    return node_list

def extract_markdown_images(text):

    match_list = re.findall(r"\!\[(.+?)\]\((.+?)\)", text)
    return match_list

def extract_markdown_links(text):
    match_list = re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)
    return match_list

def split_nodes_link(node):
    i =0
    new_nodes = []
    node_text = node.text
    caption_links = extract_markdown_links(node_text)
    if not caption_links:
        raise Exception("No markdown links to extract")

    while i < len(node_text):
        if node_text[i] == "[":
            if i > 0:
                cutoff = node_text[:i]
                new_nodes.append(TextNode(cutoff, TextType.TEXT))
                node_text = node_text[i:]

            
            new_nodes.append(TextNode(caption_links[0][0], TextType.LINK, caption_links[0][1]))
            len_to_rmv = len(caption_links[0][0]) + len(caption_links[0][1]) +4
            node_text = node_text[len_to_rmv:]
            i=0
            

            if len(caption_links) > 0:
                del caption_links[0]
            continue
        i += 1  

    if node_text:
        new_nodes.append(TextNode(node_text, TextType.TEXT))
        
    return new_nodes
            
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        i =0
        node_text = node.text
        caption_images = extract_markdown_images(node_text)
        if not caption_images:
            raise Exception("No markdown images to extract")

        while i < len(node_text):
            if node_text[i] == "!":
                if i > 0:
                    cutoff = node_text[:i] 
                    if len(cutoff) > 0:
                        new_nodes.append(TextNode(cutoff, TextType.TEXT))
                        node_text = node_text[i:]
                
                new_nodes.append(TextNode(caption_images[0][0], TextType.IMAGE, caption_images[0][1]))
                len_to_rmv = len(caption_images[0][0]) + len(caption_images[0][1]) +5 # the add of 4 accounts for []() characters
                node_text = node_text[len_to_rmv:]
                i=0
                

                if len(caption_images) > 0:
                    del caption_images[0]
                continue
            i += 1  

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
        caption_images = []
    return new_nodes

def text_to_textnodes(text):
    
    test