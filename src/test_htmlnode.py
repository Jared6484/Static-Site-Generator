import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()
