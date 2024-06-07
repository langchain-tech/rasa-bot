import os
import pandas as pd
import json
import logging
from dotenv import load_dotenv

load_dotenv()
HOME_DIR = os.getenv("HOME_DIR")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import pdb


def extract_rows_excel(email: str):
  file_path = f"{HOME_DIR}/actions/data/dummy_data_200_rows.csv"
  df = pd.read_csv(file_path)
  matching_rows = df[df['Email'] == email]
  logger.info(matching_rows)
  matching_rows_json = matching_rows.to_json(orient='records')  
  matching_rows_dict = json.loads(matching_rows_json)
  logger.info(matching_rows_dict)
  return matching_rows_dict


def extract_name_from_excel(email: str):
    matching_rows = extract_rows_excel(email)
    if matching_rows:
        first_name = matching_rows[0]['First Name']
        last_name = matching_rows[0]['Last Name']
        return f"{first_name} {last_name}"
    else:
        return None