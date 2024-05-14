import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def image_to_pixels(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize the image to a fixed size
    resized_img = cv2.resize(gray_img, (100, 100))  # Adjust as needed

    # Flatten the image to 1D array
    pixels = resized_img.flatten()
    print("Pixelating Input Image...\n\n")
    print(pixels)

    return pixels

def find_folder_by_image(input_image, dataset_dir):
    # Convert input image to pixels
    input_pixels = image_to_pixels(input_image)

    # Walk through the dataset directory recursively
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            # Check if the file is an image (assuming common image extensions)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp','.tif')):
                dataset_img_path = os.path.join(root, file)

                # Convert dataset image to pixels
                dataset_pixels = image_to_pixels(dataset_img_path)

                # Compare pixels (you may need more sophisticated methods for better accuracy)
                if np.array_equal(input_pixels, dataset_pixels):
                    return os.path.basename(os.path.dirname(dataset_img_path))

    # If no match is found, return None
    return None

def process_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary image
    _, binary_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)

    return gray_img, binary_img

def select_image(input_image_label, gray_image_label, binary_image_label, disease_label):
    # Open a file dialog for selecting an image file
    input_image = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg; *.jpeg; *.png; *.bmp; *.tif")])
    
    if input_image:
        # Load and display the selected input image
        img = Image.open(input_image)
        img = img.resize((200, 200))  # Resize image for display
        img = ImageTk.PhotoImage(img)
        input_image_label.config(image=img)
        input_image_label.image = img  # Keep a reference to prevent garbage collection

        # Process the input image to get grayscale and binary images
        gray_img, binary_img = process_image(input_image)

        # Display the grayscale image
        gray_img = Image.fromarray(gray_img)
        gray_img = ImageTk.PhotoImage(gray_img)
        gray_image_label.config(image=gray_img)
        gray_image_label.image = gray_img  # Keep a reference to prevent garbage collection

        # Display the binary image
        binary_img = Image.fromarray(binary_img)
        binary_img = ImageTk.PhotoImage(binary_img)
        binary_image_label.config(image=binary_img)
        binary_image_label.image = binary_img  # Keep a reference to prevent garbage collection

        # Find matching folder
        folder_name = find_folder_by_image(input_image, 'dataset')
        if folder_name:
            disease_label.config(text=f"Blood Group: {folder_name}")
            messagebox.showinfo("Match Found", f"Input image matches with {folder_name}")
            
            print("Category : ",folder_name)
        else:
            disease_label.config(text="Category: No match found")
            messagebox.showinfo("No Match", "No matching folder found for the input image.")

if __name__ == "__main__":
    # Create Tkinter window
    root = tk.Tk()
    root.title("Image Folder Matcher")
    root.configure(background="black")  # Set background color to black

    # Create labels for displaying images
    input_image_label = tk.Label(root, background="black")
    input_image_label.grid(row=0, column=0, padx=10, pady=10)

    gray_image_label = tk.Label(root, background="black")
    gray_image_label.grid(row=0, column=1, padx=10, pady=10)

    binary_image_label = tk.Label(root, background="black")
    binary_image_label.grid(row=0, column=2, padx=10, pady=10)

    # Create label for displaying disease name
    disease_label = tk.Label(root, text="Category:", font=("Helvetica", 12), background="black", foreground="white")
    disease_label.grid(row=1, column=0, columnspan=3, pady=10)

    # Create a button for selecting an image
    select_button = tk.Button(root, text="Select Image", command=lambda: select_image(input_image_label, gray_image_label, binary_image_label, disease_label), background="black", foreground="white")
    select_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Run the Tkinter event loop
    root.mainloop()
