student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas
student_data_frame = pandas.DataFrame(student_dict)
# print(student_data_frame)
#Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    #Access index and row
    #Access row.student or row.score
    pass



#TODO 1. Create a dictionary in this format:
data = pandas.read_csv("nato_phonetic_alphabet.csv")
# print(data)
phonetic_dict = {row.letter:row.code for (index, row) in data.iterrows()}
print(phonetic_dict)
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

def generate_phonetic():
    word = input("Enter word: ").upper()
    try:

        output_list = [phonetic_dict[letter] for letter in word]
    except KeyError:
        print("Sorry only letters should be inputted not numbers")
        generate_phonetic()
    else:
        print(output_list)

generate_phonetic()

