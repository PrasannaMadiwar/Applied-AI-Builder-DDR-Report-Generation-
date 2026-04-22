from typing import TypedDict

class DDRState(TypedDict):
    
    inspection_path : str
    thermal_path : str
    raw_inspection_text : str
    raw_thermal_text : str
    inpection_text_dignosis : str
    inspection_image_dignosis : str
    thermal_text_dignosis : str
    thermal_image_diagnosis : str
    inspection_merge : str
    thermal_merge : str
    ddr_report : str
