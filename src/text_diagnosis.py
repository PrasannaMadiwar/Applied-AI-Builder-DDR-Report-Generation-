from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
import base64
model1 = ChatGroq(model="openai/gpt-oss-120b")
model2 = ChatOpenAI(model="gpt-4o-mini")






def report_text_diagnosis(text_context):
    report_prompt = f"""You are a Text Diagnosis Agent for structural inspection reports.

    INPUT:
    You will receive raw extracted text from an inspection PDF along with image paths already mapped to sections.

    OBJECTIVE:
    Convert the raw text into a clean, structured, area-wise diagnostic JSON.
    Improve clarity and structure WITHOUT changing meaning.
    DO NOT lose any information.
    DO NOT hallucinate.

    STRICT RULES:
    - Only use information present in the input
    - If something is missing → write "Not Available"
    - If information is unclear → write "Unclear"
    - Do NOT assume or infer beyond given text
    - Preserve all image paths exactly as provided
    - Do NOT remove or rename image paths
    - Do NOT merge unrelated areas
    - Avoid duplication
    - Keep language simple and client-friendly

    TASKS:
    1. Identify all areas (Hall, Bedroom, Kitchen, etc.)
    2. Extract observations/issues per area
    3. Clean and standardize descriptions
    4. Attach corresponding image paths to correct areas
    5. Identify any mentioned causes (if explicitly present)
    6. Identify severity hints ONLY if clearly mentioned
    7. Capture missing or unclear information

    OUTPUT FORMAT (STRICT JSON ONLY):

    {{
    "source": "inspection",
    "areas": [
        {{
        "area": "",
        "observations": [
            {{
            "issue": "",
            "description": "",
            "severity_hint": "Low | Medium | High | Not Available",
            "images": []
            }}
        ]
        }}
    ],
    "general_notes": [],
    "missing_information": []
    }}

    IMPORTANT:
    - Do not add extra fields
    - Do not output anything except JSON
    - Ensure no data loss from input

    Extracted text:
    {text_context}

    """
    result = model2.invoke(report_prompt)
    return result.content


def thermal_text_diagnosis(text_context):
    prompt = f""" 
    You are a Thermal Analysis Diagnosis Agent.

    INPUT:
    You will receive raw extracted text from a thermal report PDF along with image paths.

    OBJECTIVE:
    Convert thermal readings and observations into structured insights.
    Focus on temperature interpretation and possible issue indicators.
    DO NOT hallucinate.

    STRICT RULES:
    - Only use values explicitly present (hotspot, coldspot, emissivity, etc.)
    - Do NOT invent causes unless logically derivable (e.g., coldspot → possible moisture)
    - If unsure → mark "Low Confidence"
    - If area is not mentioned → "Not Clearly Identified"
    - Preserve all image paths exactly
    - Do NOT drop any readings

    TASKS:
    1. Extract thermal readings (hotspot, coldspot, etc.)
    2. Interpret temperature differences
    3. Identify possible issue indicators (moisture, leakage, heat loss)
    4. Assign confidence level (High/Medium/Low)
    5. Attach image paths

    OUTPUT FORMAT (STRICT JSON ONLY):

    {{
    "source": "thermal",
    "observations": [
        {{
        "image": "",
        "hotspot": "",
        "coldspot": "",
        "interpretation": "",
        "possible_issue": "",
        "confidence": "High | Medium | Low",
        "area": "Not Clearly Identified"
        }}
    ],
    "general_notes": [],
    "missing_information": []
    }}

    IMPORTANT:
    - Do not output anything except JSON
    - Keep interpretations grounded in data
    - Do not exaggerate conclusions

    Extratced text:
    {text_context}
    """
    result = model2.invoke(prompt)
    return result.content

