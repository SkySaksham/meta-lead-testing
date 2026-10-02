import os
import requests
from dotenv import load_dotenv

load_dotenv()

META_GRAPH_URL = "https://graph.facebook.com/v26.0"
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")


def get_lead_details(leadgen_id: str) -> dict:
    """
    Fetches lead data from Meta Graph API by leadgen_id
    and returns a dict with name, phone, and email.
    """
    url = f"{META_GRAPH_URL}/{leadgen_id}"

    response = requests.get(
        url,
        params={"access_token": META_ACCESS_TOKEN},
    )

    print("Meta status:", response.status_code)
    print("Meta response:", response.json())

    if response.status_code != 200:
        return None

    lead_data = response.json()
    field_data = lead_data.get("field_data", [])

    # Build a lookup from field name -> first value
    fields = {
        item["name"]: item["values"][0]
        for item in field_data
        if item.get("values")
    }

    return {
        "name": fields.get("full_name"),
        "phone": fields.get("phone_number"),
        "email": fields.get("email"),
    }
