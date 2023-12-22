import re

# change working directory to the directory of this file
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def is_sentence_end(line):
    # Check if a line ends with a sentence-ending punctuation mark
    return line.strip().endswith(('.', '?', '!'))

def process_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as input_f:
        lines = input_f.readlines()

    new_lines = []

    # Initialize a flag to keep track of whether the previous line was empty
    prev_line_empty = False

    for line in lines:
        if not line.strip():
            # If the line is empty, set the flag to True
            prev_line_empty = True
        else:
            if is_sentence_end(line):
                # If the line ends with a sentence-ending punctuation mark, add a newline
                new_lines.append(line.strip() + '\n')
                prev_line_empty = False
            else:
                # If the line does not end with a sentence-ending punctuation mark
                # and the previous line was not empty, add it to the previous line
                if not prev_line_empty:
                    new_lines[-1] += ' ' + line.strip()
                else:
                    new_lines.append(line.strip())
                prev_line_empty = False

    with open(output_file, 'w', encoding='utf-8') as output_f:
        output_f.write('\n'.join(new_lines))

if __name__ == "__main__":
    input_file = "raw.txt"  # Replace with the path to your input file
    output_file = "pretty.txt"  # Replace with the desired output file path
    process_text_file(input_file, output_file)
