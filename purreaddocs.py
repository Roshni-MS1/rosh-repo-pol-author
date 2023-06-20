

#readopenaikey
def readopenaikey():
    with open('C:\\Users\\roshnipatil\\Documents\\GitHub\\openaikey.txt', 'r') as file:
        # Read all lines of the file
        return file.read()





#Open the file for reading
def readSampleDoc():
    with open('C:\\Users\\roshnipatil\\Documents\\GitHub\\testpii.txt', 'r') as file:
        # Read all lines of the file
        return file.read()


#Open the file for reading
def writeprompttofile(prompt_text):
    with open('C:\\Users\\roshnipatil\\Documents\\GitHub\\search_prompts.txt', 'w') as file:
        file.write(prompt_text)


#Open the file for reading
def writesencheckprompttofile(sen_prompt_text):
    with open('C:\\Users\\roshnipatil\\Documents\\GitHub\\sen_check_prompts.txt', 'w') as file:
        file.write(sen_prompt_text)


#Open the file for reading
def writesenlistprompttofile(sen_prompt_text):
    with open('C:\\Users\\roshnipatil\\Documents\\GitHub\\sen_list_prompts.txt', 'w') as file:
        file.write(sen_prompt_text)
