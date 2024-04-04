# File is used to create the dataset for the model, it will create a dataset with the following structure from root:
#   - data
#       - images
#           - train
#               - folders with images ...
#           - val
#               - folders with images ...
#       - labels
#           - train
#               - folders with labels ...
#           - val
#               - folders with labels ...

# Please only run this script once
# Delete the data folder if you want to run this script again, ensure that the data folder is not deleted

import os
import random
import shutil
import zipfile
import xml.etree.ElementTree as ET

percentage_train = 0.8
path_to_anadrom = "../ANADROM"
path_to_annotation = os.path.join(path_to_anadrom, "Annotation")
path_to_data = "../data"
path_to_images = os.path.join(path_to_data, "images")
path_to_labels = os.path.join(path_to_data, "labels")
path_to_images_train = os.path.join(path_to_images, "train")
path_to_images_val = os.path.join(path_to_images, "val")
path_to_labels_train = os.path.join(path_to_labels, "train")
path_to_labels_val = os.path.join(path_to_labels, "val")


def unzip_all_zips_from_source_to_target(source_dir, dest_dir):
    # Remove .DS_Store files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file == ".DS_Store":
                os.remove(os.path.join(root, file))
                print(f"Removed {file}")

    # Iterate over folders in the source directory
    for folder_name in os.listdir(source_dir):
        # print("Found folder: ", folder_name)

        folder_path = os.path.join(source_dir, folder_name)
        if folder_path.endswith(".zip"):
            new_folder_name = folder_name.split("-")[1]
            new_dest_dir = os.path.join(dest_dir, new_folder_name)
            # Unzip the folder
            with zipfile.ZipFile(folder_path, "r") as zip_ref:
                zip_ref.extractall(new_dest_dir)
                # print(f"Unzipped {folder_name} to {new_dest_dir}")

            # Move the images from new_folder_name -> images, to new_folder_name
            images_folder = os.path.join(new_dest_dir, "images")
            for image in os.listdir(images_folder):
                shutil.move(os.path.join(images_folder, image), new_dest_dir)

            # Remove the images folder
            shutil.rmtree(images_folder)

            # Create a matching folder under labels
            os.makedirs(os.path.join(path_to_labels_train, new_folder_name), exist_ok=True)


def create_labels_from_xml(xml_file, dest_path):
    print("Creating labels from xml file: ", xml_file)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get the original size of the image
    original_size = root.find('./meta/task/original_size')
    original_width = int(original_size.find('width').text)
    original_height = int(original_size.find('height').text)

    for track in root.findall(".//track"):
        for obj in track.findall("box"):
            # print("Found object: ", obj)

            # If outside="1" then skip the object, fish is not inside the box
            if obj.get("outside") == "1":
                continue

            frame_number = obj.get("frame")
            normalised_frame_number = str(int(frame_number)).zfill(6)

            # If we are here, we have a fish object, since we are only checking for fish/not fish, class is 0
            class_name = 0

            # Find the bounding box, inside the box tag as xtl, ytl, xbr, ybr
            xtl = float(obj.get("xtl"))
            ytl = float(obj.get("ytl"))
            xbr = float(obj.get("xbr"))
            ybr = float(obj.get("ybr"))

            # Calculate the center of the bounding box
            x_center = (xtl + xbr) / (2 * original_width)
            y_center = (ytl + ybr) / (2 * original_height)

            # Calculate the width and height of the bounding box
            width = (xbr - xtl) / original_width
            height = (ybr - ytl) / original_height

            # There can be multiple fish in the same frame, so we need to append to the file if it already exists
            if not os.path.exists(os.path.join(dest_path, f"frame_{normalised_frame_number}.txt")):
                with open(os.path.join(dest_path, f"frame_{normalised_frame_number}.txt"), "w") as f:
                    f.write(f"{class_name} {x_center} {y_center} {width} {height}\n")
            else:
                with open(os.path.join(dest_path, f"frame_{normalised_frame_number}.txt"), "a") as f:
                    f.write(f"{class_name} {x_center} {y_center} {width} {height}\n")


def main():
    print("Creating dataset for training and validation")

    # Create the datasets folders
    os.makedirs(path_to_data, exist_ok=True)
    os.makedirs(path_to_images, exist_ok=True)
    os.makedirs(path_to_labels, exist_ok=True)
    os.makedirs(path_to_images_train, exist_ok=True)
    os.makedirs(path_to_images_val, exist_ok=True)
    os.makedirs(path_to_labels_train, exist_ok=True)
    os.makedirs(path_to_labels_val, exist_ok=True)

    # Unzip the folders and move them to the train folders
    unzip_all_zips_from_source_to_target(path_to_annotation, path_to_images_train)

    # Create the labels for the training set
    for folder in os.listdir(path_to_images_train):
        folder_path = os.path.join(path_to_images_train, folder)
        for file in os.listdir(folder_path):
            if file.endswith(".xml"):
                create_labels_from_xml(os.path.join(folder_path, file), os.path.join(path_to_labels_train, folder))

    # TODO: Split the training set into training and validation set


if __name__ == "__main__":
    main()
