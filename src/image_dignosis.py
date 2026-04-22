from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
import base64
model1 = ChatGroq(model="openai/gpt-oss-120b")
model2 = ChatOpenAI(model="gpt-4o-mini")



def encode_pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')
    


def impact_image_diagnosis(file_path:str):

    pdf_b64 = encode_pdf_to_base64(file_path=file_path)

    prompt ="""You are a Vision Diagnosis Agent for structural inspection images.

        INPUT:
        You will receive:
        - One pdf consist of many images 
        - The image file path (must be preserved)
        - Optional context text (may or may not be accurate)

        OBJECTIVE:
        for all images in pdf "Analyze the image and extract ONLY visible, verifiable structural issues.
        Do NOT hallucinate or assume anything not clearly visible".

        STRICT RULES:
        - Only describe what is visually observable
        - Do NOT infer hidden causes unless clearly supported
        - If unsure → mark "Unclear"
        - If nothing significant → "No Visible Issue"
        - Preserve the exact image path
        - Do NOT rename or modify image path
        - Do NOT use technical jargon unnecessarily
        - Keep descriptions simple and client-friendly

        TASKS:
        1. Identify visible issues (dampness, cracks, leakage marks, tile gaps, etc.)
        2. Describe the issue clearly
        3. Estimate severity visually (Low / Medium / High)
        4. Classify issue type
        5. Assign confidence level

        OUTPUT FORMAT (STRICT JSON ONLY) for each images:

        {
        "source": "inspection_image",
        "image": "",
        "observations": [
            {
            "issue_type": "Dampness | Crack | Leakage | Tile Gap | Stain | No Visible Issue | Unclear",
            "description": "",
            "severity": "Low | Medium | High | Not Available",
            "confidence": "High | Medium | Low"
            }
        ]
        }

        IMPORTANT:
        - Do not output anything except JSON
        - Do not assume area unless explicitly visible or provided
        - Do not fabricate details"""
        
    message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "file",
                    "file": {
                        "filename": "document.pdf",
                        "file_data": f"data:application/pdf;base64,{pdf_b64}"
                    }
                }
            ]
        )

    result1 = model2.invoke([message])

    return result1.content



def thermal_image_diagnosis(file_path:str):
    
    pdf_b64 = encode_pdf_to_base64(file_path=file_path)

    prompt ="""You are a Thermal Vision Analysis Agent.

        INPUT:
        You will receive:
        - One pdf consist of many images 
        - The image file path (must be preserved)
        - Optional extracted values (hotspot, coldspot)

        OBJECTIVE:
        For all images "Analyze the thermal image and identify temperature patterns and possible issues".

        STRICT RULES:
        - Use visible thermal patterns (color differences, gradients)
        - If hotspot/coldspot values are visible → extract them
        - Do NOT invent numeric values
        - Interpret conservatively
        - If unsure → mark "Low Confidence"
        - If no clear anomaly → "No Significant Thermal Anomaly"
        - Preserve image path exactly

        TASKS:
        1. Identify temperature variation (hot vs cold regions)
        2. Extract hotspot/coldspot if visible
        3. Interpret pattern (uniform / localized variation)
        4. Identify possible issue:
        - Moisture / Leakage (cold regions)
        - Heat loss / insulation issue (hot regions)
        - No anomaly
        5. Assign confidence level

        OUTPUT FORMAT (STRICT JSON ONLY) for each image:

        {
        "source": "thermal_image",
        "image": "",
        "hotspot": "Not Available",
        "coldspot": "Not Available",
        "pattern": "Uniform | Localized Variation | Unclear",
        "interpretation": "",
        "possible_issue": "Moisture | Leakage | Heat Loss | No Significant Issue | Unclear",
        "confidence": "High | Medium | Low",
        "area": "Not Clearly Identified"
        }

        IMPORTANT:
        - Do not output anything except JSON
        - Do not exaggerate conclusions
        - Do not assume area if not given"""

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "file",
                "file": {
                    "filename": "document.pdf",
                    "file_data": f"data:application/pdf;base64,{pdf_b64}"
                }
            }
        ]
    )


    result1 = model2.invoke([message])
    return result1.content
