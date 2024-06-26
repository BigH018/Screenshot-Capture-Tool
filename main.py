import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from datetime import datetime, timedelta
import traceback

# Define global variables
videos_processed = 0
total_videos = 0

# Define screenshot interval options with corresponding frame rates
screenshot_intervals = {
    "Every Frame": 1,
    "Every 2 Frames": 2,
    "Every 30 Frames": 30,
    "Every 60 Frames": 60
}

def capture_screenshots(video_path, output_folder, crop_size, screenshot_interval, progress_bar, remaining_time_label, callback):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the video file
        video = cv2.VideoCapture(video_path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Capture screenshots
        current_frame = 0
        screenshot_count = 0
        start_time = datetime.now()
        while True:
            success, frame = video.read()
            if not success:
                break

            # Crop the frame based on user selected size
            center_x = frame.shape[1] // 2
            center_y = frame.shape[0] // 2

            crop_half_size = crop_size // 2
            cropped_frame = frame[center_y - crop_half_size:center_y + crop_half_size, center_x - crop_half_size:center_x + crop_half_size]

            # Check if it's time to capture a screenshot based on the selected interval
            if current_frame % screenshot_interval == 0:
                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                screenshot_path = os.path.join(output_folder, f"frame_{timestamp}.jpg")

                # Save the cropped frame as an image
                cv2.imwrite(screenshot_path, cropped_frame)
                screenshot_count += 1

                # Update progress bar
                progress = (current_frame / frame_count) * 100
                progress_bar['value'] = progress

                # Estimate remaining time
                current_time = datetime.now()
                elapsed_time = current_time - start_time
                if screenshot_count > 0:
                    average_time_per_screenshot = elapsed_time / screenshot_count
                    remaining_time = average_time_per_screenshot * (frame_count - current_frame)
                    remaining_time_label.config(text=f"Estimated Time Remaining: {str(remaining_time).split('.')[0]}")

                root.update_idletasks()

            current_frame += 1

        # Release the video object
        video.release()

        # Call the callback function to prompt for another video
        callback()
    except Exception as e:
        traceback.print_exc()  # Print traceback for debugging
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        callback()  # Call the callback function to prompt for another video


def select_file():
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)
    except Exception as e:
        traceback.print_exc()  # Print traceback for debugging
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def select_output_folder():
    try:
        output_folder_path = filedialog.askdirectory()
        if output_folder_path:
            output_folder_entry.delete(0, tk.END)
            output_folder_entry.insert(0, output_folder_path)
    except Exception as e:
        traceback.print_exc()  # Print traceback for debugging
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def prompt_for_another_video():
    global videos_processed
    
    # Increment the count of processed videos
    videos_processed += 1
    
    # Check if all videos have been processed
    if videos_processed == total_videos:
        # Prompt user to select another video file
        messagebox.showinfo("Capture Complete", "Screenshot capture process completed.")
        videos_processed = 0  # Reset the count of processed videos for future captures
        select_file()


def start_capture():
    global total_videos
    
    # Check if video file, output folder, and crop size are selected
    video_file = file_entry.get()
    output_folder = output_folder_entry.get()
    crop_size = int(crop_size_var.get())  # Get the selected crop size
    screenshot_interval = screenshot_intervals[screenshot_interval_var.get()]  # Get the selected screenshot interval
    if not video_file or not output_folder or crop_size <= 0:
        messagebox.showwarning("Warning", "Please select a video file, an output folder, and a valid crop size.")
        return
    
    # Set the total number of videos
    total_videos = 1
    
    # Create progress bar
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress_bar.grid(row=6, columnspan=4, padx=3, pady=5)

    # Create estimated remaining time label
    remaining_time_label = tk.Label(root, text="Estimated Time Remaining: --:--:--")
    remaining_time_label.grid(row=7, columnspan=4, padx=5, pady=5)

    try:
        # Start screenshot capture process for the selected video file
        screenshot_thread = threading.Thread(target=capture_screenshots, args=(video_file, output_folder, crop_size, screenshot_interval, progress_bar, remaining_time_label, prompt_for_another_video))
        screenshot_thread.start()
    except Exception as e:
        traceback.print_exc()  # Print traceback for debugging
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def display_explanation():
    explanation_pages = [
        """
        Page 1: Introduction
        
        Welcome to the Video Screenshot Capture Tool!

        This tool allows you to capture screenshots from video files with ease. 
        Below, you'll find a brief overview of how to use this tool:

        Click the 'Next' button to continue.
        """,
        """
        Page 2: Select Video File

        To get started, select a video file from your computer. 
        Click the 'Browse' button next to the 'Video File' field to open a file dialog. 
        Once you've selected the desired video file, its path will be displayed in the input field.

        Click the 'Next' button to continue.
        """,
        """
        Page 3: Choose Output Folder

        Next, choose the folder where the captured screenshots will be saved. 
        Click the 'Browse' button next to the 'Output Folder' field to select the output directory.

        Click the 'Next' button to continue.
        """,
        """
        Page 4: Specify Crop Size

        In this step, specify the size of the area to be cropped from each frame of the video, in pixels. 
        Enter a positive integer value in the 'Crop Size' field. 
        This determines the size of the square area to be captured from the center of each frame.

        For example, if you enter '100' as the crop size, the tool will capture a square area of 100x100 pixels 
        from the center of each frame. This means the resulting screenshots will be 100x100 pixels in size.

        Choose a crop size that suits your needs and provides sufficient detail for your screenshots.

        Click the 'Next' button to continue.
        """,
        """
        Page 5: Select Screenshot Interval

        Choose the interval at which screenshots will be captured from the video using the dropdown menu.
        Options include capturing a screenshot every frame, every 2 frames, every 30 frames, or every 60 frames.

        Click the 'Next' button to continue.
        """,
        """
        Page 6: Start Capture

        Once you've selected a video file, an output folder, specified the crop size, and chosen the screenshot interval, 
        you're ready to start capturing screenshots. Click the 'Start Capture' button to 
        initiate the screenshot capture process. The tool will process the selected video file, 
        extracting screenshots based on the specified parameters.

        That's it! Click the 'Next' button to close the explanation.
        """

    ]
    
    def next_page():
        nonlocal page_number
        page_number += 1
        if page_number < len(explanation_pages):
            explanation_label.config(text=explanation_pages[page_number])
        else:
            root.destroy()

    page_number = 0

    root = tk.Toplevel()
    root.title("Explanation")
    
    explanation_label = tk.Label(root, text=explanation_pages[page_number], wraplength=600, justify="left")
    explanation_label.pack(padx=20, pady=20)

    next_button = tk.Button(root, text="Next", command=next_page)
    next_button.pack(pady=10)

    root.mainloop()


# Create GUI
root = tk.Tk()
root.title("ScreenShot Capture Tool - By BigH")

# Add explanation button
explanation_button = tk.Button(root, text="Explanation", command=display_explanation)
explanation_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")

# Video File section
file_label = tk.Label(root, text="Video File:")
file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=1, column=1, padx=5, pady=5)
file_button = tk.Button(root, text="Browse", command=select_file)
file_button.grid(row=1, column=2, padx=5, pady=5)

# Output Folder section
output_folder_label = tk.Label(root, text="Save Folder:")
output_folder_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=2, column=1, padx=5, pady=5)
output_folder_button = tk.Button(root, text="Browse", command=select_output_folder)
output_folder_button.grid(row=2, column=2, padx=5, pady=5)

# Crop Size section
crop_size_label = tk.Label(root, text="Crop Size (pixels):")
crop_size_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
crop_size_var = tk.StringVar(root)
crop_size_entry = tk.Entry(root, textvariable=crop_size_var, width=10)
crop_size_entry.grid(row=3, column=1, padx=5, pady=5)

# Screenshot Interval section
screenshot_interval_label = tk.Label(root, text="Screenshot Interval:")
screenshot_interval_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
screenshot_interval_var = tk.StringVar(root)
screenshot_interval_dropdown = ttk.Combobox(root, textvariable=screenshot_interval_var, values=list(screenshot_intervals.keys()))
screenshot_interval_dropdown.grid(row=4, column=1, padx=5, pady=5)
screenshot_interval_dropdown.current(0)  # Set default option

# Start Capture button
start_button = tk.Button(root, text="Start Capture", command=start_capture)
start_button.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()