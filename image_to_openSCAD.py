from openai import OpenAI
import base64
from PIL import Image
import io
import os

class ImageToOpenSCAD:
    def __init__(self, api_key):
        """Initialize with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)

    def process_image(self, image_path):
        """Process and convert image to base64."""
        try:
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if needed
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Convert to base64
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            raise Exception(f"Image processing error: {str(e)}")

    def generate_openscad_code(self, image_path):
        """Generate OpenSCAD code from image."""
        try:
            base64_image = self.process_image(image_path)

            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in converting isometric drawings to OpenSCAD code. Generate precise OpenSCAD code that accurately represents the 3D model shown in the image."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Generate OpenSCAD code for this isometric drawing. Include all necessary modules and ensure accurate dimensions and geometry."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000
            )
            
            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenSCAD code generation error: {str(e)}")

    def save_scad_code(self, code, output_path):
        """Save the generated OpenSCAD code to a file."""
        try:
            with open(output_path, 'w') as f:
                f.write(code)
            print(f"OpenSCAD code saved to: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving OpenSCAD code: {str(e)}")

def main():
    # Get API key from environment variable
    api_key = "gb8bqMD0wrPkM040h1dvOz6LTEIZCa5y"  # Replace with your actual OpenAI API key
    
    # Initialize converter
    converter = ImageToOpenSCAD(api_key)

    # Set paths
    input_image = "input/isometric_drawing.png"
    output_scad = "output/generated_model.scad"

    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_scad), exist_ok=True)

        # Generate OpenSCAD code
        print("Generating OpenSCAD code from image...")
        scad_code = converter.generate_openscad_code(input_image)
        
        # Save the code
        converter.save_scad_code(scad_code, output_scad)
        
        print("Process completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()