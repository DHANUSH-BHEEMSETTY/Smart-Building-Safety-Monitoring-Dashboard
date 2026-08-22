import os
import shutil
import kagglehub

# Set Kaggle API token
os.environ["KAGGLE_API_TOKEN"] = "KGAT_854d026187cb953766344c440d38b5fb"

def download_and_setup_dataset():
    print("Downloading dataset from Kaggle...")
    # Download dataset
    path = kagglehub.dataset_download("azimjaan21/fire-and-smoke-dataset-object-detection-yolo")
    print("Dataset downloaded to:", path)
    
    # Target directory in the project data folder
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "fire_dataset"))
    
    # If target already exists, remove it or skip
    if os.path.exists(target_dir):
        print(f"Target directory {target_dir} already exists. Overwriting...")
        shutil.rmtree(target_dir)
        
    print(f"Moving dataset to {target_dir}...")
    shutil.copytree(path, target_dir)
    print("Dataset setup complete!")

if __name__ == "__main__":
    download_and_setup_dataset()
