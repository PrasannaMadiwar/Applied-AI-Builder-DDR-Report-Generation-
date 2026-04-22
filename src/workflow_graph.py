from src.extractor import extract_text_images
from src.text_diagnosis import report_text_diagnosis, thermal_text_diagnosis
from src.image_dignosis import impact_image_diagnosis, thermal_image_diagnosis
from src.merger import incpection_merge, thermal_merger
from src.ddr import ddr_agent
from src.state import DDRState
from src.last_node import save_json


from langgraph.graph import StateGraph, START, END

def impact_extraction(state:DDRState) -> DDRState:
    file_path = state['inspection_path']
    text_context = extract_text_images(doc_path=file_path,image_folder="inspect")
    return {
        'raw_inspection_text' : text_context
    }



def thermal_extraction(state:DDRState) -> DDRState:
    file_path = state['thermal_path']
    text_context = extract_text_images(doc_path=file_path,image_folder="thermal")
    return {
        'raw_thermal_text' : text_context
    }


def impact_text(state:DDRState) -> DDRState:
    text_context = state['raw_inspection_text']
    result = report_text_diagnosis(text_context=text_context)
    return{
        'inpection_text_dignosis':result
    }



def impact_image(state:DDRState) -> DDRState:
    file_path = state['inspection_path']
    result = impact_image_diagnosis(file_path=file_path)
    return {
        'inspection_image_dignosis':result
    }


def thermal_text(state:DDRState) -> DDRState:
    text_context = state['raw_thermal_text']
    result = thermal_text_diagnosis(text_context)
    return{
        'thermal_text_dignosis':result
    }


def thermal_image(state:DDRState) -> DDRState:
    file_path = state['thermal_path']
    result = thermal_image_diagnosis(file_path=file_path)
    return {
        'thermal_image_diagnosis':result
    }

def impact_merge(state:DDRState) -> DDRState:
    text = state['inpection_text_dignosis']
    image = state['inspection_image_dignosis']
    result = incpection_merge(inspection_text=text,inspection_image=image)
    return {
        'inspection_merge':result
    }
 
def thermal_merge(state:DDRState) -> DDRState:
    text = state['thermal_text_dignosis']
    image = state['thermal_image_diagnosis']
    result = thermal_merger(thermal_text=text,thermal_image=image)
    return {
        'thermal_merge':result
    }

def  resoning_agent(state:DDRState) -> DDRState:
    impact = state['inspection_merge']
    thermal = state['thermal_merge']
    result = ddr_agent(inspection_merged=impact, thermal_merged=thermal)
    return {
        'ddr_report':result
    }

def save_report(state:DDRState) -> DDRState:
    output = state['ddr_report']
    save_json(output)
    return {}



graph = StateGraph(DDRState)

graph.add_node("impact_extraction", impact_extraction)
graph.add_node("impact_text", impact_text)
graph.add_node("impact_image", impact_image)
graph.add_node("impact_merge", impact_merge)
 
graph.add_node("thermal_extraction", thermal_extraction)
graph.add_node("thermal_text", thermal_text)
graph.add_node("thermal_image", thermal_image)
graph.add_node("thermal_merge", thermal_merge)

 
graph.add_node("reasoning_agent", resoning_agent)
graph.add_node("save",save_report)


graph.add_edge(START,'impact_extraction')
graph.add_edge(START,'thermal_extraction')

graph.add_edge("impact_extraction","impact_text")
graph.add_edge("impact_extraction","impact_image")
graph.add_edge("impact_text","impact_merge")
graph.add_edge("impact_image","impact_merge")


graph.add_edge("thermal_extraction","thermal_text")
graph.add_edge("thermal_extraction","thermal_image")
graph.add_edge("thermal_text","thermal_merge")
graph.add_edge("thermal_image","thermal_merge")

graph.add_edge("impact_merge","reasoning_agent")
graph.add_edge("thermal_merge","reasoning_agent")

graph.add_edge("reasoning_agent","save")
graph.add_edge("save",END)

workflow = graph.compile()
