# Knee MRI Viewer and ROI Visualizer
![Sample MRI Slices](https://github.com/user-attachments/assets/6575e0aa-a2f5-4198-b6f2-a8d1a53566e4)

This project provides a Tkinter-based graphical user interface (GUI) for visualizing 3D knee MRI volumes. The application enables users to view individual slices, identify regions of interest (ROIs) based on metadata, and interactively analyze medical images. It also supports zooming, downloading visualizations, and exploring localized slices for diagnostic purposes.

This tool is designed to assist radiologists and researchers in studying knee conditions, including ACL injuries.

- View MRI volumes with slice-by-slice visualization.
- Highlight and localize regions of interest (ROIs) using metadata.
- Interactive zooming and downloading of visualizations.
- Supports three classes:
  - Healthy
  - Partially Injured
  - Completely Ruptured
 
# Dataset
The dataset used in this project is publicly available on Kaggle:

[Knee MRI Dataset](https://www.kaggle.com/datasets/sohaibanwaar1203/kneemridataset)

To use this tool, download the dataset from the above link and place the `.pck` and metadata file.

# Installation

1. Clone the repository:
   git clone https://github.com/yourusername/knee-mri-viewer.git
   cd knee-mri-viewer

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
   pip install -r requirements.txt

 
# Usage
Run the Tkinter application:
   python src/app.py

1. Select the class of interest (Healthy, Partially Injured, Completely Ruptured).
2. Choose the corresponding Exam ID from the dropdown.
3. Visualize the selected volume with highlighted ROIs.
4. Use the "Zoom In" and "Zoom Out" buttons for detailed analysis.
5. Save the visualized plot by clicking "Download Plot."

# Dependencies
- Python 3.8+
- pandas
- numpy
- matplotlib
- tkinter
# Screenshots
![snapshot 1](https://github.com/user-attachments/assets/d26cb49a-cf1e-4722-84cf-1be6dcf5893d)
![Screenshot 2](https://github.com/user-attachments/assets/7f01473c-25a5-4dc1-ae20-204c2e0d6124)

