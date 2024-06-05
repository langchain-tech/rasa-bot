
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd
import pdb
import requests



class DataloadAPI(object):

    def __init__(self):
        self.db = pd.read_csv("/home/bluebash-005/code/bluebash/rasa chatbot/zappy/actions/weight_management_plans.csv")

    def fetch_data(self):
        return self.db.head()

    def format_data(self, df, header=True) -> Text:
        return df.to_csv(index=False, header=header)


class ChatGPT(object):

    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        self.prompt = "Answer the following question, based on the data shown. " \
            "Answer in a complete sentence and don't say anything else."

    def ask(self, restaurants, question):
        content  = self.prompt + "\n\n" + restaurants + "\n\n" + question
        body = {
            "model":self.model, 
            "messages":[{"role": "user", "content": content}]
        }
        result = requests.post(
            url=self.url,
            headers=self.headers,
            json=body,
        )
        return result.json()["choices"][0]["message"]["content"]



dataload_api = DataloadAPI()
chatGPT = ChatGPT()

class ActionShowPrograms(Action):

    def name(self) -> Text:
        return "action_show_program"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = dataload_api.fetch_data()
        results = dataload_api.format_data(data)
        #readable = dataload_api.format_data(data[['Plan Duration']], header=False)
        readable = data[['Plan Duration']].to_string(index=True)
        dispatcher.utter_message(text=f"Here are some programs:\n\n{readable} \n\n please select a number like 0,1,2 to know more about that program...")

        return [SlotSet("results", results)]




# class ActionShowDetail(Action):
#     def name(self) -> Text:
#         return "action_show_details"

#     def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         previous_results = tracker.get_slot("results")
#         program_number = tracker.latest_message["text"]
#         print(program_number)

#         if int(program_number)>=0 and int(program_number)<3:
#             req=f"what is the benifts of {program_number} program number \n here 0 programs number means (6 Months Plan) \n 1 program number means (3 Months Plan)  2 program number means Trial Plan 21 Days ."
#             print(req)
#             answer = chatGPT.ask(previous_results, req)
#             dispatcher.utter_message(text = answer)
#         else:
#             req="Data is not availbe with this program number please recheck it and try again.."
#             dispatcher.utter_message(text = req)

#         return []



class ActionShowDetail(Action):
    def name(self) -> Text:
        return "action_show_details"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        program_number = tracker.latest_message["text"]
        print(program_number)

        program_number=int(program_number)
        if program_number>=0 and program_number<3:
            df = pd.read_csv("/home/bluebash-005/code/bluebash/rasa chatbot/zappy/actions/weight_management_plans.csv")
            if program_number==0:
                result = df[df['Plan Duration'] == "6 Months Plan"]
            elif program_number==1:
                result = df[df['Plan Duration'] == "3 Months Plan"]
            else:
                result = df[df['Plan Duration'] == "Trial Plan 21 Days"]
            result_dict = result.to_dict(orient='records')
            text_data = ""
            for item in result_dict:
                for key, value in item.items():
                    text_data += f"{key}: {value}\n"

            print(text_data)
            dispatcher.utter_message(text = text_data)
        else:
            result="Data is not available with this program number please recheck it and try again.."
            dispatcher.utter_message(text = result)
        

        return []


class ActionOrderDetails(Action):

    def name(self) -> Text:
        return "action_order_details"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tracking_number_slot = next(tracker.get_latest_entity_values("tracking_number"), None)
        tracking_number = tracker.get_slot("tracking_number") or tracking_number_slot


        data=self.get_data(tracking_number)
        res=f"The tracking number is: {tracking_number} and the related information for this order is \n{data}"
        dispatcher.utter_message(text=res)

        return []
    

    @staticmethod
    def get_data(tracking_number: str) -> Dict[Text, Any]:
        try:
            df = pd.read_excel("/home/bluebash-005/code/bluebash/rasa chatbot/zappy/actions/TrackingNumberSheet.xlsx", sheet_name='Tracking_Sheet')
            df['Tracking Number'] = df['Tracking Number'].astype(str)
            result = df[df['Tracking Number'] == tracking_number]
            if result.empty:
                return "Data is not availbe with this tracking number please recheck it and try again.."
            first_name =result["First Name"].values[0]
            last_name = result["Last Name"].values[0]
            email = result["Email"].values[0]
            order_date = result["Order date"].values[0]
            medication = result["Medication"].values[0]
            delivery_status = result["Delivery Status"].values[0]
            vial_size = result["Vial size"].values[0]


            formatted_result = (
            f"First name: {first_name}\n"
            f"Last name: {last_name}\n"
            f"Email: {email}\n"
            f"Order date: {order_date}\n"
            f"Medication: {medication}\n"
            f"Delivery status: {delivery_status}\n"
            f"Vial size: {vial_size}\n"
            )
            return formatted_result
        except:
            return "Some issue: with dataframe"
