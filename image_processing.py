import cv2
import os

def process_image(image_path):
    """
    Process an image to detect edges for vectorization.
    """
    # Log the full path and check if the file exists
    full_path = os.path.abspath(image_path)
    print(f"Full path to input file: {full_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input file not found: {image_path}")
    
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Unable to read the image file: {image_path}")
    
    # Apply edge detection using the Canny algorithm
    edges = cv2.Canny(img, 100, 200)

    # Create the output folder if it doesn't exist
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Save the processed edges to the output folder
    processed_path = os.path.join(output_folder, "processed_image.png")
    cv2.imwrite(processed_path, edges)
    print(f"Processed image saved at: {processed_path}")
    return processed_path

if __name__ == "__main__":
    # Path to the input image
    input_image = "input/isometric_drawing.png"  # Replace with the correct path if needed

    # Debugging: Print working directory and check file existence
    print(f"Current working directory: {os.getcwd()}")
    print(f"Input file exists: {os.path.exists(input_image)}")

    try:
        process_image(input_image)
    except Exception as e:
        print(f"Error: {e}")
