TRANSLATION_FILE = "C:/git/AliceWonderland/game/script.rpy"

import re
# line number where new translatins were appened

def update_translation_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []    
    for i in range(len(lines)):

        # find the first line with translate
        match = re.match(r'^\s{4}\w+\s\"', lines[i])
        if lines[i].startswith("    \""): output_lines.append(lines[i].strip() + "\n")
        elif lines[i].startswith("    ") and match: output_lines.append(lines[i].strip() + "\n")

    # clean up some exceptions: remove all lines that start with voice:
    output_lines = [line for line in output_lines if not line.startswith("voice")]

    # for each string, remove curly braces and the text inside them
    output_lines = [re.sub(r'\{.*?\}', '', line) for line in output_lines]

    # also remove special characters like \n
    output_lines = [re.sub(r'\\n', '', line) for line in output_lines]

    # Write the updated lines back to the file
    with open(file_path+"_simple.txt", 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

# Use the function
update_translation_file(TRANSLATION_FILE)
