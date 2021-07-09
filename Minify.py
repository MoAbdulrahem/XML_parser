#Minifying The XML File (by removing the new lines and some of the white spaces)
def Minify(file_directory):
    '''
    Takes the XML file as an argument, and removes new lines and each two or more successive spaces
    '''
    with open(file_directory,'r') as f:
        contents = f.read()
    contents = contents.replace("   ","")
    contents = contents.replace("\n","")
    return contents
