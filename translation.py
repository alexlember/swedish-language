import os
import re
from collections import OrderedDict

target_file = './swedish-english-similar.md'
new_file_input = './new_input.txt'
output_directory = "./results/"
output_file = output_directory + "output.md"

default_word_form_pattern = r"default: ([^,]+)"


def extract_default_form(input_str):
    match = re.search(default_word_form_pattern, input_str)
    if match:
        default_value = match.group(1).strip()
    else:
        print("Key 'default' not found in the input string.")
        default_value = None
    return default_value


def open_file(name, strip_number):
    try:
        with open(name, 'r') as file:
            # Read lines from the file and create a set with no number in the beginning

            if strip_number:
                content_set = {line.strip().split(') ', 1)[1] for line in file.readlines()}
            else:
                content_set = {line.strip() for line in file.readlines()}
        print("File content loaded into the set successfully.")
        print("Set content:", content_set)
        return content_set

    except FileNotFoundError:
        print(f"The file '{name}' was not found.")
    except Exception as e:
        print("An error occurred:", str(e))


def default_word_to_line_map(word_set):
    default_word_map = {}
    for word in word_set:
        match = re.search(default_word_form_pattern, word)

        # Check if a match is found
        if match:
            default_value = match.group(1).strip()
            default_word_map[default_value] = word
            print("Value associated with the key 'default':", default_value)
        else:
            print("Key 'default' not found in the input string.")
    return default_word_map


target_set = open_file(target_file, True)
input_set = open_file(new_file_input, False)

default_target_map = default_word_to_line_map(target_set)
default_input_map = default_word_to_line_map(input_set)

for default_word in default_input_map:
    if default_word not in default_target_map:
        default_target_map[default_word] = default_input_map[default_word]


myKeys = sorted(default_target_map.keys())
sorted_dict = {i: default_target_map[i] for i in myKeys}

updated_list = [f"{index + 1}. {item}" for index, item in enumerate(sorted_dict.values())]

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(output_file, "w") as file:
    for item in updated_list:
        file.write(item + "\n")
