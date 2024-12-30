# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:31:05 2024

@author: User
"""



import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load Metadata
metadata_path = 'updated_metadata.csv'  # Path to the metadata file
dataset_folder = 'dataset/'  # Folder containing .pck files
metadata = pd.read_csv(metadata_path)

# Map class labels to names
class_names = {0: "Healthy", 1: "Partially Injured", 2: "Completely Ruptured"}

# Function to visualize slices with ROI in a table format
def visualize_sample_with_roi_table(sample_file, metadata_row, frame, zoom_factor):
    try:
        # Load the sample volume
        with open(sample_file, 'rb') as f:
            volume = pickle.load(f)

        # Extract ROI details
        roi_x, roi_y, roi_z = metadata_row['roiX'], metadata_row['roiY'], metadata_row['roiZ']
        roi_width, roi_height, roi_depth = metadata_row['roiWidth'], metadata_row['roiHeight'], metadata_row['roiDepth']
        class_label = metadata_row['aclDiagnosis']

        # Plot all slices in the volume, arranged in rows and columns
        num_slices = volume.shape[0]
        cols = 5  # Number of slices per row
        rows = -(-num_slices // cols)  # Calculate the number of rows (ceiling division)

        # Create the figure with dynamically adjusted size based on zoom_factor
        fig, axs = plt.subplots(rows, cols, figsize=(15 * zoom_factor, rows * 3 * zoom_factor))
        axs = axs.flatten()

        for i in range(len(axs)):
            if i < num_slices:
                slice_data = volume[i]
                axs[i].imshow(slice_data, cmap='gray')

                # Add bounding box if the slice is within ROI depth
                if roi_z <= i < roi_z + roi_depth:
                    rect = patches.Rectangle(
                        (roi_x, roi_y), roi_width, roi_height, linewidth=2, edgecolor='r', facecolor='none'
                    )
                    axs[i].add_patch(rect)

                axs[i].set_title(f"Slice {i}")
            else:
                axs[i].axis('off')  # Turn off unused subplots

            axs[i].axis('off')

        # Add the class label as the overall figure title
        fig.suptitle(f"Class: {class_names[class_label]} (Label {class_label})", fontsize=16, y=1.02)
        plt.tight_layout()

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=frame)  # Create canvas
        canvas.draw()  # Render the plot
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack the widget into the frame

    except Exception as e:
        print(f"Error visualizing sample: {e}")

# Function to run the program based on the user's input
def run_program():
    try:
        # Get the inputs from the user
        class_name_input = class_name_combobox.get()
        exam_id_input = exam_id_combobox.get()

        # Validate inputs
        if not class_name_input or not exam_id_input:
            messagebox.showerror("Input Error", "Please enter both class name and exam ID.")
            return

        # Convert class_name_input to class index
        if class_name_input.lower() == "healthy":
            class_label = 0
        elif class_name_input.lower() == "partially injured":
            class_label = 1
        elif class_name_input.lower() == "completely ruptured":
            class_label = 2
        else:
            messagebox.showerror("Input Error", "Invalid class name.")
            return

        # Find the row in the metadata with the given exam ID
        sample_row = metadata[metadata['examId'] == int(exam_id_input)]
        if sample_row.empty:
            messagebox.showerror("Input Error", "Invalid exam ID.")
            return
        
        # Get the sample file path
        sample_file = os.path.join(dataset_folder, sample_row.iloc[0]['volumeFilename'])

        # Visualize the sample with ROI in a table format
        visualize_sample_with_roi_table(sample_file, sample_row.iloc[0], plot_frame, zoom_factor)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to clear the current search
def clear_inputs():
    class_name_combobox.set('')
    exam_id_combobox.set('')
    for widget in plot_frame.winfo_children():
        widget.destroy()

# Update Exam IDs based on Class Selection
def update_exam_ids(event):
    class_name_input = class_name_combobox.get().lower()
    if class_name_input:
        filtered_metadata = metadata[metadata['aclDiagnosis'] == class_names_rev[class_name_input]]
        exam_ids = filtered_metadata['examId'].unique().tolist()
        exam_id_combobox['values'] = exam_ids
        if len(exam_ids) > 0:
            exam_id_combobox.current(0)  # Set the first exam ID as default

# Reverse the class_names dictionary for easy lookup
class_names_rev = {v.lower(): k for k, v in class_names.items()}

# Zoom functionality using mouse scroll
def on_mouse_wheel(event):
    global zoom_factor
    if event.delta > 0:  # Scroll up (zoom in)
        zoom_factor += 0.1
    else:  # Scroll down (zoom out)
        zoom_factor -= 0.1
    run_program()

# Zoom In function
def zoom_in():
    global zoom_factor
    zoom_factor += 0.1
    run_program()

# Zoom Out function
def zoom_out():
    global zoom_factor
    zoom_factor -= 0.1
    run_program()

# Save Plot to Downloads
def save_plot():
    try:
        # Get the file path for the Downloads folder
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path = os.path.join(download_folder, "medical_image_plot.png")
        
        # Save the current plot to the Downloads folder
        plt.savefig(save_path)
        messagebox.showinfo("Success", f"Plot saved successfully to: {save_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the plot: {e}")

# Create the Tkinter window
window = tk.Tk()
window.title("Medical Image Viewer")

# Create and place labels, entry fields, and button in one row
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Class Name:").grid(row=0, column=0, padx=5)
class_name_combobox = ttk.Combobox(input_frame, values=["Healthy", "Partially Injured", "Completely Ruptured"])
class_name_combobox.grid(row=0, column=1, padx=5)

# Bind class dropdown to update Exam IDs
class_name_combobox.bind("<<ComboboxSelected>>", update_exam_ids)

# Dropdown for Exam ID
exam_ids = metadata['examId'].unique().tolist()  # Get all unique exam IDs
tk.Label(input_frame, text="Select Exam ID:").grid(row=0, column=2, padx=5)
exam_id_combobox = ttk.Combobox(input_frame, values=exam_ids)
exam_id_combobox.grid(row=0, column=3, padx=5)

run_button = tk.Button(input_frame, text="Show Image", command=run_program)
run_button.grid(row=0, column=4, padx=10)

# Clear button
clear_button = tk.Button(input_frame, text="Clear", command=clear_inputs)
clear_button.grid(row=0, column=5, padx=10)

# Zoom controls - in the same row as clear button
zoom_in_button = tk.Button(input_frame, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=0, column=6, padx=10)

zoom_out_button = tk.Button(input_frame, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=0, column=7, padx=10)

# Download button to save the plot
download_button = tk.Button(input_frame, text="Download Plot", command=save_plot)
download_button.grid(row=0, column=8, padx=10)

# Frame to display the plot with a scrollbar
plot_frame = tk.Frame(window)
plot_frame.pack(pady=10)

# Add a canvas with scrollbar to handle large images
canvas_frame = tk.Canvas(plot_frame)
scrollbar = tk.Scrollbar(plot_frame, orient="vertical", command=canvas_frame.yview)
canvas_frame.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas_frame.pack(side="left", fill="both", expand=True)

# Initialize zoom factor
zoom_factor = 1

# Bind mouse scroll event to zoom in and out
canvas_frame.bind_all("<MouseWheel>", on_mouse_wheel)

# Run the Tkinter main loop
window.mainloop()

