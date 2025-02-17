# Imports

import requests
from bs4 import BeautifulSoup
import re
import inflect
import gender_guesser.detector as gender






# Extraction of epicene nouns and adjectives --------------------------------------------------------------------------------------------------------------------------------------------


# finding the tables in the url provided by the guide
url = 'https://vitrinelinguistique.oqlf.gouv.qc.ca/index.php?id=25465&utm_source=BDL&utm_campaign=Redirection+des+anciens+outils&utm_content=th%3D2%26t1%3D%26id%3D5465'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table')


# creating the corresponding dictionaries to store the terms in
epicene_nouns = {} 
administrative_units = {} 
epicene_adjectives = {}


def extract_table_data(table):
    """
    Given a table in a url, this function extracts its content and stores it into a python dictionary
    It returns the created dictionary
    It also preprocesse the data before storing it so that there are only single words in the dictionary keys and values
    """
    extracted_dict = {}
    for row in table.find_all('tr')[1:]: 
        columns = row.find_all('td')
        if len(columns) >= 2:
            keys = [key.strip() for key in columns[0].get_text(strip=True).split(',')]  
            first_value = columns[1].get_text(strip=True).split(',')[0].strip()  
            for key in keys:
                extracted_dict[key] = first_value  
    return extracted_dict


# calling extract_table_data to store the terms in the corresponding dictionary
epicene_nouns = extract_table_data(tables[0])
administrative_units = extract_table_data(tables[1])
epicene_adjectives = extract_table_data(tables[2])








# Handling case conservation ---------------------------------------------------------------------------------------------------------------------------------------------


def match_case(word, replacement):
        """
        Given a word and the word it should be replaced with, this function detects the case from the initial word and returns the replacement with the same case applied
        replacement argument is always considered to be in lower case
        """
        if word.isupper():
            return replacement.upper()
        elif word.istitle():
            return replacement[0].upper() + replacement[1:]
        else:
            return replacement.lower()







# Handling article modification --------------------------------------------------------------------------------------------------------------------------------------------


def replace_article_vowels(text):
    """
    Given a string as an entry, this function detects the article+noun pattern and if the noun starts with a vowel or an h, it replaces the initial article with "L'"
    It matches the case of the initial article
    Returns the same article+noun combo with the actualized article
    """

    pattern = r"\b(Le|La)\s+([aeiouhAEIOUH]\w*)\b"

    def replace_match(match):
        article = match.group(1)  
        word = match.group(2)    
        new_article = "L'" if (article.lower() == "le" or article.lower() == "la") else article
        return match_case(article, new_article) + match_case(word, word)

    return re.sub(pattern, replace_match, text)



def replace_article_gender(text):
    """
    Given a string as an entry, this function detects the article+noun pattern and if the noun is feminine, it replaces the initial article with "La"
    If the noun isn't detected as feminine, it replaces the initial article with "Le ou la"
    It matches the case of the initial article
    Returns the same article+noun combo with the actualized article
    """

    pattern = r"\b(Le|La)\s+(\w+)\b"

    def replace_match(match):
        article = match.group(1)  
        word = match.group(2)  
        gender_result = d.get_gender(word[0])
        if gender_result in ['female', 'mostly_female']:
            new_article = match_case(word,'la ')
        else:
            new_article = match_case(word, 'Le ou la ')
        return match_case(article, new_article) + match_case(word, word)

    return re.sub(pattern, replace_match, text)







# Replacing the nouns and adjectives detected as replaceable by their epicene equivalent

# Initializatin of gender and number detectors
p = inflect.engine()
d = gender.Detector()


def epicenize(text, data_dicts):
    """
    Given a string and a list of replacement dictionaries as an entry, this function detects replaceable terms and replaces them accordingly
    It does case conservation
    Returns the same text with replaced terms and a boolean that indicates if the text has been changed
    """

    init_text = text
    modif = False

    for data_dict in data_dicts:
        for key in data_dict.keys():
            if key:

                # handling singular
                pattern = r'\b' + re.escape(key) + r'\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    text = text.replace(match, match_case(match, data_dict[key]))

                # handling plural
                pattern_plural = r'\b' + re.escape(key+'s') + r'\b'
                matches = re.findall(pattern_plural, text, re.IGNORECASE)
                for match in matches:
                    text = text.replace(match, match_case(match, p.plural(data_dict[key]))) 

    # handling article changes
    text = replace_article_vowels(text)

    if text != init_text:
        modif = True
        text = replace_article_gender(text)
     
    return text, modif









# Testing ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# list of dictionaries to pass as arguments
data_dicts = [epicene_nouns,administrative_units,epicene_adjectives]

texts = [
    "L'actrice est active.",
    "Les actrices sont actives.",
    "L'actrice est généreuse.",
    "La rivale est généreuse.",
    "La dessinatrice est détendue.",
    "L'acteur est très actif.",
    "Les acteurs sont généreux.",
    "Le président est intelligent.",
    "L'enseignant et l'enseignante ont parlé.",
    "Le chirurgien et la chirurgienne sont compétents.",
    "L'avocat et l'avocate ont plaidé.",
    "Les enseignants sont intelligents.",
    "Les actrices sont fort respectées.",
    "Le directeur est généreux.",
    "Les présidents sont intelligents."
]

for text in texts:
    modified_text, modified = epicenize(text, data_dicts)
    print(f"Original: {text}")
    print(f"Modified: {modified_text}")
    print('-' * 50)
