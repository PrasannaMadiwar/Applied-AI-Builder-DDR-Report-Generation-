import os
import pymupdf4llm
import shutil

def extract_text_images(doc_path:str,image_folder:str):
    
    if os.path.exists(image_folder):
        shutil.rmtree(image_folder)

    os.makedirs(image_folder, exist_ok=True)   
    data = pymupdf4llm.to_markdown(
        doc=doc_path,
        page_chunks=True,        
        write_images=True,       
        image_path=image_folder
    )
    
     

    return data