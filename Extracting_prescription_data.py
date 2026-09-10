from dotenv import load_dotenv, find_dotenv
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
import location

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


class Handwritting_Extraction:

    def __init__(self):

        load_dotenv(find_dotenv())

        genai.configure(api_key=api_key)

        self.Safety_Settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    def get_system_prompt(self, location_data):

        # Safe Location Handling
        if location_data:
            self.map_link_url = location.get_location(location_data)
        else:
            self.map_link_url = "Not Available"

        self.sys_prompt = f"""
You are an expert-level Medical Data Extraction tool.

Your Task:

1. Perform OCR.
2. Extract medicines.
3. Do not duplicate medicines.
4. Include timings.
5. Add this Map Link:

{self.map_link_url}

6. Patient info compulsory.

Return ONLY JSON.

{{
"patient_info": {{
"patient_name":"...",
"age":"...",
"Date":"..."
}},
"Prescription_info":[
{{
"medications":"",
"Dosage":"",
"Frequency":"",
"Duration":"",
"Map_link":"{self.map_link_url}"
}}
]
}}

If unreadable return:
"Error: Image is unreadable"

If field missing:
"Not provided"
"""

        return self.sys_prompt

    def extracting_presc_data(self, image_file, location_data):

        self.system_prompt = self.get_system_prompt(location_data)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.system_prompt,
            safety_settings=self.Safety_Settings,
        )

        try:

            image = Image.open(image_file)

            if image.width > 1024:

                ratio = 1024 / image.width

                image = image.resize(
                    (
                        1024,
                        int(image.height * ratio),
                    ),
                    Image.LANCZOS,
                )

            response = model.generate_content(
                image,
                stream=True,
            )

            return response

        except Exception as e:

            raise Exception(
                f"Error occured in Extracting prescription data : {e}"
            )