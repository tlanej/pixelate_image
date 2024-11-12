import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os
import sys, subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinterdnd2'])

def pixelate_image(input_image_path, pixel_size):
    """Pixelates the image based on the input path and pixel size."""
    try:
        img = Image.open(input_image_path)
        small_img = img.resize((img.width // pixel_size, img.height // pixel_size), Image.NEAREST)
        pixelated_img = small_img.resize((img.width, img.height), Image.NEAREST)
        return pixelated_img
    except Exception as e:
        messagebox.showerror("Error", f"Error in pixelating the image: {e}")
        return None

def load_image(file_path=None):
    """Loads the image and displays it in the GUI."""
    global loaded_image_path

    # Strip curly braces or quotes that can appear around paths during drag-and-drop
    if file_path:
        file_path = file_path.strip('{}').replace('"', '')

    # Ensure that the file exists
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Error", "File does not exist. Please select a valid file.")
        return

    try:
        # Load and display the original image
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize to fit the window
        img_tk = ImageTk.PhotoImage(img)

        label_original.config(image=img_tk)
        label_original.image = img_tk
        label_original_text.config(text="Original Image")

        # Set the file path for pixelation when the slider is adjusted
        loaded_image_path = file_path

        # Apply pixelation with the current slider value
        apply_pixelation()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the image: {e}")

def apply_pixelation():
    """Applies pixelation to the loaded image and displays the result."""
    if loaded_image_path:
        try:
            pixel_size = pixelation_slider.get()
            pixelated_img = pixelate_image(loaded_image_path, pixel_size)
            if pixelated_img is None:
                return
            pixelated_img.thumbnail((300, 300))  # Resize for display
            pixelated_img_tk = ImageTk.PhotoImage(pixelated_img)

            label_pixelated.config(image=pixelated_img_tk)
            label_pixelated.image = pixelated_img_tk
            label_pixelated_text.config(text=f"Pixelated Image (Pixel Size: {pixel_size})")

            # Save pixelated image in-memory for saving later
            global pixelated_image_to_save
            pixelated_image_to_save = pixelated_img

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply pixelation: {e}")
    else:
        messagebox.showinfo("No Image Loaded", "Please load an image first.")

def save_image():
    """Saves the pixelated image to a user-specified file."""
    if pixelated_image_to_save:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if save_path:
            try:
                pixelated_image_to_save.save(save_path)
                messagebox.showinfo("Success", f"Image saved successfully as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the image: {e}")
        else:
            messagebox.showinfo("Cancelled", "Save operation was cancelled.")
    else:
        messagebox.showinfo("No Image", "There is no pixelated image to save. Please load and pixelate an image first.")

def on_drop(event, drop_window):
    """Handles drag-and-drop event and closes the pop-up."""
    file_path = event.data
    load_image(file_path)
    drop_window.destroy()

def open_drop_popup():
    """Opens a pop-up window that says 'Drop Image Here'."""
    drop_window = Toplevel(root)
    drop_window.geometry("300x200")
    drop_window.title("Drop Image Here")
    drop_window.config(bg="lightgray")

    # Instructions label
    label = tk.Label(drop_window, text="Drop Image Here", bg="lightgray", font=("Arial", 16))
    label.pack(expand=True, pady=50)

    # Bind drag-and-drop functionality to the pop-up window
    drop_window.drop_target_register(DND_FILES)
    drop_window.dnd_bind('<<Drop>>', lambda event: on_drop(event, drop_window))

# Create the tkinter window
root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
root.title("Image Pixelator")

# Create and place GUI components
frame = tk.Frame(root)
frame.pack(pady=20)

# Load Button (opens drop popup)
btn_load = tk.Button(frame, text="Load Image", command=open_drop_popup)
btn_load.grid(row=0, column=0, padx=10)

# Pixelation intensity slider
label_slider = tk.Label(frame, text="Pixel Size:")
label_slider.grid(row=0, column=1, padx=10)

pixelation_slider = tk.Scale(frame, from_=1, to_=50, orient=tk.HORIZONTAL, length=200)
pixelation_slider.set(10)  # Default pixel size
pixelation_slider.grid(row=0, column=2, padx=10)

# Slider event to automatically apply pixelation on change
pixelation_slider.bind("<Motion>", lambda event: apply_pixelation())

# Save Button
btn_save = tk.Button(frame, text="Save As", command=save_image)
btn_save.grid(row=0, column=3, padx=10)

# Original Image Label
label_original_text = tk.Label(root, text="No Image Loaded")
label_original_text.pack(pady=10)
label_original = tk.Label(root)
label_original.pack()

# Pixelated Image Label
label_pixelated_text = tk.Label(root, text="")
label_pixelated_text.pack(pady=10)
label_pixelated = tk.Label(root)
label_pixelated.pack()

# Track the loaded image and pixelated image
loaded_image_path = None
pixelated_image_to_save = None

# Start the tkinter main loop
root.mainloop()
