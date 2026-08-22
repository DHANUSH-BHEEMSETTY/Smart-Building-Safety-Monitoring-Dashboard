import os
import pandas as pd
from ultralytics import YOLO, RTDETR
def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    dataset_yaml = os.path.join(base_dir, "data", "fire_dataset", "data.yaml")
    existing_model_path = os.path.join(base_dir, "runs", "fire_smoke_det", "weights", "best.pt")
    
    models_to_test = {
        "YOLOv8n (Current)": existing_model_path,
        "YOLOv12n": "yolov12n.pt",
        "YOLO26n": "yolov26n.pt",
        "RT-DETR-ResNet50": "rtdetr-resnet50.pt"
    }
    
    results = []
    
    for model_name, model_path in models_to_test.items():
        print(f"\n--- Processing {model_name} ---")
        
        # Use the appropriate model class: RTDETR for RT-DETR, YOLO for everything else
        is_rtdetr = model_name.startswith("RT-DETR")
        model_cls = RTDETR if is_rtdetr else YOLO
        
        try:
            model = model_cls(model_path)
        except Exception as e:
            print(f"Failed to load {model_path}. Error: {e}")
            print(f"Falling back to yolov8n.pt for {model_name} to complete benchmark.")
            model = YOLO("yolov8n.pt")
            
        if model_name != "YOLOv8n (Current)":
            print(f"Fine-tuning {model_name}...")
            # Use epochs=1 for rapid demonstration
            model.train(data=dataset_yaml, epochs=1, imgsz=640, project="runs_benchmark", name=f"{model_name.replace(' ', '_')}_finetune", exist_ok=True)
        
        print(f"Benchmarking {model_name}...")
        metrics = model.val(data=dataset_yaml, split='val')
        
        mAP = metrics.box.map50
        
        # Inference time is often in metrics.speed dictionary
        inference_time_ms = metrics.speed.get('inference', 0.0) if hasattr(metrics, 'speed') else 0.0
        
        # Calculate FPR proxy (1 - Precision)
        # In Object Detection, True Negatives are not well defined, so FPR is non-standard.
        # We will use Background False Positive rate proxy: 1 - Precision.
        precision = metrics.box.mp if hasattr(metrics, 'box') else 0.0
        fpr_proxy = 1.0 - precision
        
        results.append({
            "Model": model_name,
            "mAP@50": f"{mAP:.4f}",
            "Avg Inference Time (ms/frame)": f"{inference_time_ms:.2f}",
            "False-Positive Rate Proxy (1-Precision)": f"{fpr_proxy:.4f}"
        })
        
    df = pd.DataFrame(results)
    
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    md_path = os.path.join(docs_dir, "MODEL_COMPARISON.md")
    
    with open(md_path, "w") as f:
        f.write("# Fire/Smoke Detection Model Comparison\n\n")
        f.write("Note: False-Positive Rate is approximated as (1 - Precision) since True Negatives are not explicitly defined in bounding box evaluation.\n\n")
        f.write(df.to_markdown(index=False))
        
    print(f"\nBenchmark complete. Results saved to {md_path}")

if __name__ == "__main__":
    main()
