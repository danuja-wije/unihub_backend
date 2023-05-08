import pandas as pd
import networkx as nx
import spacy
import pandas as pd
from spacy import displacy
import PyPDF2
from os.path import join, dirname, realpath
from spacy.matcher import PhraseMatcher
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
NER = spacy.load('en_core_web_lg')
nlp = spacy.load("en_core_web_lg")

def exctractor(path: str):
    path = join(dirname(realpath(__file__)), path)
    path = path + '.pdf'
    print(path)
    with open(path, 'rb') as file:
        # Create a PDF object
        pdf = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        num_pages = len(pdf.pages)

        # Initialize an empty list to store the skills
        skills = []
        all_text = []
        # Iterate through each page of the PDF
        for i in range(num_pages):
            # Get the text of the current page
            page = pdf.pages[i]
            text = page.extract_text()
            all_text.append(text)
        # print(" ".join(all_text))



    # init params of skill extractor

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    annotations = skill_extractor.annotate("".join(all_text))

    data = [line['doc_node_value'] for line in annotations['results']['full_matches']]
    for d in data:
        temp = d
        data.remove(d)
        temp = temp.lower()
        # print(temp)
        data.append(temp)

    return {"skills":list(set(data))}

# print(exctractor('Ambulance Booking System.pdf'))