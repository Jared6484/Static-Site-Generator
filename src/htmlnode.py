class HTMLNode:
    def __init__(self, tag= None, value= None, children= None, props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_str = ""
        for k, v in self.props.items():
            prop_str += f' {k}="{v}"'
        return prop_str

    def __repr__(self):
        return f'HTML Node : tag is {self.tag}, value is {self.value}, children are {self.children}, props are {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.value = value
        self.tag = tag
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            props_str =""
            if self.props:
                props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'

    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("a tag needs to be given")
        if self.children is None:
            raise ValueError("child or children need to be given")

        children_html = ""
        for child in self.children:
            child_html = child.to_html()
            if child_html is None:
                continue
                #raise ValueError("child returned None from to_html()")          
            children_html += child_html


        props_str = ""
        if self.props:
            props_str = self.props_to_html()

        return f'<{self.tag}{props_str}>{children_html}</{self.tag}>'

        
