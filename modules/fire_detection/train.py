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
    
    print("Initializing YOLO model...")
    model = YOLO("yolov8n.pt")  # load a pretrained model
    
    print("Starting training...")
    # Train the model
    # Keep epochs low for the first pass as requested
    results = model.train(
        data=yaml_path,
        epochs=3,
        imgsz=640,
        project="runs",
        name="fire_smoke_det"
    )
    print("Training completed!")

if __name__ == "__main__":
    train_model()
