#!/usr/bin/env python3

'''
Program: codex.py
Author: Jacob Hammond
Date: 12/10/2023

Description: 

        This program is the main executable for CODEX - Color-Object Detection and EXtraction.
        It is a tool for interior designers or hobbyists to input an image of an interior space
        and an object of interest, and the program will craft a curated color palette based on
        the interior image and then compare the object of interest to the palette to determine
        if it is a good fit for the interior space.

        The program uses a custom trained YOLO (You Only Look Once) segmentation model to 
        attempt to match the object of interest to a common object category. If the object
        has a high enough confidence score, the model will apply isolating segmentation to 
        the object of interest and use a finer-scale color matching scheme focused solely
        on the object of interest. 

        The intent behind this approach is to stretch the capabilities of this program so that
        input images require little to no preprocessing. A user should be able to snap a picture
        of an object of interest without worrying about separating it from other potential 
        objects nearby, or about the consistency of the background.
            
        Additionally, by matching the object of interest to a common object category, the segmentation 
        and labeling can be used to extract multiple objects of interest from the same image, and 
        compare all potential common objects to the interior color palette. An example of this use 
        case might be the user snapping a photo of a catalog page, or taking a photo in a show room 
        with multiple objects, and then be able to decide which object(s) would be the best fit for 
        their interior space.

            
Notes on the CODEX segmentation model:

        The model was developed using a custom dataset that I created using Roboflow.
        This allowed me to select a large amount of data from images that are FOSS around 
        the web and on RoboFlow, and add hand-drawn segmentations to the dataset. Then, using
        the Ultralytics YOLOv8 model, I was able to train the model extensively on the dataset
        to acheive a high level of accuracy. 

        The YOLOv8 model was chosen because it is a fast, lightweight model, that is trained on 
        the MS COCO (Common Objects in Context) dataset, which contains 80 common object 
        categories and over 300,000 images. Since many items in an interior space are a 
        part of the COCO dataset, it was a good starting point for the CODEX model. Additional
        categories not in the MS COCO dataset were added the CODEX model and trained. 

        The source code for the model generation can be found in codex_model.py. Since model 
        training is a time-intensive, and resource-intensive process, I have included the 
        pre-trained model in the project files for runtime use and it is not required for 
        the user to train the model themselves. 

        There are 16 supported object categories in the CODEX model:

        'bed', 'chair', 'clock', 'couch', 'curtain', 'dresser', 'lamp', 'light', 
        'pillow', 'plant', 'rug', 'shelf', 'stool', 'table', 'vase', 'wall-art'

Dependencies: 

        This project was developed on Python 3.11.5. Additional packages are listed in 
        requirements.txt and automatically installed via pip in a virtual environment.

Addditional Documentation, source code, and dataset:

        https://github.com/jhammo32/codex
        https://universe.roboflow.com/codex-oqz5i/codex_segmentation_v5

Project Files: 

- codex.py - main executable
- codex_common.py - common functions used by codex.py
- codex_model.py - model training and testing functions
- dataset/object-training - dataset used for training the model
- datasets/examples - example images used for testing and demonstration
- datasets/object-training/codex.pt - CODEX segmentation model 
- requirements.txt - list of dependencies

Usage:

   > python codex.py <interior_image_file> <object_of_interest_image_file>

  to use included sample images:

   > python codex.py

Usage Example:

    python codex.py interior.jpg  couch.jpg

  '''

# setup virtual environment, dependencies, and imports
import codex_common as codex
codex.setup()

# MAIN PROGRAM
if __name__ == '__main__':

    # check sys args for interior image file, and object of interest
    if len(sys.argv) == 3:
        image_file = sys.argv[1]
        object_of_interest = sys.argv[2]
    # otherwise if not provided, use a sample included in the project
    else:
        print("No input args with image files provided, using sample image set")
        image_file = "datasets/examples/interior3.jpg"
        object_of_interest = "datasets/examples/sofa.jpg"


    # load the interior image 
    image = cv2.imread(image_file)

    # call the extract_color_palette function
    palette, hsv_colors = codex.extract_color_palette(image)

    # Initialize an instance of the InteriorPalette class
    codex.InteriorPalette(image_file, image, hsv_colors, palette)

    # load the object of interest image
    object_of_interest = cv2.imread(object_of_interest)

    # Extract objects
    objects = codex.get_obj_mask(image)



    # Deactivate virtual environment
    os.system("deactivate")