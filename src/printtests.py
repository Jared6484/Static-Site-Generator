from textnode import TextNode, TextType,BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import (text_node_to_html_node, split_nodes_delimeter, 
                        split_nodes_link, split_nodes_images, 
                        text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node)

def test_split_links():
    '''node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
    new_nodes = split_nodes_link(node)
    expected = [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]'''
    '''node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).With some extra text",
    TextType.TEXT,
    )
    new_nodes = split_nodes_link(node)
    expected = [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(".With some extra text", TextType.TEXT)
            ,
        ]'''

    '''node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
    new_nodes = split_nodes_link(node)
    expected = [
    TextNode("This is text with a link ", TextType.TEXT),
    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    ]'''

    '''node1 = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,)
    new_nodes = split_nodes_images(node1)
    expected = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
    ]'''
'''
def test_text_to_textnodes():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    nodes = text_to_textnodes(text)

    expected =[
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
        ]'''
'''   
def test_markdown_to_blocks():
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
    
    print("Expected:")
    for node in expected:
        print("", node)

    print("Actual:")
    #for node in blocks:
    print("", blocks)

    print("Match:", blocks == expected)
'''
'''
def test_paragraphs_manual():
    md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

    node = markdown_to_html_node(md)
    html = node.to_html()

    expected_html = (
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
        "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
    )

    print("Expected:")
    print(expected_html)
    print("\nActual:")
    print(html)

    print("\nMatch:", html == expected_html)
'''
def test_code_manual():
    md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
    node = markdown_to_html_node(md)
    html = node.to_html()

    expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"

    print("Expected:")
    print(expected)
    print("\nActual:")
    print(html)
    print("\nMatch:", html == expected)

if __name__ == "__main__":
    test_code_manual()