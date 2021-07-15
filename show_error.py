text = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- A random selection of elements from data.xml
     Some IDREFS (refs attribute of element pointer) do not have a corresponding id in this sample-->
<?xml-model href="data.rnc" type="application/relax-ng-compact-syntax"?>
<data version="3.0"> 
   <synsets source="dict/data.adv" xml:base="data.adv.xml">

      <synset id="r00001740" type="r">
         02</lex_filenum>
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
</data>
'''



def show_error(text):
    stack = []
    stack2 = []

    stack_error_loc = []
    #stack_error_loc2 = []

    final = []
    #final2 = []

    has_children = []
    true = "true"
    false = "false"

    for i in range(len(text)):
        temp = ""
        temp2 = ""
        temp_error_loc = 0
        #temp_error_loc2 = 0
        compare = ""
        j = i + 1
        if j > len(text) - 1:
            break
        k = i + 2
        if k > len(text) - 1:
            break
        flag = 0

        if text[i] == '<' and text[i+1] != '/' and text[i+1] != '!' and text[i+1] != '?':    # storing opening tags
            temp += text[i]  # put <
            temp_error_loc = i
            while text[j] != '>' and text[j] != ' ':  # and text[j] != '?' and text[j] != '!':
                temp += text[j]
                j += 1
            if text[j] == '>' or text[j] == ' ' or text[j] != '/':  # we reached the end of the op tag
                temp += '>'
                if text[j-1] != '/':  # if it is a self closing tag don't put in stack
                    stack.append(temp)
                    stack_error_loc.append(temp_error_loc)
                    ch = j
                    while text[ch] != '>':
                        ch += 1

                    if text[ch+1] != '\n':
                        has_children.append(false)
                    elif text[ch + 1] == '\n':
                        has_children.append(true)

        if text[i] == '<' and text[i + 1] == '/':   #stroing closing tag'
            temp2 += text[i]
            #temp_error_loc2 = i
            # temp2 += text[i+1]
            while text[k] != '>' and text[k] != ' ':  #and text[k] != '?' and text[k] != '!':
                temp2 += text[k]
                k += 1
            if text[k] == '>' or text[k] == ' ':  # closing tag ended
                temp2 += '>'
                stack2.append(temp2)  # store the closing tag to stack2

                if len(stack) == 0:
                    continue
                #print(stack, stack2)
                compare = stack[-1]   # compare the closing with the opening
                #print(has_children)
                if compare == temp2:
                #if stack[-1] == stack2[-1]:
                    stack.pop()
                    stack2.pop()
                    has_children.pop()
                    stack_error_loc.pop()
                elif compare != temp2:
                #elif stack[-1] != stack2[-1]:  #missing closing tag so add a closing tag

                    if has_children[-1] == "true":      #FIX FOR TAGS WITH CHILDREN

                        stack.pop()
                        stack2.pop()
                        final.append(stack_error_loc[-1])
                        stack_error_loc.pop()

                        has_children.pop()
                        #print("done")
                    elif has_children[-1] == "false":    #FIX FOR MISS CL TAGS WITHOUT CHILDREN
                        stack.pop()
                        #print(has_children)
                        has_children.pop()
                        final.append(stack_error_loc[-1])

                        stack_error_loc.pop()

                        stack2.pop()
                        #print("done2")









    # print("stack2:", stack2)

    #print(stack_error_loc)
    #print(stack)
    #print(stack2)
    #while len(stack) != 0:                              #fix last closing tag miss corner case\
    #    error2(text, stack, has_children, stack_error_loc, final)
    #    indent = len(stack) - 1
    #    text = text + '\n' + indent*'\t' + stack[-1][:1] + '/' + stack[-1][1:]
    #    stack.pop()

    #print(stack)
    return final


#x = show_error(text)

#print(x)