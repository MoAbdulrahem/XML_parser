from enum import Enum
import re

class Tag(Enum):
    CLOSING_TAG = 1
    DATA = 2
    OPENING_TAG_WITH_METADATA = 3
    OPENING_TAG = 4

def get_element_type(tag):
    tag = tag.strip()

    if re.match(r'</.*>', tag):
        return Tag.CLOSING_TAG
    elif re.match(r'<[A-Za-z0-9]*( [A-Za-z0-9:_]* ?= ?("?[A-Za-z0-9\\/._]"?)*)+>', tag):
        return Tag.OPENING_TAG_WITH_METADATA
    elif re.match(r'<.*>', tag):
        return Tag.OPENING_TAG
    else:
        return Tag.DATA

def parse_tag(tag):
    element_type = get_element_type(tag)
    if element_type == Tag.OPENING_TAG_WITH_METADATA:
        tag_type = re.search(r'<([A-Za-z0-9_]*)',tag).group(1)
        metadata_list = re.findall(r'(([A-Za-z0-9:_]+) ?= ?("?[A-Za-z0-9\\/._]+"?))',tag,re.DOTALL)
        metadata = [(md[1], md[2]) for md in metadata_list]
        return tag_type, metadata
    elif element_type == Tag.OPENING_TAG:
        tag_type = re.search(r'<([A-Za-z0-9_]*)',tag).group(1)
        return tag_type, None
    elif element_type == Tag.CLOSING_TAG:
        tag_type = re.search(r'</([A-Za-z0-9_]*)',tag).group(1)
        return tag_type, None
    else:
        return None, None

def json_write_field(tag_type, current_json):
    return current_json + tag_type + ":"

def json_write_bracket_or_qoutation(tags, current_position, current_json):
    next_tag = tags[current_position+1]
    element_type = get_element_type(next_tag)
    if element_type == Tag.OPENING_TAG:
        current_json = current_json + "\'\'"
    elif element_type == Tag.CLOSING_TAG or element_type == Tag.OPENING_TAG_WITH_METADATA:
        current_json = current_json + "{"
    elif element_type == Tag.DATA:
        if get_element_type(tags[current_position+2]) == Tag.OPENING_TAG_WITH_METADATA:
            current_json = current_json + "{"
        else:
            current_json = current_json + "\""
    return current_json

def json_write_data(data, current_json):
    if current_json[-1] == "\"":
        return current_json + data + "\", "
    else:
        return current_json+ "_text:"  + data 

def json_write_metadata(metadata, current_json):
    if not current_json[-1] == '{':
        current_json+= ','
    for md in metadata:
        current_json += f"_{md[0]}:{md[1]}, "
    return current_json+ "}"

# tags = scrape_data(sample)
# tags = ['<data version="3.0">', '<synsets source="dict/data.adv" xml:base="data.adv.xml">',
#         '<synset id="r00001740" type="r">', '<lex_filenum>', '02', '</lex_filenum>',
#         '<word lex_id="0">', 'a cappella', '</word>', '<def>', 'without musical accompaniment',
#         '</def>', '<example>', 'they performed a cappella', '</example>', '</synset>',
#         '<synset id="r00261389" type="r">', '<lex_filenum>', '02', '</lex_filenum>',
#         '<word lex_id="0">', 'agonizingly', '</word>', '<word lex_id="0">', 'excruciatingly',
#         '</word>', '<word lex_id="0">', 'torturously', '</word>', '<pointer refs="a01711724" source="3" target="6">',
#         'Derived from adjective', '</pointer>', '<pointer refs="a01711724" source="2" target="3">',
#         'Derived from adjective', '</pointer>', '<pointer refs="a01711724" source="1" target="1">',
#         'Derived from adjective', '</pointer>', '<def>', 'in a very painful manner', '</def>', '<example>',
#         'the progress was agonizingly slow', '</example>', '</synset>', '<synset id="r00423888" type="r">',
#         '<lex_filenum>', '02', '</lex_filenum>', '<word lex_id="0">', 'rallentando', '</word>', '<pointer refs="n07020895">',
#         'Domain of synset - TOPIC', '</pointer>', '<def>', 'slowing down', '</def>', '<example>',
#         'this passage should be played rallentando', '</example>', '</synset>', '<synset id="r00471945" type="r">',
#         '<lex_filenum>', '02', '</lex_filenum>', '<word lex_id="0">', 'surpassingly', '</word>',
#         '<pointer refs="a01676026" source="1" target="5">', 'Derived from adjective', '</pointer>', '<def>',
#         'to a surpassing degree', '</def>', '<example>', 'she was a surpassingly beautiful woman',
#         '</example>', '</synset>', '</synsets>', '</data>']
# tags = ['<h1 font=13>', '<dev>', 'asfdaf', '</dev>', '</h1>']
def jsonify(tags):
    tags = tags[::-1]  #invert the list

    current_json = "{"

    for i, tag in enumerate(tags):
        element_type = get_element_type(tag)
        tag_type, metadata = parse_tag(tag)
        # if tag_type == "pointer":
        #     print(element_type, tag_type, metadata)
        if element_type == Tag.CLOSING_TAG:
            if current_json[-1] == "}":
                current_json+= ','
            current_json = json_write_field(tag_type, current_json)
            current_position = i
            current_json = json_write_bracket_or_qoutation(tags, current_position, current_json)
        elif element_type == Tag.DATA:
            current_json = json_write_data(tag, current_json)
        elif element_type == Tag.OPENING_TAG_WITH_METADATA:
            current_json = json_write_metadata(metadata, current_json)
        else:

            current_json = current_json + "}"
    # print(current_json)
    return current_json

# test_json = (jsonify(tags))