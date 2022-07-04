
PLACEHOLDER = '[name]'


with open("./Input/Names/invited_names.txt", "r") as name_file:
    names = name_file.readlines()
    print(names)

with open("./Input/Letters/starting_letter.txt", "r") as letter_file:
    letters = letter_file.read()
    for name in names:
        stripped_name = name.strip()
        new_letter = letters.replace(PLACEHOLDER, stripped_name)
        with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", mode='w') as completed_letter:
            completed_letter.write(new_letter)



