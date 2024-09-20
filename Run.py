import os
from IPython import display
import ultralytics
import torch
from ultralytics import YOLO
from IPython.display import display, Image

# Ensure this code is inside the main block
if __name__ == "__main__":
    # Get the current working directory
    HOME = os.getcwd()
    print(HOME)

    # Check system environment
    ultralytics.checks()  

    # Check if GPU is available
    device = 'cuda' 
    print(f"Using device: {device}")

    # Load the pre-trained YOLOv8 model
    model = YOLO("yolov8s.pt")

    # Train the model with output folder specified
    model.train(
        data="M:\\Uni_Siegen\\Sem-5\\SA\\Studienarbeit\\Work\\Training_Offline\\Training_Colored_Images\\data.yaml",  # Path to your data.yaml file
        epochs=50,         # Number of training epochs
        batch=16,          # Batch size
        imgsz=640,         # Image size
        plots=True,        # Enable plot generation during training
        project="M:\\Uni_Siegen\\Sem-5\\SA\\Studienarbeit\\Work\\Training_Offline\\Training_Colored_Images\\runs",  # Output folder for training results
        name="exp_colored"  # Name of the specific training experiment (e.g., 'exp_custom')
    )

    # Validate the trained model
    model = YOLO('M:\\Uni_Siegen\\Sem-5\\SA\\Studienarbeit\\Work\\Training_Offline\\Training_Colored_Images\\runs\\exp_custom\\weights\\best.pt')  # Load the best weights after training

    metrics = model.val(
        data="M:\\Uni_Siegen\\Sem-5\\SA\\Studienarbeit\\Work\\Training_Offline\\Training_Colored_Images\\data.yaml",  # Path to your data.yaml file
        imgsz=640,         # Image size
        plots=True         # Enable plot generation during validation
    )

    # Print the validation metrics
    print(metrics)
