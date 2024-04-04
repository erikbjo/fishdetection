from ultralytics import YOLO

if __name__ == "__main__":
    # Create the YOLO model
    # https://docs.ultralytics.com/tasks/detect/
    model = YOLO('YOLOv8n.pt')  # Can use many other models check link above

    # Train the model
    model.train(data='../nemoV1.yaml', epochs=2)

    # Save the model
    # model.save('../model.pt')
    # --- Model is saved to runs/detect/train{number}/weights/best.pt
