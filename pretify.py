from Minify import Minify

# temp_dir= 'data-sample.xml'
# x= Minify(temp_dir)
# print(x)

# Converting the XML file into a tree
# Definning the tree
class Node:
    def __init__(self,data):
        self.data = data
        self.children = []
        self.parent = None
        