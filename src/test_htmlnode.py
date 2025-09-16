import unittest

from textnode import TextNode, TextType, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import (text_node_to_html_node, split_nodes_delimeter, 
                        split_nodes_link,split_nodes_images, text_to_textnodes,
                        markdown_to_blocks, block_to_block_type, markdown_to_html_node)

class TestHTMLNode(unittest.TestCase):

    def test_instance_creation(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "blank"})
        #print(self.__repr__())
        self.assertIsInstance(node, HTMLNode)

    def test_props_to_html(self):

        node = HTMLNode(props={"href": "https://www.google.com", "target": "blank"})
        html = node.props_to_html()
        #print(f' HTTTTTML {html}')
        expected = ' href="https://www.google.com" target="blank"'
        self.assertEqual(html, expected)

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        self.assertIsInstance(node, HTMLNode)

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        nod2_html = node2.to_html()
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(nod2_html, expected2)

        node3 = LeafNode(value="Text with no tag")
        no_tag_text = node3.to_html()
        expected3 = "Text with no tag"
        self.assertEqual(no_tag_text, expected3)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_deeply_nested_parents(self):
        leaf = LeafNode("em", "deep")
        level3 = ParentNode("p", [leaf])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(),
            "<div><section><p><em>deep</em></p></section></div>"
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})        

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "An image"})

    def test_split_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode(" word", TextType.TEXT),
                                        ])
        
        node = TextNode("This is text with a _italics block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ITALIC)
        #print(f'NEWWWWW NODES {new_nodes}')
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("italics block", TextType.ITALIC),
                                        TextNode(" word", TextType.TEXT),
                                        ])
        
    def text_extract_markdown_images(self):
        matches = extract_markdown_images(            
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches2 = extract_markdown_links(            
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches2)

    def test_split_links(self):
        node = [TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
         ], 
         new_nodes)
 
        node1 = [TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).With some extra text",
        TextType.TEXT,
        )]
        new_nodes1 = split_nodes_link(node1)
        self.assertListEqual([
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(".With some extra text", TextType.TEXT)
            ,
        ], new_nodes1)

        node2 = [TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )]
        new_nodes2 = split_nodes_link(node2)
        self.assertListEqual([
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ], new_nodes2)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,)

        node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)
        new_nodes2 = split_nodes_images([node2])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes2,)

        '''node3 = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,), TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)]
        new_nodes3 = split_nodes_images([node3])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes3,)'''

    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word "
        "and a `code block` and an ![obi wan image]"
        "(https://i.imgur.com/fJRm4Vk.jpeg) and "
        "a [link](https://boot.dev)")

        nodes = text_to_textnodes(text)

        self.assertListEqual([
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
            ], nodes)

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
        
    def test_heading_block(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        assert result == BlockType.HEADING, f"Expected HEADING, got {result}"

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        assert result == BlockType.ORDERED_LIST, f"Expected ORDERED_LIST, got {result}"

    def test_paragraph_block(self):
        block = "This is just a normal paragraph of text without any special formatting."
        result = block_to_block_type(block)
        assert result == BlockType.PARAGRAPH, f"Expected PARAGRAPH, got {result}"

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

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain 
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",html
        )

if __name__ == "__main__":
    unittest.main()
