import requests
import time
from pathlib import Path
from tqdm import tqdm

def download_to_local(url:str, out_path:Path,parent_mkdir:bool=True):
    if not isinstance(out_path,Path):
        raise ValueError(f"{out_path} is not a valid path, Provide valid pathlib path")
    if parent_mkdir:
        out_path.parent.mkdir(parents=True,exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
        # write the response to out_path file in binary mode to prevent any newline conversion
        # out_path.write_bytes(response.content)
        
        # implementing of a progress bar
        total_size = int(response.headers.get('content-length',0)) 
        block_size = 1024 # corresponds to 1kb

        with tqdm(total=total_size,unit="iB", unit_scale=True,desc=out_path.name,colour="green",ascii=True) as progress_bar:
            with open(out_path,"wb") as file:
                for data in response.iter_content(chunk_size=block_size):
                    time.sleep(0.00001)
                    progress_bar.update(len(data))
                    file.write(data)
        return True
    except requests.RequestException as e:
        print(f"failled to download from {url}: due to {e}")
        return False
