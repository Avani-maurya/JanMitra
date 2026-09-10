"""
JanMitra AI - Civic Reporting AI Module
Phase 3: Optional image analysis (FREE VERSION - uses Google Gemini)

analyze_complaint() accepts an optional image_path. If an image is given,
Gemini looks at BOTH the photo and the complaint text together and
produces one combined analysis. If no image is given, it's text-only.
"""

import json
import os
from typing import Literal, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()

MODEL_NAME = "gemini-3.6-flash"


class ComplaintAnalysis(BaseModel):
    category: Literal[
        "Pothole", "Road Damage", "Garbage/Waste", "Street Light",
        "Water Leakage", "Sewage", "Drainage", "Other"
    ] = Field(description="The type of civic issue being reported")

    severity: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="How urgent/dangerous the issue is"
    )

    department: Literal[
        "Road Department", "Sanitation Department", "Water Department",
        "Electricity Department", "Municipal Corporation"
    ] = Field(description="The municipal department responsible for handling this")

    priority: int = Field(
        description="A priority score from 0 (lowest) to 100 (highest/most urgent)"
    )

    summary: str = Field(
        description="A concise, one-line summary of the complaint in plain English"
    )

    suggested_action: str = Field(
        description="A short recommendation for what the department should do"
    )

    confidence: int = Field(
        description="The AI's confidence in this analysis, from 0 to 100"
    )


def analyze_complaint(complaint_text: str, image_path: Optional[str] = None) -> dict:
    """
    Sends a citizen's complaint (and optionally a photo) to Gemini and
    returns a structured Python dictionary matching ComplaintAnalysis.
    """
    if image_path:
        prompt = f"""You are an AI assistant for a civic complaint system used by a municipal corporation in India.

A citizen has submitted a complaint along with a photo of the issue.
Use BOTH the photo and the text together to make one combined, final assessment.
If the photo and text seem to disagree, use your judgement to decide which
signal is more reliable and explain your reasoning through your chosen field values.

Complaint text:
"{complaint_text}"
"""
    else:
        prompt = f"""You are an AI assistant for a civic complaint system used by a municipal corporation in India.

Analyze the following citizen complaint and classify it according to the required schema.

Complaint:
"{complaint_text}"
"""

    contents = []
    if image_path:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")
        image = Image.open(image_path)
        contents.append(image)
    contents.append(prompt)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComplaintAnalysis,
        ),
    )

    analysis = ComplaintAnalysis.model_validate_json(response.text)
    return analysis.model_dump()


if __name__ == "__main__":
    sample_complaint = (
        "There is a huge pothole near my college gate. Yesterday a bike almost "
        "crashed because of it, and there is no street light at night."
    )

    print("Complaint:", sample_complaint)
    result = analyze_complaint(sample_complaint)
    print(json.dumps(result, indent=2))
