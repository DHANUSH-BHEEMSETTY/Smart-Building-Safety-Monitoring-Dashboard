import os
import shutil
import kagglehub
from ultralytics import YOLO

def download_and_train():
    print("Downloading weapon dataset from Kaggle...")
    path = kagglehub.dataset_download("raghavnanjappan/weapon-dataset-for-yolov5")
    print(f"Dataset downloaded to: {path}")
    
    # Usually datasets have a data.yaml in the root or a subdirectory
    # We will search for it
    import glob
    yaml_files = glob.glob(os.path.join(path, "**", "*.yaml"), recursive=True)
    if not yaml_files:
        print("Error: Could not find data.yaml in the downloaded dataset.")
        return
        
    data_yaml = yaml_files[0]
    print(f"Found data configuration at: {data_yaml}")
    
    # Initialize YOLOv11n — best performing model from comparison
    print("Initializing YOLOv11n for fine-tuning...")
    model = YOLO("yolo11n.pt")
    
    # Train the model — 30 epochs to match the Kaggle training configuration
    print("Starting training...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    model.train(
        data=data_yaml,
        epochs=30, 
        imgsz=640,
        batch=16,
        project=os.path.join(base_dir, "runs"),
        name="weapon_det_v11"
    )
    print("Training completed!")
    print(f"Best weights saved to: runs/weapon_det_v11/weights/best.pt")
    print(f"Copy the best.pt to models/yolo11n_weapon_best.pt to use in the dashboard.")

if __name__ == "__main__":
    download_and_train()
