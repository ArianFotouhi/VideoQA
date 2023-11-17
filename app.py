import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
import threading
from model import ModelManager

# from model import ModelManager

class WebcamApp:
    def __init__(self, window, window_title, on_capture_callback):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Use default camera (change if you have multiple cameras)

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_capture = ttk.Button(window, text="Capture Image", command=self.capture_image)
        self.btn_capture.pack(pady=10)

        self.photo = None
        self.text_on_screen = ""
        self.text_y_position = 50  # Default y-position
        self.on_capture_callback = on_capture_callback

        self.window.after(10, self.update)
        self.window.mainloop()

    def capture_image(self):
        # Display "Just a sec..." message
        self.set_text_on_screen("Just a sec...", self.text_y_position)

        # Start a new thread for capturing the image
        capture_thread = threading.Thread(target=self.capture_image_thread)
        capture_thread.start()

    def capture_image_thread(self):
        ret, frame = self.vid.read()

        if ret:
            # Save the captured frame to a file (you can customize the filename)
            image_path = "captured_image.png"
            cv2.imwrite(image_path, frame)

            # Encode the image to base64
            base64_image = self.encode_image(image_path)

            # Call the callback function with the base64 image
            reply_content = self.on_capture_callback(base64_image)

            # Directly update the text on the screen
            self.set_text_on_screen(reply_content, self.text_y_position)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_image

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            # Check if there's a photo to display
            if self.photo:
                self.canvas.delete(self.photo)

            # Display the received text on the video frame
            if self.text_on_screen:
                lines = self.text_on_screen.split('\n')
                y = self.text_y_position
                for line in lines:
                    cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y += 20  # Adjust the vertical spacing as needed

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def set_text_on_screen(self, text, y):
        self.text_on_screen = text
        self.text_y_position = y

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Callback function to update the GUI with the received image
def on_capture_callback(base64_image):


    reply = ModelManager(base64_image)
    words = reply.split()
    string_lists = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]

    return "\n".join(string_lists)

# Create a window and pass it to WebcamApp along with the callback function
root = tk.Tk()
app = WebcamApp(root, "Webcam App", on_capture_callback)
