import imageio
import numpy as np
import gradio as gr
import os

class VideoCache:
    def __init__(self, video_path):
        self.reader = imageio.get_reader(video_path)
        self.total_frames = self.reader.count_frames()
        self.frames = self.load_frames()
        self.video_path = video_path

    def load_frames(self):
        return [frame for frame in self.reader]

    def get_frame(self, frame_number):
        if 0 <= frame_number < self.total_frames:
            return self.frames[frame_number]
        else:
            return np.zeros((480, 640, 3), dtype=np.uint8)

# Global variable to store the video cache
video_cache = None

def save_video(image):
    if image is None:
        return "No image uploaded", None, gr.Slider(minimum=0, maximum=0, step=1, label="Frame", interactive=False)
    
    output_path = "testvideo.mp4"
    # Here you would implement the logic to create a video from the image
    # For this example, we'll just save the image as a single-frame video
    # imageio.mimsave(output_path, [image], fps=1)
    
    global video_cache
    video_cache = VideoCache(output_path)
    
    new_slider = gr.Slider(minimum=0, maximum=video_cache.total_frames-1, step=1, label="Frame", interactive=True)
    
    return f"Video saved as {output_path}", output_path, new_slider

def show_frame(frame_number):
    global video_cache
    if video_cache is None:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    return video_cache.get_frame(frame_number)

def save_frame(frame):
    if frame is None:
        return "No frame to save"
    
    output_path = "saved_frame.png"
    imageio.imwrite(output_path, frame)
    return f"Frame saved as {output_path}"

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Image to Video Converter and Frame Viewer")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(label="Upload Image")
            run_button = gr.Button("Run")
        
        with gr.Column(scale=2):
            video_component = gr.Video(label="Video Player")
            frame_image = gr.Image(label="Current Frame")
            frame_slider = gr.Slider(minimum=0, maximum=0, step=1, label="Frame", interactive=False)
            save_button = gr.Button("Save Frame")
    
    output_text = gr.Textbox(label="Output")
    
    run_button.click(
        save_video, 
        inputs=[input_image], 
        outputs=[output_text, video_component, frame_slider]
    )
    
    frame_slider.change(
        show_frame, 
        inputs=[frame_slider], 
        outputs=[frame_image]
    )
    
    save_button.click(
        save_frame, 
        inputs=[frame_image], 
        outputs=[output_text]
    )

# Launch the interface
iface.launch()