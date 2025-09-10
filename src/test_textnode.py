import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("this is another text not", TextType.ITALIC)
        #self.assertEqual(node, node3)
        node4 = TextNode("This is a text node", TextType.BOLD, None)

        node5 = TextNode("This is a text node", TextType.ITALIC, None)

        self.assertNotEqual(node2, node3)

        self.assertEqual(node, node4)

        self.assertNotEqual(node, node5)

if __name__ == "__main__":
    unittest.main()
