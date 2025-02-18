# Imports
import json
import os
import re



# Triplet extraction ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

triplet_path = "./formatted_wikidata.json" # 

with open(triplet_path, 'r') as file:
    data = json.load(file)
print(data[0])

# Dictionary for masculine and neutral -----------------------------------------------------------------------------------------------------------------------------------------------------------

masc_neutral_data_dict = {}
for triplet in data:
  masc_neutral_data_dict[triplet[1]] = triplet[0]


# Dictionary for masculine and feminine -----------------------------------------------------------------------------------------------------------------------------------------------------------

masc_fem_data_dict = {}
for triplet in data:
    masc_fem_data_dict[triplet[1]] = triplet[2]


# Object vs entity detection -----------------------------------------------------------------------------------------------------------------------------------------------------------

import nltk
from nltk.corpus import wordnet as wn
nltk.download('omw-1.4')

nltk.download('wordnet')

def is_person_top(word, lang='fra'):
    synsets = wn.synsets(word, lang=lang)

    if not synsets:
        return f"Aucun synset trouvé pour le mot : {word}"

    person_synset = wn.synset('person.n.01')

    for synset in synsets:
        current_synset = synset
        while current_synset.hypernyms():
            current_synset = current_synset.hypernyms()[0]

            if current_synset == person_synset:
                return True

    return False

# Handling case -----------------------------------------------------------------------------------------------------------------------------------------------------------


def match_case(word, replacement):
        if word.isupper():
            return replacement.upper()
        elif word.istitle():
            return replacement[0].upper() + replacement[1:]
        else:
            return replacement.lower()


# Handling plural -----------------------------------------------------------------------------------------------------------------------------------------------------------

# def pluralize(word, inclusive = 'or'):
#     if inclusive == 'or':
#         words = word.split(" ")
#         print(words)
#         pluralized = []
#         for split_word in words:
#             if split_word!='ou' and not split_word.endswith('s'):
#                 pluralized.append(split_word + 's')
#             else:
#                 pluralized.append(split_word)
#         return " ".join(pluralized)

#     elif inclusive == 'dot':
#         return word + '.s'

#     else:
#         print("This type of inclusive French is not handled.")


def pluralize(word):
    words = word.split(" ")
    pluralized = []
    for split_word in words:
        if split_word!='ou' and not split_word.endswith('s'):
            pluralized.append(split_word + 's')
        else:
            pluralized.append(split_word)
    return " ".join(pluralized)


print(pluralize('informaticien ou informaticiennes'))

# Replacing masculine with neutral in standard french, handling case --------------------------------------------------------------------------------------------------------------------


# def masc_to_neutral(text, data_dict, inclusive = 'or'):
#     init_text = text
#     modif = False
#     for key in data_dict.keys():
#         if key:
#             text = text.replace(key, match_case(key, data_dict[key]))
#     if text!=init_text:
#         modif = True
#     return text, modif

def masc_to_neutral(text, data_dict):
    init_text = text
    modif = False

    for key in data_dict.keys():
        if key:
            pattern = r'\b' + re.escape(key) + r'\b'
            pattern = r'\b' + re.escape(key) + r'\b'
            match = re.search(pattern, text, re.IGNORECASE)  # Ignore case if needed
            return bool(match)
            text = text.replace(key, match_case(key, data_dict[key]))

    if text!=init_text:
        modif = True

    return text, modif

print(masc_neutral_data_dict['acteur'])

text1 = "Bonjour, je suis informaticien. J'ai un orteil et un marteau et je suis acteur à mes heures perdues. Acteur."
text2 = "Bonjour"
text3 = "Bonjour, nous sommes informaticiens. J'ai un orteil et un marteau et nous sommes acteurs à nos heures perdues."

resultat1 = masc_to_neutral(text1, masc_neutral_data_dict)
print(resultat1)

resultat2 = masc_to_neutral(text2, masc_neutral_data_dict)
print(resultat2)

resultat3 = masc_to_neutral(text3, masc_neutral_data_dict)
print(resultat3)



# Creating the dot version -----------------------------------------------------------------------------------------------------------------------------------------------------------

# def create_dot_word(dot_dict, word):

#     if word in dot_dict:
#         feminine = dot_dict[word]
        
#         if feminine.startswith(word):
#             difference = feminine[len(word):]
#             return f"{word}.{difference}"

#         else:
#             return word
#     else:
#         return word

#print(create_dot_word(masc_fem_data_dict,'président'))




# Handling inclusive french  -----------------------------------------------------------------------------------------------------------------------------------------------------------








