import base64
from PIL import Image
from io import BytesIO
import re


def read_svg_content_from_file(file_path):
    """Reads the entire content of the SVG file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def clean_base64_string(base64_string):
    """Cleans up the Base64 string by removing unwanted patterns."""
    # Remove patterns like "\n' +", newlines, and backslashes
    base64_string = base64_string.replace("\\n' +", '')
    base64_string = base64_string.replace('\n', '')
    base64_string = base64_string.replace('\\', '')
    return base64_string


def convert_base64_to_image(base64_string, output_file):
    # Clean up the Base64 string
    clean_base64 = clean_base64_string(base64_string)

    try:
        # Remove the data:image part and keep the base64 string
        image_data = re.sub(r'^data:image/.+;base64,', '', clean_base64)

        # Decode the base64 string
        image_bytes = base64.b64decode(image_data)

        # Debug: Print length of image bytes to check if it's valid
        print(f"Image data length: {len(image_bytes)} bytes")

        # Convert bytes to an image
        image = Image.open(BytesIO(image_bytes))

        # Save the image in the desired format (e.g., PNG)
        image.save(output_file, 'PNG')
        print(f"Image saved as {output_file}")
    except Exception as e:
        print(f"Error: {e}")


def extract_base64_from_svg(svg_content):
    """Extract the base64-encoded image data from the SVG content."""
    match = re.search(r'href="data:image/.+;base64,([^"]+)"', svg_content)
    if match:
        return match.group(1)
    else:
        raise ValueError("No Base64 image data found in the SVG content.")


# Example usage
svg_file_path = 'input_svg.txt'  # Path to your SVG text file

# Read SVG content from the file
svg_content = read_svg_content_from_file(svg_file_path)

# Extract the base64 image from the svg_content
base64_image = extract_base64_from_svg(svg_content)

# Convert and save the image
convert_base64_to_image(base64_image, 'output_image.png')
