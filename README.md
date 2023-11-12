# my-chatbot
This chatbot was created during the course "M913 - Dialogue Systems" (Fall 2023). This is a third semester course of the MSc Language Technology.

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
