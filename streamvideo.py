import streamlit as st
from PIL import Image, ImageEnhance
from moviepy.editor import VideoFileClip
import numpy as np
from io import BytesIO

def enhance_frame(frame, enhancement_factor):
    image = Image.fromarray(frame)  # Convert frame to PIL Image
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(enhancement_factor)
    return np.array(enhanced_image)  # Convert back to NumPy array

def enhance_video(input_path, output_path, enhancement_factor):
    clip = VideoFileClip(input_path)
    enhanced_clip = clip.fl_image(lambda frame: enhance_frame(frame, enhancement_factor))
    enhanced_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main():
    st.title("Enhance Your Videos")

    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)

        enhancement_factor = st.slider("Enhancement Factor", min_value=0.0, max_value=2.0, value=1.0, step=0.01)

        if st.button("Enhance"):
            # Save the uploaded video to a temporary file
            temp_video_path = "temp_video.mp4"
            with open(temp_video_path, "wb") as temp_video:
                temp_video.write(uploaded_file.read())

            # Enhance the video and get the enhanced video path
            enhanced_video_path = "enhanced_video.mp4"
            enhance_video(temp_video_path, enhanced_video_path, enhancement_factor)

            # Display the enhanced video
            st.video(enhanced_video_path)

if __name__ == "__main__":
    main()
