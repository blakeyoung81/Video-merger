import glob
import os
from moviepy.editor import *
from PyQt5.QtWidgets import *

# Create the GUI
app = QApplication([])
list_widget = QListWidget()
list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Allow multiple selection
button_up = QPushButton("Move Up")
button_down = QPushButton("Move Down")
button_combine = QPushButton("Combine")
button_choose_dir = QPushButton("Choose Directory")
layout = QVBoxLayout()
layout.addWidget(list_widget)
layout.addWidget(button_up)
layout.addWidget(button_down)
layout.addWidget(button_combine)
layout.addWidget(button_choose_dir)
window = QWidget()
window.setLayout(layout)
window.show()

# Choose a directory and search for MP4 files
def choose_dir():
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    if directory:  # If a directory was selected
        # Clear the list widget
        list_widget.clear()

        # Search for MP4 files in the selected directory
        mp4_files = glob.glob(os.path.join(directory, "*.mp4"))

        # Populate the list widget with the MP4 files
        for file in mp4_files:
            #file_name = os.path.basename(file)  # Extract just the file name
            list_item = QListWidgetItem(file)
            list_widget.addItem(list_item)
button_choose_dir.clicked.connect(choose_dir)

# Move the selected items up or down in the list
def move_up():
    selected_items = list_widget.selectedItems()
    for item in selected_items:
        current_row = list_widget.row(item)
        if current_row > 0:
            list_widget.takeItem(current_row)
            list_widget.insertItem(current_row - 1, item)
            list_widget.setCurrentItem(item)
def move_down():
    selected_items = list_widget.selectedItems()
    for item in reversed(selected_items):  # Reverse the order to avoid index errors
        current_row = list_widget.row(item)
        if current_row < list_widget.count() - 1:
            list_widget.takeItem(current_row)
            list_widget.insertItem(current_row + 1, item)
            list_widget.setCurrentItem(item)
button_up.clicked.connect(move_up)
button_down.clicked.connect(move_down)

# Combine the selected clips when the button is clicked
def combine_clips():
    selected_clips = []
    for index in range(list_widget.count()):
        item = list_widget.item(index)
        if item.isSelected():
            selected_clips.append(VideoFileClip(item.text()))
    final_clip = concatenate_videoclips(selected_clips)
    final_clip.write_videofile("Output/final_clip.mp4")
button_combine.clicked.connect(combine_clips)

# Run the GUI
app.exec_()