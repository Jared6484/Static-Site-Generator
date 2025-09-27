import re
import textwrap

from textnode import TextNode, TextType, BlockType
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
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
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
                continue

            else:
                i+=1

        if text:
            node_list.append(TextNode(text, TextType.TEXT))
    return node_list

def extract_markdown_images(text):

    match_list = re.findall(r"\!\[(.+?)\]\((.+?)\)", text)
    return match_list

def extract_markdown_links(text):
    #match_list = re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)
    match_list = re.findall(r"\[(.+?)\]\((.+?)\)", text)
    return match_list

def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        i =0
        node_text = node.text
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        caption_links = extract_markdown_links(node_text)
        if not caption_links:
            new_nodes.append(node)
            continue

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
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        caption_images = extract_markdown_images(node_text)
        if not caption_images:
            new_nodes.append(node)
            continue

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
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes,"`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):

    split_parts = markdown.split("\n\n")
    parts = [part.strip() for part in split_parts if part.strip()]

    return parts
        
def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"#{1,6} ", lines[0]):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">" )for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    ordered = True
    for i in range(len(lines)):
        exp_prefix = f"{i+1}. "
        if not lines[i].startswith(exp_prefix):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):  # Meat of the generator
    block_list = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", children=[])

    for block in block_list:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            lvl_of_heading = block.count("#", 0, block.find(" "))
            #idx_cut = block.find(" :")
            raw_string = block.lstrip("#").strip()
            children = text_to_children(raw_string)
            node = ParentNode(f"h{lvl_of_heading}", children=children)

        elif block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            cleaned_block = " ".join(line.strip() for line in lines) 
            children = text_to_children(cleaned_block)
            node = ParentNode("p", children=children)

        elif block_type == BlockType.CODE:
            raw_block = block.strip()
            lines = raw_block.split("\n")

            code_lines = lines[1:-1]

            cleaned_lines = [line.rstrip() for line in code_lines]

            content = textwrap.dedent("\n".join(cleaned_lines)).rstrip()

            text_node = TextNode(content, TextType.TEXT)
            code_leaf = text_node_to_html_node(text_node)
            code_node = ParentNode("code", children=[code_leaf])
            node = ParentNode("pre", children=[code_node])

        elif block_type == BlockType.QUOTE:
            final_text = ""
            for line in block.split("\n"):
                clean_line = line[1:].strip()
                final_text += clean_line + "\n"
            final_text = final_text.strip()
            children = text_to_children(final_text)
            node = ParentNode("blockquote", children=children)
        
        elif block_type == BlockType.UNORDERED_LIST:
            li_parts = []
            for line in block.split("\n"):
                content = line[2:].strip()
                children = text_to_children(content)
                li_parts.append(ParentNode("li", children=children))
            node = ParentNode("ul", children=li_parts)

        elif block_type == BlockType.ORDERED_LIST:
            li_parts = []
            for line in block.split("\n"):
                dot_space_idx = line.find(". ")
                content = line[dot_space_idx +2:].strip()
                children = text_to_children(content)
                li_parts.append(ParentNode("li", children=children))
            node = ParentNode("ol", children=li_parts)

        else:
            children = text_to_children(block)
            node= HTMLNode("p", children=children)

        parent_node.children.append(node)
    return parent_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_list = []
    for node in text_nodes:
        html_list.append(text_node_to_html_node(node))
    return html_list
