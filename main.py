import os
from pathlib import Path

import google.generativeai as genai

from api import get_mp3_from_text
from model import get_model, upload_to_gemini
from utils import list_files_in_folder, wait_for_files_active

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

cwd = Path(__file__).parent

files = list_files_in_folder(cwd / "data")

# TODO Make these files available on the local file system

uploaded_file_response_list = [
    upload_to_gemini(file, mime_type="application/pdf") for file in files
]

model = get_model()

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(uploaded_file_response_list)


chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                uploaded_file_response_list[0],
                "Summarise the data in Dallas",
            ],
        },
        {
            "role": "model",
            "parts": [
                "ZONDA AI here, your BTR market analyst.\n\nDallas is a strong BTR market, ranking second only to Phoenix. Here's a summary:\n\n* **Strong Growth:** Expects 102% growth in BTR units by 2025.  Ranks second for total BTR units (active, under construction, and future).\n* **High Demand:** Currently represents  6.3% of the total rental market, with this number expected to increase.\n* **Construction & Investment:** Large share of units under construction (13,207). Institutional investors are highly active, particularly in the entry-level and move-up segments.\n* **Unit Breakdown:**\n    * Active Units: 6,378\n    * Under Construction: 13,207\n    * Future Pipeline: 6,147\n* **Key Players:** Phoenix, Atlanta, and Dallas are the top 3 markets for future BTR community growth.\n\nOverall, Dallas presents a significant opportunity for BTR investors and developers due to its strong growth potential and renter demand.\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "show me the dallas data as a graph\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Unfortunately, I can't create visual graphs directly from the text data. I can generate responses in textual format only. \n\nHowever, I can help you understand how to represent the Dallas BTR data you requested in a graph:\n\n**Graph Idea 1:  BTR Unit Growth in Dallas (2023-2025)**\n\n* **Graph Type:** Bar Graph\n* **X-Axis:** Years (2023, 2024, 2025) \n* **Y-Axis:** Number of BTR Units\n* **Data to Plot:**\n    * Start with the 2023 baseline of active BTR units in Dallas (6,378). \n    * Add the under-construction units (13,207) over the next two years (assuming even distribution).\n    * Add a portion of the future pipeline units (6,147) over the two years based on a reasonable conversion rate.\n\n**Graph Idea 2:  Breakdown of Dallas BTR Units by Status (Current)**\n\n* **Graph Type:** Pie Chart\n* **Slices:** Active, Under Construction, Future Pipeline\n* **Data to Plot (as percentages of the total):**\n    * Active Units: 6,378 (calculate percentage)\n    * Under Construction: 13,207 (calculate percentage)\n    * Future Pipeline: 6,147 (calculate percentage)\n\nYou could create these graphs in a spreadsheet program or data visualization tool. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "show me the dallas data as a table\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Here's the Dallas BTR data presented as a table:\n\n| Category               | Dallas |\n| ------------------------ | ------ |\n| Total BTR Units (Projected 2025) | 21,122 |\n| Active BTR Units (2023) | 6,378  |\n| Under Construction Units | 13,207 |\n| Future Pipeline Units   | 6,147  |\n| BTR Market Share (2023)  | 6.3%   |\n\n**Note:**  The Total BTR Units projection for 2025 is based on the data provided in the document, which might not account for unforeseen market changes or project delays. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "what is the source of this data\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "The source of the data, as stated multiple times throughout the provided PDF content, is **Zonda** itself. \n\nIt's mentioned in these contexts:\n\n* **Data source:** Found next to charts and graphs.\n* **Zonda's BTR database:**  Mentions their internal database as the source for BTR unit and community count growth rates.\n* **Zonda's proprietary tracking methodology:** Used for identifying the conversion of communities from for-sale to for-rent.\n* **Zonda Research team:**  Conducts tracking of active and future BTR projects.\n* **Zonda Portal:** A platform where more detailed project-specific data is available for download.\n\nTherefore, the accuracy and reliability of the data rely on Zonda's data collection, analysis, and modeling processes. \n",
            ],
        },
    ]
)

response = chat_session.send_message("Í")

print(response.text)
