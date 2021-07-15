# This file contains two functions: scrape_data(text) and prettify_data(tags)
# scrape_data(text) should be assigned the XML file at the beggining of execution, it returns a list of tags that should be used during the rest of the runtime
# prettify_data(tags) takes a list of tags (like the one outputted by scrape_data()) then it reorganizes and displays the data with indentations corrosponding to its tag level

from minify import Minify

temp_dir= 'data-sample.xml'
# text= Minify(temp_dir)
# dummy input
text = '''<synset id="r00001740" type="r"> 
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">a cappella</word>
         <def>without musical accompaniment</def>
         <example>they performed a cappella</example>
      </synset>''' 

# Scraping the tags out of the XML document 
def scrape_data(text):
    '''
    Takes the XML file as a string and scrapes the data from it into a list.
    Returns a list of tags and their values.
    '''
    text = text.replace("   ","")
    text = text.replace("\n","")
    tags = []
    for i in range(len(text)):
        j = i+1     #used as an index to get the tag name
        k = i+1     #used as an index to get the tag value
        temp  = ""
        temp2 = "" 
        if text[i] == '<': #an openning tag
            temp += text[i]
            try:
                while text[j] != '>' and text[j] != '!': #loop until '>' or " " to get the tag name
                    temp += text[j]     #concatenate the tag name to temp
                    j += 1

                if text[i]== '>' or text[i] == ' ' or text[j] != '/': #we reached the end of the tag
                    temp += '>'
                    tags.append(temp)
                    if tags[-1] == "<>": # check if there were empty tags and remove them 
                        tags.pop()
            except:
                pass
        elif text[i] == ">": # this part is to get the vlaue of the tag (i.e. <tag>value</tag>)
            if i == len(text)-1:    #we reached the end of the text
                break
            while text[k] != '<':
                if k == len(text)-1:    #we reached the end of the text
                    break
                temp2 += text[k]
                k+=1
            tags.append(temp2)
            if tags[-1] == " " or tags[-1] == '':   #make sure we didn't get empty spaces as elements
                tags.pop()
    # print(tags)
    return tags

#prettifying and printing the tree
def prettify_data(tags):
    '''
    Takes the list of tages that was outputted by scrape_data(), reorganizes it, then displays it in a proper order
    '''
    powers = []     #each tag in tags will have a corrosponding power that descripes its location in the hierarchical tree
    level = -1      #start at -1 so that the root would be level 0
    new_text = ""   #contains the new layout of the XML document
    for tag in tags:
        if tag[0] == "<" and tag[1] != "/":
            level+= 1
            powers.append(level)
        elif tag[0] == "<" and tag[1] == "/":
            powers.append(level)
            level-= 1
        else:
            powers.append(level)

    for i in range(len(tags)):
        indentation = ' '*5*powers[i]
        new_text += indentation + tags[i] +'\n'
    return new_text

# print(prettify_data(scrape_data(text)))

#Converting the XML file into a tree
# Definning the tree
# class Node:
#     def __init__(self,data):
#         self.data = data
#         self.children = []
#         self.parent = None
    
#     def add_child(self,child):
#         child.parent = self
#         self.children.append(child)
        