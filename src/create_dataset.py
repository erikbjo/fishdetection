# File is used to create the dataset for the model, it will create a dataset with the following structure:
#   - datasets
#       - data
#           - train
#               - images
#                   - {date} (folder)
#                       - {image}.png
#                       - {image}.png
#                       - ...
#                   - ...
#               - labels
#                   - {date} (folder)
#                       - {image}.txt with YOLO format: {class} {x_center} {y_center} {width} {height}
#                       - {image}.txt
#                       - ...
#                   - ...
#           - val
#               - ...
# Please only run this script once
# Delete the datasets folder if you want to run this script again, ensure that the data folder is not deleted

import os
import random
import shutil
import zipfile
import xml.etree.ElementTree as ET

percentage_train = 0.8
path_to_data = "../data"
path_to_annotation = os.path.join(path_to_data, "Annotation")
path_to_datasets = "../datasets"
path_to_data_under_datasets = os.path.join(path_to_datasets, "data")
path_to_train = os.path.join(path_to_data_under_datasets, "train")
path_to_images_train = os.path.join(path_to_train, "images")
path_to_labels_train = os.path.join(path_to_train, "labels")
path_to_val = os.path.join(path_to_data_under_datasets, "val")
path_to_images_val = os.path.join(path_to_val, "images")
path_to_labels_val = os.path.join(path_to_val, "labels")


def unzip_folders(source_dir, dest_dir):
    # Remove .DS_Store files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file == ".DS_Store":
                os.remove(os.path.join(root, file))
                print(f"Removed {file}")

    # Iterate over folders in the source directory
    for folder_name in os.listdir(source_dir):
        print("Found folder: ", folder_name)
        folder_path = os.path.join(source_dir, folder_name)
        if folder_path.endswith(".zip"):
            new_folder_name = folder_name.split("-")[1]
            new_dest_dir = os.path.join(dest_dir, new_folder_name)
            # Unzip the folder
            with zipfile.ZipFile(folder_path, "r") as zip_ref:
                zip_ref.extractall(new_dest_dir)
                print(f"Unzipped {folder_name} to {new_dest_dir}")

            # Move the images from new_folder_name -> images, to new_folder_name
            images_folder = os.path.join(new_dest_dir, "images")
            for image in os.listdir(images_folder):
                shutil.move(os.path.join(images_folder, image), new_dest_dir)

            # Remove the images folder
            shutil.rmtree(images_folder)

            # Create a matching folder under labels
            os.makedirs(os.path.join(path_to_labels_train, new_folder_name), exist_ok=True)

            # Not creating labels now, TODO: create labels

def main():
    print("Creating dataset for training and validation")

    # Create the datasets folders
    os.makedirs(path_to_datasets, exist_ok=True)
    os.makedirs(path_to_train, exist_ok=True)
    os.makedirs(path_to_images_train, exist_ok=True)
    os.makedirs(path_to_labels_train, exist_ok=True)
    os.makedirs(path_to_val, exist_ok=True)
    os.makedirs(path_to_images_val, exist_ok=True)
    os.makedirs(path_to_labels_val, exist_ok=True)

    # Unzip the folders and move them to the train folders
    unzip_folders(path_to_annotation, path_to_images_train)


if __name__ == "__main__":
    main()
