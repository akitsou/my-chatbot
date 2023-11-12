# This files contains your custom actions which can be used to run
# custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from urllib.parse import quote_plus 


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
        return "inform_abt_helpline"
    
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
        return "list_247_pharmacies"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Current tracker staet:", tracker.current_state())

        url = "https://farmakeia.gr/farmakeia-konta-mou"

        dispatcher.utter_message(text=f"""Μπες εδώ και δες τα φαρμακεία της περιοχής σου: {url}. Μην ξεχάσεις να επιτρέψεις
        την πρόσβαση στην τοποθεσία σου, ώστε να γίνει αυτόματα η αναζήτηση των πλησιέστερων φαρμακείων.
        Αν κάποιο φαρμακείο εφημερεύει, τότε θα δεις την πράσινη ταμπέλα με τη λέξη 'Εφημερεύει' στην πάνω αριστερή γωνία.""")

        return[] 