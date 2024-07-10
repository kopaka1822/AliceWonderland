import os
from openai import OpenAI
from prompt_toolkit import prompt # pip install prompt_toolkit
import sys

# Load API key from environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# File path and start line
file_path = "game/tl/german/script.rpy"
start_line = 7422

history = [
    {"role": "system", "content": "Translate the following English text from alice in wonderland into German. Use vocabulary and grammar that is common in today's German language and suitable for a 10 year old native speaker. Split very long sentences into smaller sentences. The input format from the user will be <sayer>: <quote>. Only output the translation of the quote. If the sayer is alice, translate it in a way that would be common for a 10 year old German in 2020 and use German teenage slang without making it cringe. If the user input starts with 'instruct:' edit the previous user translation as requested. After the translation the user will supply its accepted translation. Please make sure to stay consistent with the user edits for future translations"}
]

def ask_AI(prompt):
    try:
        history.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        respone = completion.choices[0].message.content
        history.append({"role": "assistant", "content": respone})
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None

def read_lines_from_file():
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

def write_line_to_file(line_number, new_line):
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        lines[line_number] = new_line
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    return lines

def replace_last(s, old, new):
    s_reversed = s[::-1]
    s_reversed_replaced = s_reversed.replace(old[::-1], new[::-1], 1)
    s_replaced = s_reversed_replaced[::-1]
    return s_replaced

def process_lines():
    lines = read_lines_from_file()
    i = max(start_line - 1, 0)
    last_comment = ""

    while i < len(lines):
        line = lines[i]
        i += 1
        stripped_line = line.strip()

        if stripped_line.startswith('#'):
            last_comment = stripped_line
            continue
        if stripped_line.startswith("translate") or stripped_line.startswith("\"{size=+40}Chapter"):
            continue

        parts = stripped_line.split('"', 1)
        if len(parts) < 2:
            continue

        sayer = parts[0].strip()
        # if sayer is empty, its the narrator
        if len(sayer) == 0:
            sayer = "narrator"

        quote = parts[1][0:-1]
        brackets = False
        if quote.startswith("(") and quote.endswith(")"):
            brackets = True
            quote = quote[1:-1]

        os.system('cls')
        console_input = ""
        print(last_comment)
        print(f"Original line {i}/{len(lines) + 1} ({round(i / len(lines) * 100.0, 2)}%): {stripped_line}")
        print("Enter to skip.\ng to generate with OpenAI\nm modify\np to pass line\nb to go back\nAny other text to replace:")

        while True:
            user_input = prompt("> ", default=console_input).strip()

            if user_input == "g":
                console_input = ask_AI(f"{sayer}: {quote}")
            elif user_input == "m":
                intruction = prompt("> ", default="").strip()
                console_input = ask_AI(f"instruct: {intruction}")
            elif user_input == "c":
                console_input = quote
            elif user_input == "p":
                white_spaces = len(line) - len(line.lstrip())
                lines = write_line_to_file(i - 1, " " * white_spaces + "pass\n")
                user_input = None
                break
            elif user_input == "b":
                i -= 8
                user_input = None
                break
            else:
                break

        if user_input:
            if brackets and user_input.endswith("."):
                user_input = user_input[:-1]
            if brackets and user_input.startswith("(") and user_input.endswith(")"):
                user_input = user_input[1:-1]
            user_input = user_input.replace('"', "'")

            history.append({"role": "user", "content": f"{sayer}: {user_input}"})
            modified_line = replace_last(line, quote, user_input)
            lines = write_line_to_file(i - 1, modified_line)

if __name__ == "__main__":
    process_lines()
