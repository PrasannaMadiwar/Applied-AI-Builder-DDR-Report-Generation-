import json
from langchain_core.utils.json import parse_json_markdown


def save_json(ddr_output:str):
    parsed_json = parse_json_markdown(ddr_output)

    with open("json/ddr.json", "w") as file:
        json.dump(parsed_json, file, indent=4)


        