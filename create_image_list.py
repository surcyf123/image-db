import os
import json

# Path to your images directory
image_dir = "wandb_images/media/images/"

# List all files in the directory
file_list = os.listdir(image_dir)

# Filter out only image files (e.g., .png, .jpg)
image_files = [file for file in file_list if file.endswith('.png') or file.endswith('.jpg')]

# Write the list of image files to image_list.json
with open('image_list.json', 'w') as f:
    json.dump(image_files, f)

print("image_list.json has been created.")