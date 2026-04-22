from src.workflow_graph import workflow 
from jinja2 import Template
import webbrowser
import json





def main():
      
    res = workflow.invoke({
        "inspection_path" : "Sample Report.pdf",
        "thermal_path"  : "Thermal Images.pdf"
    })
     
    with open("json/ddr.json") as f:
        data = json.load(f)

    with open("Report/template.html") as f:
        template = Template(f.read())

    html = template.render(
        summary=data.get("property_issue_summary"),
        areas=data.get("areas"),
        additional_notes=data.get("additional_notes"),
        missing_information=data.get("missing_information"),
        conflicts=data.get("conflicts")
    )

    with open("report.html", "w") as f:
        f.write(html)
     
    webbrowser.open("report.html")    


if __name__ == "__main__":
    main()
