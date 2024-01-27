import spacy
nlp = spacy.load("el_core_news_lg")

sentence = "Σου αρέσει ο Ντόναλντ Τραμπ; Εμένα όχι πολύ! πάμε μια βόλτα μαζί στην Νέα Υόρκη;"
sentence2= "Αγόρασα μια καινούρια τηλεόραση Samsung! Εσύ βλέπεις ταινίες στην τηλεόραση ή στο σινεμά;"
# Proces = s the sentence
doc = nlp(sentence2)
#print(doc.text)

# Print the text, and entity type (if any)
for token in doc:
    print(token.text, token.ent_type_)

# Additionally, printing entities in the sentence
for ent in doc.ents:
    print(ent.text, ent.label_)
############################################################################
    
# Access the NER component of the pipeline
# ner = nlp.get_pipe("ner")

# # Print all unique entity labels
# print("Entity labels in the Greek model:")
# for label in ner.labels:
#     print(label)