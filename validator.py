text = '''<synset id="r00001740" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">a cappella
         <def>without musical accompaniment
         <example>they performed a cappella</example>
      </synset>'''


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

    for i in range(len(text)):
        temp = ""
        temp2 = ""
        compare = ""
        j = i + 1
        k = i + 2
        flag = 0

        if text[i] == '<' and text[i + 1] != '/':  # storing opening tags
            temp += text[i]
            # stack.append(text[i])
            while text[j] != '>' and text[j] != ' ':  # and text[j] != '?' and text[j] != '!':
                temp += text[j]
                j += 1
            if text[j] == '>' or text[j] == ' ' or text[j] != '/':  # we reached the end of the tag
                temp += '>'
                if text[j - 1] != '/':  # if it is a self closing tag don't put in stack
                    stack.append(temp)

        if text[i] == '<' and text[i + 1] == '/':  # stroing closing tag'
            temp2 += text[i]
            # temp2 += text[i+1]
            while text[k] != '>' and text[k] != ' ':  # and text[k] != '?' and text[k] != '!':
                temp2 += text[k]
                k += 1
            if text[k] == '>' or text[k] == ' ':
                temp2 += '>'
                stack2.append(temp2)
                compare = stack[-1]
                # print(stack, compare)
                # print(temp2)
                if compare == temp2:
                    stack.pop()
                    stack2.pop()
                # elif compare != temp2:  #missing closing tag so stack at the end not zero
                # print("compare(s-1): ", compare)
                # print("temp2:", temp2)

    # print("stack2:", stack2)
    return stack


def fix_closing(s, txt):  # missing closing tag so stack at the end not zero
    op_tag = s[-1]
    cl_tag = op_tag[:1] + '/' + op_tag[1:]
    new_txt = ""
    holder = ""
    for i in range(len(text)):
        temp = ""
        j = i + 1
        if txt[i] == '<' and txt[i + 1] != '/':  # searching for opening tags only
            temp += text[i]
            while text[j] != '>' and txt[j] != ' ':
                temp += txt[j]
                j += 1
            if txt[j] == '>' or txt[j] == ' ' or txt[j] != '/':  # we finished the tag
                temp += '>'
            if temp == op_tag:
                holder = temp

        if holder == op_tag:  # if we found our opening tag
            if txt[i + 1] == '<':  # skip to the next tag(closing or opening)
                new_text = txt[:i + 1] + cl_tag + txt[i + 1:]
                return new_text


# def fix_opening( , txt):


x = error2(text)

y = fix_closing(x, text)

# print(y)

# print(scrape_data(text))


# my = ["ssssssss", "skljaslkajs", "hhhhhhhhh"]
