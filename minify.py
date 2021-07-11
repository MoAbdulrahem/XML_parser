# THIS FILE SHOULD BE MODIFIED TO TAKE THE XML FILE INSTEAD OF THE DIRECTORY AFTER THE GUI DESIGN IS DONE

#Minifying The XML File (by removing the new lines and some of the white spaces)
def Minify(contents):
    '''
    Takes the XML file as an argument, and removes new lines and each two or more successive spaces
    '''
    contents = contents.replace("   ","")
    contents = contents.replace("\n","")
    return contents
