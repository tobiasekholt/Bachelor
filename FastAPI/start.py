import subprocess
from pathlib import Path

# get the absolute path to the directory containing start.py
root_dir = Path(__file__).resolve().parent.parent

# construct the paths to the ngisopenapi and kartAI directories
ngisopenapi_dir = root_dir / 'ngisopenapi'
kartAI_dir = root_dir / 'kartAI'

# execute the commands
subprocess.call(['cmd.exe', '/c', f'cd {ngisopenapi_dir} && conda activate venv && python demo.py && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', f'cd {kartAI_dir} && conda activate gdal_env && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', f'cd {kartAI_dir} && conda activate gdal_env && kai.bat train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json'])
