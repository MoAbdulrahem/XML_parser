text = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- A random selection of elements from data.xml
     Some IDREFS (refs attribute of element pointer) do not have a corresponding id in this sample-->
<?xml-model href="data.rnc" type="application/relax-ng-compact-syntax"?>
<data version="3.0"> 
   <synsets source="dict/data.adv" xml:base="data.adv.xml"><!--10 out of 3621 elements-->
    <synset id="r00001740" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">a cappella</word>
         <def>without musical accompaniment</def>
         <example>they performed a cappella</example>
      </synset>
      <synset id="r00261389" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">agonizingly</word>
         <word lex_id="0">excruciatingly</word>
         <word lex_id="0">torturously</word>
         <pointer refs="a01711724" source="3" target="6">Derived from adjective</pointer>
         <pointer refs="a01711724" source="2" target="3">Derived from adjective</pointer>
         <pointer refs="a01711724" source="1" target="1">Derived from adjective</pointer>
         <def>in a very painful manner</def>
         <example>the progress was agonizingly slow</example>
      </synset>
      <synset id="r00423888" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">rallentando</word>
         <pointer refs="n07020895">Domain of synset - TOPIC</pointer>
         <def>slowing down</def>
         <example>this passage should be played rallentando</example>
      </synset>
      <synset id="r00471945" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">surpassingly</word>
         <pointer refs="a01676026" source="1" target="5">Derived from adjective</pointer>
         <def>to a surpassing degree</def>
         <example>she was a surpassingly beautiful woman</example>
      </synset>
   </synsets>
</data>'''






def error(text):
    stack = []
    for i in range(len(text)):
        if text[i] == '<':
            stack.append(text[i])

        if text[i] == '>':
            x = stack[-1]
            stack.pop()
            if x != '<':
                return False
            break

    return len(stack)


def error2(text):
    stack = []
    stack2 = []
    has_children = []
    true = "true"
    false = "false"

    for i in range(len(text)):
        temp = ""
        temp2 = ""
        compare = ""
        j = i + 1
        if j > len(text)-1:
            break
        k = i + 2
        if k > len(text)-1:
            break
        flag = 0

        if text[i] == '<' and text[i+1] != '/':    # storing opening tags
            temp += text[i]  # put <

            while text[j] != '>' and text[j] != ' ':  # and text[j] != '?' and text[j] != '!':
                temp += text[j]
                j += 1
            if text[j] == '>' or text[j] == ' ' or text[j] != '/':  # we reached the end of the op tag
                temp += '>'
                if text[j-1] != '/':  # if it is a self closing tag don't put in stack
                    stack.append(temp)
                    if text[j+1] != '\n':
                        has_children.append(false)
                    else:
                        has_children.append(true)

        if text[i] == '<' and text[i + 1] == '/':   #stroing closing tag'
            temp2 += text[i]
            # temp2 += text[i+1]
            while text[k] != '>' and text[k] != ' ':  #and text[k] != '?' and text[k] != '!':
                temp2 += text[k]
                k += 1
            if text[k] == '>' or text[k] == ' ':  # closing tag ended
                temp2 += '>'
                stack2.append(temp2)  # store the closing tag to stack2


                compare = stack[-1]   # compare the closing with the opening
                # print(stack, compare)
                # print(temp2)
                if compare == temp2:
                    stack.pop()
                    stack2.pop()
                    has_children.pop()
                elif compare != temp2:  #missing closing tag so add a closing tag
                    temp2_cl_tag = compare[:1] + '/' + compare[1:]
                    if has_children[-1] == "true":
                        text = text[:i] + temp2_cl_tag + '\n' + text[i:]
                        stack.pop()
                        stack2.pop()
                        has_children.pop()
                    elif has_children[-1] == "false":
                        text = fix_closing(stack, text)
                        has_children.pop()





    # print("stack2:", stack2)
    return text

def fix_closing(s, txt):        #missing closing tag so stack at the end not zero
    op_tag = s[-1]
    cl_tag = op_tag[:1] + '/' + op_tag[1:]
    new_txt = ""
    holder = ""
    for i in range(len(txt)):
        temp = ""
        j = i + 1
        if j > len(txt) - 1:
            break
        if txt[i] == '<' and txt[i + 1] != '/':     #searching for opening tags only
            temp += txt[i]
            while txt[j] != '>' and txt[j] != ' ':
                temp += txt[j]
                j += 1
            if txt[j] == '>' or txt[j] == ' ' or txt[j] != '/':     #we finished the tag
                temp += '>'
            if temp == op_tag:
                holder = temp

        if holder == op_tag:                             #if we found our opening tag
            if txt[i+1] == '<':                         #skip to the next tag(closing or opening)
                new_text = txt[:i+1] + cl_tag + '\n' + txt[i+1:]
                s.pop()
                return new_text



test = '''
<synset id="r00001740" type="r"> 
        <lex_filenum>02</lex_filenum>
        <word lex_id="0">a cappella
        <def>without musical accompaniment
        <example>they performed a cappella</example>
</synset>
'''











#print(scrape_data(text))


# my = ["ssssssss", "skljaslkajs", "hhhhhhhhh"]