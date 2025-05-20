from gradio_client import Client
import requests
import os
import shutil
# Initialize the client with the Hugging Face Space URL
client = Client("stabilityai/stable-diffusion-3.5-large-turbo")
def gen_image(prompt,path):
    # Define the text prompt

    new_path = os.path.join(os.getcwd(), f"comics_generated/{path}.png")
    # Generate the image
    result = client.predict(prompt,prompt, api_name="/infer")

    image_data = result[0]  

    # Define a new location to move the image
    new_path = os.path.join(os.getcwd(), "generated_image.png")

    # Move the image to the current working directory
    shutil.move(image_data, new_path)
