
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import pdb

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
