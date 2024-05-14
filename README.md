# Video Screenshot Capture Tool

This tool is designed to capture screenshots from video files using OpenCV and Tkinter GUI in Python.

## Features

- **Multi-Video Support:** Capture screenshots from one or more video files simultaneously, saving time and effort.
- **Customizable Crop Size:** Specify the size of the area to be cropped from each frame of the video, providing flexibility in screenshot composition.
- **Efficient Processing:** Utilizes threading to process multiple videos concurrently, maximizing performance.
- **Visual Progress Tracking:** Monitor the progress of screenshot capture with a visual progress bar and estimated remaining time.
- **Error Handling:** Gracefully handle errors and exceptions to ensure a smooth user experience.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.x:** The programming language used to run the tool.
- **OpenCV (`opencv-python`):** OpenCV library for image and video processing.
- **Tkinter:** GUI toolkit for Python (usually included in standard Python installations).

### Installation

Clone the repository:

git clone https://github.com/yourusername/video-screenshot-capture-tool.git


### Usage

1. Run the script `main.py`.
2. **Select Video Files (MAX 5):** Click the "Browse" button next to "Video Files" to select one or more video files for screenshot capture. Please note that due to threading limitations, the tool supports capturing screenshots from a maximum of 5 videos at a time.
3. **Choose Output Folder:** Select the output folder where captured screenshots will be saved by clicking the "Browse" button next to "Output Folder."
4. **Specify Crop Size:** Enter the desired crop size in pixels in the "Crop Size" field, determining the area to be captured from each frame.
5. **Start Capture:** Click the "Start Capture" button to initiate the screenshot capture process.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/yourfeature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/yourfeature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
