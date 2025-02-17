# Project Overview
This repository contains various files that contribute to the automatic transformation of standard French text into inclusive French. Below is an overview of the key files included in the repository:

## Repository Files

### 1. `classif_common_noun_person.h5`
This file is a trained neural network model that classifies common nouns in French based on whether they refer to a person. The classification is a probability score between 0 and 1:
- **closer to 0**: The noun does not refer to a person.
- **closer to 1**: The noun refers to a person.

### 2. `formatted_wikidata.json`
This file consists of triplets extracted from Wikidata containing common nouns in their feminine, masculine, and neutral forms. It is a valuable resource for identifying and transforming gendered terms in texts.

### 3. `Lexique_tous_noms_communs.xlsx`
This spreadsheet contains an extensive list of common French nouns along with their gender and other relevant linguistic properties. The data has been sourced from Lexique.org.

### 4. `to_inclusive.ipynb`
A Jupyter Notebook that processes French text to convert it into its inclusive form. It utilizes various NLP techniques, dictionaries, and machine learning models to detect and modify gendered language.

### 5. `train_classifier_noun_person.py`
This Python script trains the neural network model used in `classif_common_noun_person.h5`. It loads a dataset (`data_classif_person.csv`), which contains common nouns along with their respective labels (person/non-person) and precomputed embeddings, to train a binary classifier.

### 6. `data_classif_person.csv`
A dataset used for training the classifier found in `classif_common_noun_person.h5`. It contains three columns:
- **Noun**: The common noun in French.
- **Label**: Whether it refers to a person (1) or not (0).
- **Embedding**: A vector representation of the noun used as input for the classifier.

### 7. `epicene.py`
This script extracts a list of epicene nouns and adjectives from The Office Québécois de la langue Française and stores them in dictionaries. It detects instances of replaceable terms using regular expressions and replaces them while handling:

- Case preservation

- Article modifications (e.g., words that start with vowels)

---

# To Inclusive - Convert Standard French to Inclusive French

## Overview
`to_inclusive` is a project designed to automatically convert standard French text into inclusive French. It processes text by modifying gendered words, ensuring more inclusive and representative language usage. The project uses various NLP techniques, including a deep learning model and linguistic resources, to identify and transform gendered noun phrases and expressions.

## Features
- **Automatic Gender-Neutralization**: Converts gendered nouns, adjectives, determiners, and past participles to inclusive forms.
- **Context-Aware Transformation**: Ensures accuracy by analyzing the grammatical structure of sentences.

## Installation
### 1. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies
Manually install required packages using:
```sh
pip install tensorflow==2.18.0
pip install transformers==4.47.1
pip install torch==2.5.1+cu124
pip install spacy==3.7.5
python -m spacy download fr_core_news_md
pip install numpy==1.26.4
pip install SPARQLWrapper==2.0.0
pip install requests==2.32.3
pip install pandas==2.2.2
pip install regex==2024.11.6
pip install pattern3==3.0.0
pip install openpyxl==3.1.5
pip install sentencepiece==0.2.0
pip install inflect
pip install gender_guesser
```

### 3. Install pynlg (Natural Language Generation Library)
```sh
git clone https://github.com/mapado/pynlg.git
cd pynlg
python setup.py install
cd ..
mv pynlg pynlg2
cd pynlg2
mv pynlg ../
```

### 4. Modify Pattern Library
Modify `pattern3` package to fix compatibility issues:
- Open the file `pattern3/text/tree.py`.
- On **line 36**, add `'str'` to resolve any errors.

## Usage
### Running the Notebook
Open `to_inclusive.ipynb` in Jupyter Notebook and execute all cells.

### Input and Processing
The project processes text input by:
1. Identifying gendered nouns referring to persons, adjectives, past participles, and determiners associated with the noun.
2. Applying transformation rules based on linguistic structures and using several linguistic resources.
3. Ensuring inclusivity while maintaining grammatical correctness.
