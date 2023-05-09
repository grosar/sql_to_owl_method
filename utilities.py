from parameters import *

def list_elements_inside_string(string): # for sql insert with multiple values
    list_of_inserts = []
    flag_count = 0
    copy_string = []
    count = 0

    for index in range(len(string)):
        character = string[index]
        if "(" == character:
            flag_count += 1
        elif ")" == character and flag_count>1:  
            flag_count -= 1
        elif ")" == character and flag_count>0:
            index_prog = index + 1
            flag_def = False
            if index_prog >= len(string):
                flag_def = True

            while(index_prog < len(string)):
                if string[index_prog]!=" " and string[index_prog]!="\n":
                    break
                if string[index_prog]=="(":
                    flag_def = True
                    break
                index_prog += 1

            if flag_def:    
                flag_count -= 1
                if flag_count == 0:
                    list_of_inserts.append(convert_character_list_into_string(copy_string))

                    copy_string = []
                    count = 0
        
        if flag_count > 0 and count > 0:
            copy_string.append(character)
        elif flag_count > 0 and count == 0:
            count+=1
    if flag_count > 0:
        list_of_inserts.append(convert_character_list_into_string(copy_string[:(len(copy_string)-1)]))

    return list_of_inserts

def convert_character_list_into_string(s):
    new = ""
    for x in s:
        new += x
    return new

def acquire_user_choice(question):
    answer1 = ""
    while answer1 not in ("y", "n"): 
        answer1 = input(question) 
        if str.lower(answer1) == "y": 
           return True
        elif str.lower(answer1) == "n":
            return False
        else: 
            print("Please enter y or n.")
