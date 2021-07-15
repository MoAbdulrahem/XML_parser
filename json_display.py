

def display_json(json_string):
    '''
    takes the json string generatied by the jsonify function then
    pretty prints it
    '''
    json_string = json_string.replace(', ',' ')
    level = 0
    spaces = ' '*4*level
    display = ""
    temp_tag = ""
    temp_value = ""
    openning_brackets = 0
    closing_brackets = 0
    i = 0
#     for i in range(len(json_string)):
    while i < len(json_string)-1:
        spaces = ' '*4*level
        if json_string[i] == '{':
#             print(spaces + json_string[i])
            display = display +  spaces + json_string[i]+ '\n'
            openning_brackets +=1 
            level += 1
            i += 1
        elif json_string[i] == '}':
            if closing_brackets > openning_brackets:
                i += 1
                continue
            else:
                closing_brackets += 1
#                 print(spaces + json_string[i],)
                display = display +  spaces + json_string[i]+ '\n'
                level -= 1
                if level < 1:
                    level = 2
                i += 1
        else:
            if json_string[i] != ':':
                temp_tag += json_string[i]
                i += 1
            elif json_string[i] == ':'or json_string[i] == ',':
                
                i += 1
                if json_string[i] != '{':
                    temp_value += json_string[i]
                    i += 1
                    while True:
                        if json_string[i] == ',' or json_string[i] == '}':
                            break
                        temp_value += json_string[i]
                        i += 1
#                 print (spaces  + temp_tag + ':'+temp_value,),
                display = display +  spaces + '"' +temp_tag + '"' +':'+temp_value + '\n'
                temp_tag = ""
                temp_value = ""
                
    if display.endswith('{'):
        pass
    else:
        display += '\n}'
    display = display.replace(',','')
    return display

if __name__ == "__main__":

    # temp_print = display_json(test_json.replace(', ',' ').replace(',',''))
    # print(temp_print)