from image_processing import process_image
from huit_api_interpreter import interpret_drawing_with_huit
from rhino_model_creator import create_rhino_model_from_json

def main_pipeline(huit_api_key, input_image_path):
    """
    Complete pipeline to process an isometric drawing and create a Rhino model.
    """
    # Step 1: Process the image
    processed_image_path = process_image(input_image_path)

    # Step 2: Interpret drawing with HUIT API
    drawing_json = interpret_drawing_with_huit(huit_api_key, processed_image_path)

    # Step 3: Generate Rhino geometry from JSON
    if drawing_json:
        json_path = "output/drawing_output.json"
        create_rhino_model_from_json(json_path)

if __name__ == "__main__":
    huit_api_key = "gb8bqMD0wrPkM040h1dvOz6LTEIZCa5y"  # Replace with your HUIT API key
    input_image_path = "input/isometric_drawing.png"  # Replace with your input image path
    main_pipeline(huit_api_key, input_image_path)
