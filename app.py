#import tkinter as tk
#from tkinter import filedialog, messagebox, Toplevel
#from PIL import Image, ImageTk
import os
import sys, subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinterdnd2'])
from tkinterdnd2 import TkinterDnD, DND_FILES
import streamlit as st
from PIL import Image
import io

def pixelate_image(img, pixel_size):
    """
    Pixelates the given image based on the specified pixel size.

    Args:
        img (PIL.Image.Image): The original image.
        pixel_size (int): The size of each pixel block.

    Returns:
        PIL.Image.Image: The pixelated image.
    """
    # Calculate the new size of the image
    new_width = max(1, img.width // pixel_size)
    new_height = max(1, img.height // pixel_size)

    # Resize down and then back up to achieve pixelation
    small_img = img.resize((new_width, new_height), Image.NEAREST)
    pixelated_img = small_img.resize(img.size, Image.NEAREST)
    return pixelated_img

def main():
    st.set_page_config(page_title="Image Pixelator", layout="centered")
    st.title("📸 Image Pixelator")
    st.write("Upload an image, adjust the pixel size, and download your pixelated image.")

    # File uploader accepts various image formats
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "bmp", "gif", "tiff"])

    if uploaded_file is not None:
        try:
            # Open the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Original Image', use_column_width=True)

            # Slider for pixel size
            pixel_size = st.slider("Select Pixel Size", min_value=1, max_value=100, value=10, step=1)

            # Pixelate button
            if st.button("Pixelate"):
                with st.spinner("Pixelating..."):
                    pixelated_image = pixelate_image(image, pixel_size)
                st.success("Pixelation Complete!")

                # Display the pixelated image
                st.image(pixelated_image, caption='Pixelated Image', use_column_width=True)

                # Prepare image for download
                buffered = io.BytesIO()
                # Save as PNG to preserve quality; adjust format if needed
                pixelated_image.save(buffered, format="PNG")
                byte_im = buffered.getvalue()

                st.download_button(
                    label="Download Pixelated Image",
                    data=byte_im,
                    file_name="pixelated_image.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")

if __name__ == "__main__":
    main()

