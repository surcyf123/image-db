# import wandb
# import pandas as pd

# api = wandb.Api()
# username = "username here"
# project_name = "project name here"
# run_name = "run name here"
# # run = api.run(f"/{username}/{project_name}/runs/{run_name}")
# run = api.run("/cortex-t/synthetic-QA/runs/amczp753")
# history = run.history()

# # Write the history to a file in JSON format using pandas
# history.to_json('run_history.json', orient='records', lines=True, indent=4)

# print("History has been saved to run_history.json")

import wandb
import os
import json
import concurrent.futures

def download_image(file, run_id, root="wandb_images"):
    # Construct the full path for the image file
    file_path = os.path.join(root, file.name)

    # Check if the file already exists
    if not os.path.exists(file_path):
        file.download(root=root)
        print(f"Downloaded {file.name} from run {run_id}")
    else:
        print(f"{file.name} already exists, skipping download.")

    return file.name

# Initialize wandb API
api = wandb.Api()

# Define your project path
project_path = "cortex-t/synthetic-QA"

# Create a directory to store images
os.makedirs("wandb_images", exist_ok=True)

# Fetch all runs from the project
project_runs = api.runs(project_path)

# Set the number of threads for parallel downloads
num_threads = 10  # Adjust as necessary

image_names = []

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = []
    for run in project_runs:
        if run.config.get('version') == '1.1.0':
            for file in run.files():
                if file.name.endswith(".png") or file.name.endswith(".jpg"):
                    future = executor.submit(download_image, file, run.id)
                    futures.append(future)

    # Collecting image names from futures
    for future in concurrent.futures.as_completed(futures):
        image_names.append(future.result())

# Write the image names to a JSON file
with open('image_list.json', 'w') as f:
    json.dump(image_names, f)

print("All relevant images have been downloaded and image_list.json has been created.")
