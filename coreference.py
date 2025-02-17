import spacy
import re
from fastcoref import FCoref

def resolve_coreferences(text: str):
    
    nlp = spacy.load("fr_core_news_sm")
    coref = FCoref(device="cpu")
  
    clusters = coref.predict(texts=[text])

    return clusters

def replace_coreferences(coref_result):
    
    coref_result = coref_result[0]
  
    text = coref_result.text
    clusters = coref_result.clusters
  
    for cluster in clusters:
        
    
        reference_start, reference_end = cluster[0]
        reference = text[reference_start:reference_end+1] 
        
        for mention_start, mention_end in cluster[1:]:
            mention = text[mention_start:mention_end+1] 
          
            text = re.sub(r'\b' + re.escape(mention) + r'\b', reference, text)
    
    return text




if __name__ == "__main__":
    test_sentences = [
        "Jean adore le football. Il joue tous les week-ends avec ses amis.",
        "Sophie a perdu son sac. Elle l’a cherché partout.",
        "Paul et Luc sont allés au cinéma. Ils ont regardé un film d’action.",
        "Le professeur a donné des devoirs aux élèves. Ceux-ci doivent être rendus lundi.",
        "Claire s'est acheté une robe. Elle se l'est offerte pour son anniversaire."
    ]

    resolved_text = replace_coreferences(resolve_coreferences(test_sentences[1]))
    print(resolved_text)
  
    for i, sentence in enumerate(test_sentences):
        clusters = resolve_coreferences(sentence)
        resolved = replace_coreferences(clusters)
        print(f"Exemple {i}:\nAvant: {sentence}\nAprès: {resolved}\n")
