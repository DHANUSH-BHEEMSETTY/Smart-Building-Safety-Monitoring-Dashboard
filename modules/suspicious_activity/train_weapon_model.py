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
    
    # Initialize YOLOv8n
    print("Initializing YOLOv8n for fine-tuning...")
    model = YOLO("yolov8n.pt")
    
    # Train the model (Set epochs=1 for a quick test, or 50+ for actual accuracy)
    print("Starting training...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    model.train(
        data=data_yaml,
        epochs=10, 
        imgsz=640,
        project=os.path.join(base_dir, "runs"),
        name="weapon_det"
    )
    print("Training completed! The weapon model is now available in runs/weapon_det/weights/best.pt")

if __name__ == "__main__":
    download_and_train()
