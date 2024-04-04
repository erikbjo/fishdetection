from ultralytics import YOLO

if __name__ == "__main__":
    # Create the YOLO model
    model = YOLO()

    # Train the model
    model.train(data="../nemoV1.yaml", epochs=1)

    # Save the model
    model.save("../model.pt")
