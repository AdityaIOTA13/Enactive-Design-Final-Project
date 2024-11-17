import requests
import json

def interpret_drawing_with_huit(huit_api_key, processed_image_path):
    """
    Send processed image data to HUIT proxy to get JSON interpretation.
    """
    # Define the HUIT proxy endpoint
    url = "https://go.apis.huit.harvard.edu/ais-openai-direct/v1/chat/completions"

    # The prompt for interpreting the drawing
    prompt = """
    I have a simple isometric line drawing represented as detected edges.
    Please provide a JSON structure with the following:
    - Nodes (key points of the drawing)
    - Edges (connections between nodes)
    - Circles or arcs (if applicable)

    The goal is to recreate this in Rhino.
    """

    # Prepare the headers
    headers = {
        "api-key": huit_api_key,
        "Content-Type": "application/json"
    }

    # Prepare the data payload
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    # Make the POST request to the HUIT proxy
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        output_json = response.json()
        output_path = "output/drawing_output.json"
        with open(output_path, "w") as file:
            json.dump(output_json, file, indent=4)
        print(f"JSON output saved at: {output_path}")
        return output_json
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    huit_api_key = "gb8bqMD0wrPkM040h1dvOz6LTEIZCa5y"  # Replace with your HUIT API key
    processed_image_path = "input/isometric_drawing.png"
    interpret_drawing_with_huit(huit_api_key, processed_image_path)
