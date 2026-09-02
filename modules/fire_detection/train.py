import os
import yaml
from ultralytics import YOLO

def setup_data_yaml(dataset_dir):
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"data.yaml not found at {yaml_path}")
        
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Update paths to be absolute
    data['path'] = dataset_dir
    data['train'] = "train/images"
    data['val'] = "valid/images"
    if 'test' in data:
        data['test'] = "test/images"
        
    # Write back
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f)
        
    return yaml_path

def train_model():
    # The images are actually inside data/fire_dataset/fire_smoke
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "fire_dataset"))
    
    print("Setting up data.yaml...")
    # Skip rewriting data.yaml because we already manually created a correct one
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    
    print("Initializing YOLOv11 model...")
    model = YOLO("yolo11n.pt")  # YOLOv11 nano — best performing model from comparison
    
    print("Starting training...")
    # Train the model — 30 epochs to match the Kaggle training configuration
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    results = model.train(
        data=yaml_path,
        epochs=30,
        imgsz=640,
        batch=16,
        project=os.path.join(base_dir, "runs"),
        name="fire_smoke_det_v11"
    )
    print("Training completed!")
    print(f"Best weights saved to: runs/fire_smoke_det_v11/weights/best.pt")
    print(f"Copy the best.pt to models/yolo11n_fire_smoke_best.pt to use in the dashboard.")

if __name__ == "__main__":
    train_model()
