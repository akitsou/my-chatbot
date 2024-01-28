# my-chatbot (Assignment 1)
This chatbot was created during the course 'M913 - Dialogue Systems' (Fall 2023), which is a third semester course of the MSc Language Technology offered by the National and Kapodistrian University of Athens in Greece.

## Project structure
```
$PROJECT_ROOT
¦   # Directory containing custom actions for the chatbot
+-- actions
¦   ¦   # Initializer for the actions module
¦   +-- __init__.py
¦   ¦   # Python script defining custom actions
¦   +-- actions.py
¦   # Directory containing training data for the chatbot
+-- data
¦   ¦   # NLU training data
¦   +-- nlu.yml
¦   ¦   # Rules for the chatbot
¦   +-- rules.yml
¦   ¦   # Stories for the chatbot
¦   +-- stories.yml
¦   # Directory containing trained model files
+-- models
¦   ¦   # Trained model archive
¦   +-- 20231112-170215-little-staff.tar.gz
¦   
+-- .gitignore
¦   
+-- LICENSE
¦  
+-- README.md
¦   # Configuration file for the chatbot
+-- config.yml
¦   # Domain file specifying chatbot's intents, entities, slots, and templates
+-- domain.yml
¦   # Endpoints configuration for the chatbot
+-- endpoints.yml
```

## Domain
I have chosen to develop a chatbot in the medical domain, because I believe such a service can be extremely helpful to humans. Providing accurate and fast answers to medical questions is of paramount importance, as it can improve human health and, therfore, human longevity. The majority of exisitng commercial medical chatbots works for the English language, this is why I decided to create one for the Greek language.

## Three main scenarios
My chatbot can provide three main services. Firstly, it can fetch answers for questions about various health issues, their symptoms and their treatments. Secondly, it can search for a range of medications, either when a specific symptom is specified or not. Thirdly, it can search for pharmacies near the user's area. Also, my chatbot is programmed to recognise suicidal intents and respond with empathy while providing the appropriate helpline and resources.

## Future capabilities
By the end of the course, I would like my chatbot to be able to connect to more medical resources, e.g. well-known journals for different medical domains like cardiology, neurology, etc., and be able to summarize the most relevant information into 'plain Greek'. To do this, I plan to cooperate with a practising Greek GP.

## Forms and Policies (Assignment 3)
Our task was to use Rasa to further develop our chatbot prototype to use forms and more advanced dialogue policies. 

### 1. Rasa forms: Update at least one of your chatbot scenarios to be handled by means of Rasa forms. The form must be used for the data collection part, a.k.a slot filling. Make sure your chatbot properly responds to cases when the user provides an invalid input or they just say something irrelevant, e.g., chitchat. 
I have extended the  bot’s functionality by adding a fourth scenario, i.e. the intent of searching for nearby hospitals and clinics. The relevant story involves filling in the slots ‘city’ and ‘country’ via a form (‘hospital_form’) addressed to the user, so that a Google Maps webpage can be pulled up in a subsequent step, once the two slots have been filled. During the slot filling process, I have added a validation step that checks whether the two slots for ‘city’ and ‘country’ are indeed provided by the user in a valid way (i.e. whether they are alphabetic characters of more than 2 and 3 characters respectively, and non-empty inputs); if not, the user is prompted to type again. The validation step is a custom form validation action found in the `action.py` file. What is more, my code in that file now includes more debugging print statements, so that it is easier to check the action server’s logs.

Also, the bot now properly handles certain deviations from the four main stories, e.g. when the user says something silly to tease the bot. The bot can now also handle the users complaining about being misunderstood. What is more, the bot handles chitchat about its name, birthplace, and age, and tactfully refuses to gossip about other people when the user intends to.

### 2. Policies: Experiment with Rasa policies: RulePolicy, MemoizationPolicy, TEDPolicy.
Regarding the policies (which are responsible for the Dialogue Management), I have extended the ‘RulePolicy’, which has the first priority in predicting the next action, by writing more rules (e.g. ‘Activate hospital form - Happy path only!’, ‘Submit form’,  ‘User complains to the bot for misunderstanding’, ‘User wants to search more sites’, ‘Interruption during hospital form for the bot challenge’, ‘Chitchat about birthplace’, ‘Chitchat about age’, ‘Chitchat about person’, ‘Chitchat about silly things’, ‘Chitchat about name "Hippocrates"’ ). For that policy I have lowered the default value for 'core_fallback_threshold' to 0.2 , as it works better and does not overstimulate the `action_default_fallback` like higher values did. I have also defined a ‘MemoizationPolicy’, which takes second priority, and which uses the memory of 6 previous turns (N.B.: one turn comprises a user’s message and a bot’s action) from the existing, defined stories to make predictions for the bot’s next action. Last, I have defined the ‘TEDPolicy’, which is a transformer-based policy for next action prediction and entity recognition, with training for 100 epochs, a ‘max_history: 8’ (following the example in the official RASA documentation) so that it makes predictions for the next best action based on the 8th previous state in a story, and ‘constrain_similarities: True’, which leads to better generalization of the model to real world data. As further experimentation, I added the 'UnexpectedTEDPolicy' too, which is an experimental and auxiliary policy to the ‘TEDPolicy’, and allows the bot to react to unlikely user turns. I kept the same number of ‘max_history’ as the ‘TEDPolicy’, since it is recommended by the official Rasa documentation.

My repository now has the optimal policy and the forms implemented. 
Indicative test cases that should be working correctly:
1. all four scenarios' happy paths, as described in the `stories.yml` file
2. all four scenarios interrupted by the user at any time for the bot challenge or for one of the five kinds of chitchat (chitchat on bot's birthplace, age or name; gossip about people; chitchat about silly things) or when the user expresses suicidal thoughts
3. the 'hospital form' is validated and displays a message for re-entering input, if the user inputs a number, too few characters, or just nothing when asked to type in their city and country.
4. the user signifies being misunderstood

## Extra experimentation on Pipeline
Regarding the pipeline, it is important to mention that the chatbot only supports the Greek language, but not the English or a mix of those (i.e. Greeklish. Interestingly, I have experimented by using the SpaCy model’s pre-trained Greek word embeddings (large model), but the results were disappointing, i.e. noticeably worse in the intent classification task than when <i>not</i> using the Greek SpaCy model, but just the DIETClassifier. This is presumably because the transformer-based DIETClassifier, working in tandem with ‘CountVectorsFeaturizer’ and ‘LexicalSyntacticFeaturizer’, performs better when trained on the `nlu.yml` training data belonging to a specific domain (here, the medical domain) than the “off-the-shelf” SpaCy word embeddings, which are pre-trained on general Greek text. 

Nonetheless, I did use the SpaCy model for complementing the bot’s named entity extraction, in particular regarding the ‘PERSON’ and ‘GPE’ entities (N.B.: the Greek model’s NER can only extract the following entities: PERSON, GPE, LOC, ORG, PRODUCT, and EVENT; moreover, it is not as great at recall as the English model). 

Regarding the DIETClassifier, I have set the following, moderately complex hyperparameters for the model’s training: 
- name: DIETClassifier
- loss_type: cross_entropy, as it is a common loss function for classification problems
- embedding_dimension: 128, which is a moderate value, since my training data is not very large
- transformer_size: 512, for a fairly good model performance
- number_of_attention_heads: 4, which is a standard value
- number_of_transformer_layers: 1, the model remains simple, but it performs well
- constrain_similarities: True, which is a normalization step ensuring that the similarity values (between input text embeddings and label embeddings, like intents or entities) are scaled in a way that helps the model learn more effectively

As for entity extraction, I decided against using the entity classifier ‘EntitySynonymMapper’, because it often marked non-entities as real entities. Another experiment was that I tried to use the ‘RegexEntityExtractor’ together with a regex pattern for an example of a certain entity, but it did not capture that example in a real story, so I only kept it for the lookup table of cities. In the end, I had to comment it out as well, as the problem that arose was multiple extraction of entities. Specifically, there were overlaps in entity extraction (duplicate entities or even triple ) extracted by ‘DIETClassifier’, ‘RegexEntityExtractor’, and ‘SpacyEntityExtractor’.

Last, I found it beneficial to lower the threshold of the 'FallbackClassifier' to 0.2. The FallbackClassifier classifies a user's message with the intent 'nlu_fallback' in case the previous intent classifier wasn't able to classify the intent with a confidence greater or equal than the threshold. 


## TO DO (ideas coming from people who have tested the chatbot):
A) An extra slot ‘brand’ for the NLU training data of the intent ‘search_drug’.

B) A fifth intent ‘search_doctor_specialization’, and a corresponding form with three slots to be filled after being validated: ‘doc_specialization’, ‘city’, and ‘country’.

C) Observe more test users asking for certain things, which I will then turn into new intents.


