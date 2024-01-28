# This files contains your custom actions which can be used to run custom Python code.
# import logging

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction # Tracker: Contains the state of the conversation.
from rasa_sdk.executor import CollectingDispatcher # Used to send messages back to the user.
from urllib.parse import quote_plus 
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet


class ActionFetchWebAdvice(Action):
    def name(self) -> Text:
        return "action_fetch_web_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())

        # Get the *values* from the tracker
        symptom = tracker.get_slot("symptoms")

        # Additional Debugging - symptom value
        print("Symptom slot value:", symptom)

        encoded_symptom = quote_plus(symptom)

        url = f"https://www.onmed.gr/search?q={encoded_symptom}"

        dispatcher.utter_message(text=f"Δες περισσότερες πληροφορίες σχετικά με το πρόβλημά σου εδώ: {url}")

        return []


class ActionTrySkroutz(Action):
    def name(self) -> Text:
        return "action_try_skroutz"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())
        
        drug = tracker.get_slot("drug") or ''
        symptom = tracker.get_slot("symptoms") or ''

        # Debugging 2 - print both values
        print("Drug + symptom slot value:", drug, symptom)
        
        encoded_drug = quote_plus(drug)
        final_search = encoded_drug
        if symptom:
            encoded_symptom = quote_plus(symptom)
            final_search += f"+{encoded_symptom}"

        url = f"https://www.skroutz.gr/search?keyphrase={final_search}"

        # Debugging 3 - print URL
        print(f"The final URL for skroutz.gr is: {url}")

        dispatcher.utter_message(text=f"Μπορείς να επιλέξεις και να παραγγείλεις το φάρμακο που ζήτησες εδώ: {url}")

        return []


class ActionTryFarmakopoios(Action):
    def name(self) -> Text:
        return "action_try_farmakopoios"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())
        
        drug = tracker.get_slot("drug") or ''
        symptom = tracker.get_slot("symptoms") or ''

        # Debugging 2 - print both values
        print("Drug + symptom slot value:", drug, symptom)

        encoded_drug = quote_plus(drug)
        final_search = encoded_drug
        if symptom:
            encoded_symptom = quote_plus(symptom)
            final_search += f"%20{encoded_symptom}" # Concatenate drug %20 symptom for the specfic wesite

        url = f"https://www.ofarmakopoiosmou.gr/#search/{final_search}"

        dispatcher.utter_message(text=f"Μπορείς να επιλέξεις και να παραγγείλεις το φάρμακο που ζήτησες εδώ: {url}")

        return []    
    

class ActionFetchQuote(Action):
    def name(self) -> Text:
        return "action_fetch_quote"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())

        url = "https://www.brainyquote.com/quote_of_the_day"

        dispatcher.utter_message(text=f"Πάτησε εδώ και αφιέρωσε όσο χρόνο θες για να αναλογιστείς πάνω στο θετικό ρητό της ημέρας: {url}")

        return []
    

class InformAbtHelpline(Action):
    def name(self) -> Text:
        return "action_inform_abt_helpline"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())

        url = "http://suicide-help.gr/ori-stichia/"

        dispatcher.utter_message(text=f"""Επίσης, μην διστάσεις να τηλεφωνήσεις στην 24ωρη γραμμή παρέμβασης για την αυτοκτονία στο 1018 ή να στείλεις email στη διεύθυνση:
        help@suicide-help.gr. Πάτησε τον ακόλουθο σύνδεσμο, περιηγήσου στην ιστοσελίδα και μάθε σημαντικά στοιχεία για την αυτοκτονία παγκοσμίως 
        πριν κάνεις οποιαδήποτε κίνηση: {url}""")

        return []


class List247Pharmacies(Action):
    def name(self) -> Text:
        return "action_list_247_pharmacies"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Current tracker staet:", tracker.current_state())

        url = "https://farmakeia.gr/farmakeia-konta-mou"

        dispatcher.utter_message(text=(
            'Μπες εδώ και δες τα φαρμακεία της περιοχής σου: {url}. '
            'Μην ξεχάσεις να επιτρέψεις την πρόσβαση στην τοποθεσία σου, '
            'ώστε να γίνει αυτόματα η αναζήτηση των πλησιέστερων φαρμακείων. '
            'Αν κάποιο φαρμακείο εφημερεύει, τότε θα δεις την πράσινη ταμπέλα '
            'με τη λέξη "Εφημερεύει" στην πάνω αριστερή γωνία.'
            ).format(url=url))

        return[] 
    


class ShowHospitalsOnGMaps(Action):
    def name(self) -> Text:
        return "action_show_hospitals_on_GMaps"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging - tracker state
        print("Current tracker state:", tracker.current_state())
        
        city = tracker.get_slot("city") #or ''
        country = tracker.get_slot("country") #or ''

        # Debugging 2 - print both values
        print("City & country slot values are :", city, country)

        encoded_city = quote_plus(city)
        encoded_country = quote_plus(country)
        final_search = f"{encoded_city}+{encoded_country}"

        url = f"https://www.google.com/maps/search/hospitals+in+{final_search}"

        # Debugging 3 - print URL
        print(f"Final URL is: {url}")

        dispatcher.utter_message(text=f"Μπορείς να δεις όλα τα κοντινότερά σου νοσκομεία στο χάρτη πατώντας εδώ: {url}")

        return []    
    

# BELΟW ARE A COUPLE OF FAILED ATTEMPTS TO VALIDATE & DEBUG THE 'HOPSPITAL_FORM'. THEY TOOK TOO MANY HOURS TO JUST DELETE...
    
# logger = logging.getLogger(__name__)
# class ValidateHospitalForm(FormValidationAction): # Handle cases where no valid 'city'/'country' entity is detected.
#     def name(self) -> Text:
#         logger.info("Loaded action: validate_hospital_form")
#         return "validate_hospital_form"

#     # def name(self) -> Text:
#     #     return "validate_hospital_form" # Custom actions named validate_<form name> will run automatically if the form it specifies in its name is activated.

#     def validate_city(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:

#         # Extract the latest 'city' entity value from the user's last message. If no 'city' entity is found, then 'city_entity'=None.
#         city_entity = next(tracker.get_latest_entity_values("city"), None)
#         last_user_message = tracker.latest_message.get('text')


#         # Debugging - print the slot value
#         logger.info(f"Validating city slot. slot_value: {slot_value}, city_entity: {city_entity}")

#         logger.info(f"Validating city. Entity extracted: {city_entity}, User input: {tracker.latest_message.get('text')}")

#         # Debugging - print print the entity
#         print(f"This is the city entity extracted: {city_entity}.")

#         if city_entity:
#         # Verify if the entity was successfully extracted.
#             return {"city": city_entity}
#         elif last_user_message and len(last_user_message.strip()) >= 2:
#         # If no entity is extracted, but the raw input is valid, use it.
#             return {"city": last_user_message.strip()}
#         else:
#         # Handle the case where no city entity was extracted (the NLU model does not recognize any entity in the user's input as a city).
#             dispatcher.utter_message(text="Νομίζω ότι πληκτρολόγησες κάτι λάθος! Ξαναγράψε μου την περιοχή, την πόλη, το νησί ή το χωριό σου, σε παρακαλώ!")
#             return {"city": None} # THis prompts the use to enter their input once more.

#     def validate_country(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:

#         country_entity = next(tracker.get_latest_entity_values("country"), None)

#         # Debugging
#         logger.info(f"Validating country slot. slot_value: {slot_value}, country_entity: {country_entity}")
#         logger.info(f"Validating country. Entity extracted: {country_entity}, User input: {tracker.latest_message.get('text')}")

#         # Debugging - print
#         print(f"This is the country entity extracted: {country_entity}.")

#         if country_entity:
#             return {"country": country_entity}
#         else:
#             dispatcher.utter_message(text="Νομίζω ότι πληκτρολόγησες κάτι λάθος! Ξαναγράψε μου τη χώρα σου!")
#             return {"country": None}


##### The following 2 classes work, but are ΝΟΤ automatically called during the execution of the hospital form when the respective slot is filled.
# class ValidateCityAction(Action): 
#     def name(self) -> Text:
#         return "validate_hospital_form_city"

#     async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:
        
#         city = tracker.get_slot("city")
        
#         # Debugging
#         print(f"The city slot extracted from the user's input is: {city}.")

#         if city is not None and self.city_is_valid(city):  
#             return [SlotSet("city", city)]
#         else:
#             dispatcher.utter_message(text="Νομίζω ότι πληκτρολόγησες κάτι λάθος! Ξαναγράψε μου την περιοχή, την πόλη, το νησί ή το χωριό σου, σε παρακαλώ!")
#             return [SlotSet("city", None)]
        
#     def city_is_valid(self, city: Text) -> bool:
#         """Check if the city is valid."""
#        # Check if it's a real city name with alphabetic characters.
#         return city.isalpha()  

# class ValidateCountryAction(Action):
#     def name(self) -> Text:
#         return "validate_hospital_form_country"

#     async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:
        
#         country = tracker.get_slot("country")
        
#         # Debugging
#         print(f"The country slot extracted from the user's input is: {country}.")

#         if country is not None and self.country_is_valid(country):  
#             return [SlotSet("country", country)]
#         else:
#             dispatcher.utter_message(text="Νομίζω ότι πληκτρολόγησες κάτι λάθος! Ξαναγράψε μου τη χώρα σου!")
#             return [SlotSet("country", None)] 
        
#     def country_is_valid(self, country: Text) -> bool:
#         """Check if the country is valid."""
#        # Check if it's a real country name with alphabetic characters.
#         return country.isalpha()  


class ValidateHospitalForm(FormValidationAction):
    def name(self) -> Text:
         return "validate_hospital_form"

    async def validate_city(self, slot_value: Any, dispatcher: CollectingDispatcher,
                            tracker: Tracker, domain: Dict[Text, Any],) -> Dict[Text, Any]:
        
        # Debugging
        print(f"The slot value for the city is: {slot_value}.")

        if slot_value and self.is_valid_city(slot_value):
            # Validation is successful if there is a non-empty input and if the method 'is_valid_city'=True.
            return {"city": slot_value}
        else:
            # Validation fails and 'city'=null.
            dispatcher.utter_message(text=f'Νομίζω ότι πληκτρολόγησες κάτι λάθος εδώ: "{slot_value}"! Ξαναγράψε μου την περιοχή, την πόλη, το νησί ή το χωριό σου, σε παρακαλώ! Θα με βοηθήσεις πολύ αν γράψεις μόνο μια λέξη, π.χ. "Αθήνα". Προσπάθησε να μη βάλεις καθόλου νούμερα στην απάντησή σου!')
            return {"city": None}


    async def validate_country(self, slot_value: Any, dispatcher: CollectingDispatcher,
                               tracker: Tracker, domain: Dict[Text, Any],) -> Dict[Text, Any]:

        # Debugging
        print(f"The slot value for the country is: {slot_value}.")

        if slot_value and self.is_valid_country(slot_value): # Same as above for 'validate_city'.
            return {"country": slot_value}
        else:
            dispatcher.utter_message(text=f'Νομίζω ότι πληκτρολόγησες κάτι λάθος εδώ: "{slot_value}"! Ξαναγράψε μου τη χώρα σου! Θα με βοηθήσεις πολύ αν γράψεις μόνο μια λέξη, π.χ. "Ελλάδα". Προσπάθησε να μη βάλεις καθόλου νούμερα στην απάντησή σου!')
            return {"country": None}

    def is_valid_city(self, city: Text) -> bool:
        """Check if the city from user's input is valid."""
        # Check if it's a real city name with alphabetic characters and maybe spaces, e.g. Νέα Υόρκη (NO digits are accepted anywhere in the name).
        # Also check if it's at least 2 characters long (valid inputs with 2 chars: Κω=Kos island, Ίο=Ios island).
        passes_test_city = all(c.isalpha() or c.isspace() for c in city) and len(city) >=2
        return passes_test_city

    def is_valid_country(self, country: Text) -> bool:
        """Check if the country from user's input is valid."""
        passes_test_country = country.isalpha() and len(country) >=3 # valid input with 3 chars: ΗΠΑ
        return passes_test_country
        