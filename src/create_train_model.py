from ultralytics import YOLO

if __name__ == "__main__":
    # Create the YOLO model
    # https://docs.ultraxlytics.com/tasks/detect/
    model = YOLO('YOLOv8m.pt')  # Can use many other models check link above

    # Train the model
    model.train(data='../nemoV1.yaml', epochs=200, name='nemo_v2')

    model.export()
