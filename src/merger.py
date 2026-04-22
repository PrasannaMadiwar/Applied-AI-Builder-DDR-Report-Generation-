from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
import base64
model1 = ChatGroq(model="openai/gpt-oss-120b")
model2 = ChatOpenAI(model="gpt-4o-mini")



def incpection_merge(inspection_text,inspection_image):

    prompt3 = f"""You are a Merge Agent for an Inspection Report.

        INPUT:
        - text_diagnosis_json  (from Text Diagnosis Agent)
        - image_diagnosis_json_list (array of Vision Agent outputs for inspection images)

        OBJECTIVE:
        Create a unified, area-wise inspection report by merging text and image diagnoses.

        STRICT RULES:
        - Do NOT hallucinate. Use only provided inputs.
        - Do NOT lose any information.
        - Preserve all image paths exactly.
        - If duplicate issues exist → merge them into one entry.
        - If conflicts exist → record them explicitly in "conflicts".
        - If information is missing → write "Not Available".
        - If uncertain → write "Unclear".
        - Do NOT invent areas; use areas from text_diagnosis_json. If an image has no area, attach it to "Unmapped".

        TASKS:
        1) Normalize area names (e.g., "MB Bedroom" → "Master Bedroom") without changing meaning.
        2) For each area:
        - Merge text observations with image observations.
        - Deduplicate similar issues (same type + location).
        - Attach all relevant image paths to the merged issue.
        3) Map image observations:
        - If an image includes area info → map to that area.
        - Else → place under area "Unmapped".
        4) Capture severity:
        - Prefer explicit severity from text; else use image severity; else "Not Available".
        5) Capture conflicts:
        - Example: text says dampness, image shows no visible issue.
        6) Collect general notes and missing information.

        OUTPUT FORMAT (STRICT JSON ONLY):

        {{
        "source": "inspection_merged",
        "areas": [
            {{
            "area": "",
            "observations": [
                {{
                "issue_type": "Dampness | Crack | Leakage | Tile Gap | Stain | Other",
                "description": "",
                "severity": "Low | Medium | High | Not Available",
                "evidence": {{
                    "text": [],
                    "images": []
                }},
                "confidence": "High | Medium | Low"
                }}
            ]
            }}
        ],
        "unmapped_images": [
            {{
            "image": "",
            "observations": []
            }}
        ],
        "conflicts": [
            {{
            "area": "",
            "detail": ""
            }}
        ],
        "general_notes": [],
        "missing_information": []
        }}

        IMPORTANT:
        - Output JSON only.
        - Ensure every image path from input appears either under an area or in "unmapped_images".
        - Keep language simple and client-friendly.
        
        Input JSONs:
        text_diagnosis_json:
        {inspection_text}

        image_diagnosis_json
        {inspection_image}
        
        """

    result2 = model2.invoke(prompt3)
    return result2.content



def thermal_merger(thermal_text, thermal_image):

    prompt3 = f"""You are a Merge Agent for a Thermal Report.

    INPUT:
    - text_diagnosis_json  (from Thermal Text Diagnosis Agent)
    - image_diagnosis_json_list (array of Vision Agent outputs for thermal images)

    OBJECTIVE:
    Create a unified thermal analysis by combining readings and visual patterns.

    STRICT RULES:
    - Do NOT hallucinate. Use only provided inputs.
    - Do NOT invent numeric values.
    - Preserve all image paths exactly.
    - If values conflict → record in "conflicts".
    - If area is not specified → "Not Clearly Identified".
    - If information is missing → "Not Available".
    - Interpret conservatively.

    TASKS:
    1) For each image:
    - Combine text readings (hotspot/coldspot) with visual analysis (pattern, issue).
    2) Prefer explicit numeric values from text; if absent, use only what is visible.
    3) Derive interpretation:
    - Cold region → possible moisture/leakage
    - Hot region → possible heat loss/insulation issue
    - Uniform → likely no significant anomaly
    4) Assign confidence:
    - High: consistent text + image
    - Medium: partial match
    - Low: unclear/weak signal
    5) Keep each image as a separate observation entry.
    6) Capture conflicts and missing info.

    OUTPUT FORMAT (STRICT JSON ONLY):

    {{
    "source": "thermal_merged",
    "observations": [
        {{
        "image": "",
        "hotspot": "Not Available",
        "coldspot": "Not Available",
        "pattern": "Uniform | Localized Variation | Unclear",
        "interpretation": "",
        "possible_issue": "Moisture | Leakage | Heat Loss | No Significant Issue | Unclear",
        "confidence": "High | Medium | Low",
        "area": "Not Clearly Identified"
        }}
    ],
    "conflicts": [
        {{
        "image": "",
        "detail": ""
        }}
    ],
    "general_notes": [],
    "missing_information": []
    }}

    IMPORTANT:
    - Output JSON only.
    - Ensure every image from input is present in "observations".
    - Do not exaggerate conclusions.
    
    Input JSONs:
    -text_diagnosis_json:
    {thermal_text}

    -image_diagnosis_json
    {thermal_image}
    

    """

    result2 = model2.invoke(prompt3)
    return result2.content