# PixelSync

PixelSync is a Python FastAPI-based application designed for single-board computers like Raspberry Pi and Jetson Nano.
It enables users to access the camera feed of a single-board computer from other devices (laptops, computers, smartphones) connected to the same network.

## Features

- Real-time camera feed streaming.
- Easy setup for single-board computers.
- Compatible with a variety of devices on the same local network.

## Requirements

- Python 3.x
- FastAPI
- OpenCV


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nitin2606/PixelSync.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the PixelSync server on your single-board computer:

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

2. Open a web browser on any device connected to the same network.

3. Access the PixelSync interface:

    ```
    http://<single-board-computer-ip>:8000
    ```

4. Enjoy the real-time camera feed!


## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/nitin2606/PixelSync/issues).

Happy coding!
