# Creating a tree out of the xml document 

class TreeNode:
    def __init__(self,data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self,child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        # spaces = ' ' * self.get_level() * 4
        print(self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

    # def get_level(self):
    #     level = 0
    #     p = self.parent
    #     while p:
    #         level += 1
    #         p = self.parent

        # return level

def get_tag_name(tag):
    tag_name = ""
    for i in tag:
        pass


def build_XML_tree(tags):
    for i in range(len(tags)):
        node = TreeNode(tags[i])
        if node.parent == None:
            root = node
            continue
        else:
            child = node

        if tags[i][0] == '<' and tags[i][1] != '/':
            root.add_child(child)
        elif tags[i][0] == '<' and tags[i][1] == '/':
            pass
        else:
            root.children[i-1].add_child(TreeNode(tags[i]))
        print('node = ' , child.data , '\nparent  =', child.parent)

            
    # first_child = TreeNode("First Child")
    # root.add_child(first_child)
    return root


if __name__ == "__main__":
    tags = ['<tag1>','<tag2>', 'value','</tag2>' , '</tag1>']
    root = build_XML_tree(tags)
    
    root.print_tree()
    print('\n\n\n')
    for child in root.children:
        print(child.data)