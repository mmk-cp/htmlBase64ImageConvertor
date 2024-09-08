import base64
from PIL import Image
from io import BytesIO
import re


def clean_base64_string(base64_string):
    """Removes newlines and trailing backslashes added by IDE."""
    return base64_string.replace('\\', '').replace('\n', '')


def convert_base64_to_image(base64_string, output_file):
    # Clean up the Base64 string
    clean_base64 = clean_base64_string(base64_string)

    # Remove the data:image part and keep the base64 string
    image_data = re.sub(r'^data:image/.+;base64,', '', clean_base64)

    # Decode the base64 string
    image_bytes = base64.b64decode(image_data)

    # Convert bytes to an image
    image = Image.open(BytesIO(image_bytes))

    # Save the image in the desired format (e.g., PNG)
    image.save(output_file, 'PNG')
    print(f"Image saved as {output_file}")


def read_svg_from_file(file_path):
    """Reads SVG content from a given file."""
    with open(file_path, 'r') as file:
        return file.read()


# Example usage
svg_file_path = 'input_svg.txt'  # Replace with your SVG file path
svg_content = read_svg_from_file(svg_file_path)

# Extract the base64 image from the svg_content
base64_image = re.search(r'href="([^"]+)"', svg_content).group(1)

# Convert and save the image
convert_base64_to_image(base64_image, 'output_image.png')
