#TRANSLATION_FILE = "C:/git/AliceWonderland/game/tl/german/script.rpy"
TRANSLATION_FILE = "C:/git/AliceWonderland/game/tl/simple_english/script.rpy"
NEW_TRANSLATIONS_INDEX = 10065

# line number where new translatins were appened

def update_translation_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for i in range(len(lines)):
        # find the first line with translate
        if not lines[i].startswith("translate"): continue

        # find the first comment to get the original text
        for j in range(i+1, len(lines)):
            if not lines[j].strip().startswith("#"): continue
            
            # 

            # find the last occurence line in the remaining lines
            block_index = -1
            for k in range(len(lines)-1, NEW_TRANSLATIONS_INDEX, -1):
                if lines[k] == lines[j]:
                    block_index = k
                    break
            
            if block_index == -1: break # no occurence found => label does not need updating

            # check if the next line is a voice line
            voice = None
            if block_index + 1 < len(lines) and lines[block_index+1].strip().startswith("voice"):
                voice = lines[block_index+1]

            # rewind to the translate block
            while not lines[block_index].startswith("translate"):
                block_index -= 1
            
            # overwrite translate block with new translateion 
            lines[i] = lines[block_index]

            # erase old translate block
            lines[block_index] = ""
            while block_index < len(lines) and not lines[block_index].startswith("translate"):
                lines[block_index] = ""
                block_index += 1

            # insert voice line if it exists
            if voice:
                lines.insert(j+1, "    #" + voice.strip() + "\n")
            break

    # remove empty lines from eof
    while lines[-1].strip() == "":
        lines.pop()

    # Write the updated lines back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Use the function
update_translation_file(TRANSLATION_FILE)
