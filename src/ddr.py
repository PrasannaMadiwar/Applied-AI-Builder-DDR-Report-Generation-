from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
import base64
model1 = ChatGroq(model="openai/gpt-oss-120b")
model2 = ChatOpenAI(model="gpt-4o-mini")



def ddr_agent(inspection_merged, thermal_merged):

    prompt4 = f"""
    You are a DDR (Detailed Diagnostic Report) Generation Agent.

    INPUT:
    You will receive:
    1. inspection_merged_json  (merged output of inspection text + images)
    2. thermal_merged_json    (merged output of thermal text + images)

    OBJECTIVE:
    Generate a final, structured, client-ready DDR report by combining both inputs.

    STRICT RULES:
    - Do NOT hallucinate
    - Do NOT invent facts or causes
    - Use ONLY provided data
    - If information is missing → write "Not Available"
    - If data conflicts → explicitly mention in "conflicts"
    - Avoid duplicate points
    - Keep language simple and client-friendly
    - Preserve all image paths exactly
    - Ensure images support the corresponding observations
    - Do NOT drop any critical information

    ---

    TASKS:

    1. PROPERTY ISSUE SUMMARY
    - Provide a concise & detailed overview of major issues across the property
    - Base only on repeated or significant observations

    ---

    2. AREA-WISE OBSERVATIONS
    For each area (Hall, Bedroom, Kitchen, etc.):
    - Merge inspection + thermal findings
    - Avoid duplication
    - Attach relevant images
    - If thermal data not mapped → include only inspection
    - If area unclear → "Not Clearly Identified"

    Each observation must include:
    - issue
    - description(4-5 lines)
    - supporting evidence (text + thermal insight)
    - image paths

    ---

    3. PROBABLE ROOT CAUSE
    - Only if logically supported by BOTH sources or clearly stated
    - If not enough data → "Not Available"

    ---

    4. SEVERITY ASSESSMENT (WITH REASONING)
    - Assign: Low / Medium / High
    - Based on:
    - frequency of issue
    - structural impact (crack vs stain)
    - thermal anomaly strength
    - Provide reasoning

    ---

    5. RECOMMENDED ACTIONS
    - Suggest practical fixes based ONLY on identified issues
    - Keep simple (repair leakage, seal joints, etc.)
    - Do NOT suggest advanced engineering unless clearly needed

    ---

    6. ADDITIONAL NOTES
    - General observations
    - Patterns (e.g., multiple dampness areas)

    ---

    7. MISSING OR UNCLEAR INFORMATION
    - Explicitly list:
    - missing values
    - unclear mappings
    - unavailable images

    ---

    8. CONFLICTS
    - Clearly mention contradictions between inspection and thermal data

    ---

    OUTPUT FORMAT (STRICT JSON ONLY):

    {{
    "property_issue_summary": "",
    "areas": [
        {{
        "area": "",
        "observations": [
            {{
            "issue": "",
            "description": "",
            "thermal_insight": "Not Available",
            "root_cause": "Not Available",
            "severity": {{
                "level": "Low | Medium | High",
                "reason": ""
            }},
            "recommended_action": "",
            "images": []
            }}
        ]
        }}
    ],
    "additional_notes": [],
    "missing_information": [],
    "conflicts": []
    }}

    ---

    IMPORTANT:
    - Output ONLY JSON (no explanation)
    - Ensure every image path from inputs appears in relevant sections
    - Do NOT duplicate the same issue multiple times
    - Maintain logical consistency
    - Keep wording clear and client-friendly

    Input JSONs:

    -inspection_merged_json:
    {inspection_merged}

    -thermal_merged_json
    {thermal_merged}


    """


    result4 = model2.invoke(prompt4)
    return result4.content


