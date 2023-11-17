import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64

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
        self.on_capture_callback = on_capture_callback

        self.window.after(10, self.update)
        self.window.mainloop()

    def capture_image(self):
        ret, frame = self.vid.read()

        if ret:
            # Save the captured frame to a file (you can customize the filename)
            image_path = "captured_image.png"
            cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Encode the image to base64
            base64_image = self.encode_image(image_path)

            # Call the callback function with the base64 image
            reply_content = self.on_capture_callback(base64_image)
            
            # Directly update the text on the screen
            self.set_text_on_screen(reply_content)

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
                cv2.putText(frame, self.text_on_screen, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                   
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def set_text_on_screen(self, text):
        self.text_on_screen = text

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Callback function to update the GUI with the received image
def on_capture_callback(base64_image):
    # reply = ModelManager(base64_image=base64_image)
    reply = "This is a long sentence that needs to be displayed on separate lines to ensure readability. It might contain multiple lines and can be quite lengthy."
    words = reply.split()
    word_lists = [words[i:i+10] for i in range(0, len(words), 10)]

    return word_lists


# Create a window and pass it to WebcamApp along with the callback function
root = tk.Tk()
app = WebcamApp(root, "Webcam App", on_capture_callback)
