# 🏗️ Detailed Diagnosis Report (DDR) Generation — Agentic AI System
 
> An agentic AI pipeline that transforms raw property inspection and thermal imaging PDFs into structured, client-ready Detailed Diagnosis Reports (DDR) — automatically.
 
---
 
## 📌 Overview
 
Property inspection workflows typically produce two separate technical documents:
 
- **Inspection Report** — containing area-wise observations with photos of impacted zones
- **Thermal Diagnosis Report** — containing thermal imaging data of the property
Manually synthesizing these into a single client-ready report is time-consuming and error-prone. This project automates that entire process using a **multi-agent LangGraph pipeline** that extracts, analyzes, merges, and renders a professional DDR — complete with images, severity ratings, root cause analysis, and recommendations.
 
---
 
## 🧠 Agentic Architecture
 
The system runs **two parallel workflows** — one for each input PDF — that later converge into a final reasoning agent.
 
![Agentic Workflow](agentic%20workflow.png) 
 
 
### Node-by-Node Breakdown
 
**1. Extraction Nodes (Impact & Thermal)**
- Uses `PyMuPDF4LLM` to extract both text and images from each PDF
- Text is structured as a page-indexed list: `[{page: N, content: "..."}]`
- Images are saved to dedicated folders (`/inspection_images/`, `/thermal_images/`)
- Feeds two parallel sub-agents per workflow
**2. Image-Based Agent**
- Receives all extracted images
- Generates a detailed JSON summary for each image — identifying visible damage, material condition, and anomalies
- Output: structured JSON per image
**3. Text-Based Agent**
- Receives page-indexed text content
- Cleans, normalizes, and converts it into valid JSON
- Makes downstream parsing reliable for the merge step
**4. Merge Agent**
- Combines outputs from the Image Agent and Text Agent
- Merges without hallucination — no new information is introduced
- Matches each image to its correct folder path (as provided by PyMuPDF)
- Output: single unified JSON per PDF
**5. Final Reasoning Agent**
- Receives both merged JSONs (inspection + thermal)
- Cross-references and compares findings from both sources
- Generates the final DDR with:
  - Property summary
  - Area-wise observations (description, thermal insights, root cause, severity, recommended actions)
  - Associated images per area
  - Additional notes and conflict flags
- Output: final structured JSON saved to `/json/`
**6. Save Node + HTML Rendering**
- Persists the final JSON
- Rendered into a client-facing HTML report via a Django template (`report.html`)
---
 
## 🗂️ Repository Structure
 
```
├── src/                    # Core agent and graph logic
├── json/                   # Final output JSON files
├── Report/                 # Generated HTML reports
├── main.py                 # Entry point
├── report.html             # Django HTML template for rendering
├── testing.ipynb           # Notebook for development & testing
├── Sample Report.pdf       # Sample inspection input PDF
├── Thermal Images.pdf      # Sample thermal input PDF
├── agentic workflow.png    # Visual diagram of the pipeline
└── pyproject.toml          # Project dependencies (uv)
```
 
---
 
## ⚙️ Tech Stack
 
| Layer | Technology |
|---|---|
| Agent Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM Integration | [LangChain OpenAI](https://github.com/langchain-ai/langchain) |
| PDF Parsing | [PyMuPDF4LLM](https://pymupdf.readthedocs.io/) |
| Report Rendering | Django + HTML Template |
| Package Manager | [uv](https://github.com/astral-sh/uv) |
| Language | Python ≥ 3.13 |
 
---
 
## 🚀 Getting Started
 
### Prerequisites
 
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
### Installation
 
```bash
# Clone the repository
git clone https://github.com/PrasannaMadiwar/Applied-AI-Builder-DDR-Report-Generation-.git
cd Applied-AI-Builder-DDR-Report-Generation-
 
# Install dependencies using uv
uv sync
```
 
### Configuration
 
Set your OpenAI API key as an environment variable:
 
```bash
export OPENAI_API_KEY="your-api-key-here"
```
 
### Running the Pipeline
 
```bash
uv run python main.py
```
 
The pipeline takes approximately **3–4 minutes** to complete for a standard property report. The final JSON output is saved to `/json/` and the rendered HTML report is available in `/Report/`.
 
---
 
## 📊 Sample Output
 
The generated DDR includes:
 
- **Property Summary** — 2–3 sentence high-level overview
- **Area-wise Observations** — per room/zone breakdown with:
  - Description of damage or issue
  - Thermal insights (from thermal report)
  - Probable root cause
  - Severity: `Low` / `Medium` / `High`
  - Recommended actions
  - Associated inspection images
- **Additional Notes** — conflicts, missing data, unclear findings
---
 
## ⚠️ Known Limitations & Recommendations for Input PDFs
 
Based on testing, the accuracy of the output improves significantly when input PDFs follow these guidelines:
 
**Inspection Report:**
- Each impacted area (e.g., Parking Area C) should be **fully contained within a single page** — including both the description and its associated images. The current system extracts images per page; content that spans two pages may result in missing image associations.
**Thermal Report:**
- Each thermal image should be **explicitly labeled** with the room/area name (e.g., "Master Bedroom — Thermal Scan"). Without spatial labels, the reasoning agent cannot precisely map thermal findings to physical locations.
---
 
## 🔮 Future Improvements
 
- Cross-page content linking for inspection reports
- Automated spatial labeling for thermal image regions
- Django web interface for uploading PDFs and viewing reports
- Support for multi-floor / multi-unit properties
---
 
## 👤 Author
 
**Prasanna Madiwar**  
[GitHub](https://github.com/PrasannaMadiwar)
 
---