import openai
from gtts import gTTS
import os
from PIL import Image
import io
import requests
import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import imageio_ffmpeg

# Set the path to ffmpeg
ffmpeg_path = "/usr/local/bin/ffmpeg"  # Update with your ffmpeg path if installed manually
if not os.path.exists(ffmpeg_path):
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()  # Use imageio's ffmpeg if manual path is invalid
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

# Create necessary directories if they don't exist
os.makedirs("audio", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)

def generate_script(genre, length, intensity):
    """
    Generates a script based on genre, length, and intensity.
    """
    openai.api_key = "YOUR_OPENAI_API_KEY"
    prompt = f"Write a {length} script in the {genre} genre with {intensity} intensity."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=length
    )
    script = response['choices'][0]['message']['content'].strip()
    return script

def generate_story(genre, length):
    """
    Generates a story based on genre and length.
    """
    openai.api_key = "YOUR_OPENAI_API_KEY"
    prompt = f"Write a {length} word story in the {genre} genre."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=length
    )
    story = response['choices'][0]['message']['content'].strip()
    return story

def script_to_audio(script, filename="audio/output.mp3"):
    """
    Converts script text into an audio file.
    """
    tts = gTTS(text=script, lang='en')
    tts.save(filename)
    return filename

def generate_image_from_scene(scene_description, filename):
    """
    Generates an image from a scene description using DALL-E and saves it.
    """
    openai.api_key = "YOUR_OPENAI_API_KEY"
    response = openai.Image.create(
        prompt=scene_description,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))
    image.save(filename)
    return filename

def create_movie_with_audio(images, audio_file, genre, output_filename="videos/output_movie.mp4"):
    """
    Combines images and audio to create a movie with background music.
    """
    # Create video clips from images
    image_clips = [ImageClip(img).set_duration(3) for img in images]
    video = concatenate_videoclips(image_clips, method="compose")

    # Load the audio file
    narration = AudioFileClip(audio_file)

    # Add narration to the video
    video = video.set_audio(narration)

    # Add background music based on genre
    background_music_file = f"audio/background_{genre.lower()}.mp3"
    if os.path.exists(background_music_file):
        background_music = AudioFileClip(background_music_file).volumex(0.2)
        combined_audio = CompositeAudioClip([narration, background_music])
        video = video.set_audio(combined_audio)

    # Write the final video to a file
    video.write_videofile(output_filename, fps=24)
    return output_filename

def main():
    st.title("Script and Story Generator")

    # Step 1: Script Generation
    st.header("Generate a Script")
    genre = st.text_input("Enter the genre of the script:")
    length = st.number_input("Enter the length of the script (in number of tokens):", min_value=10, max_value=1000, value=100)
    intensity = st.selectbox("Enter the intensity of the script:", ["high", "medium", "low"])

    if st.button("Generate Script"):
        if genre and length and intensity:
            script = generate_script(genre, length, intensity)
            st.subheader("Generated Script:")
            st.text(script)
            st.session_state['script'] = script  # Store script in session state
        else:
            st.warning("Please fill in all fields to generate the script.")

    # Step 2: Text to Audio Generation
    if 'script' in st.session_state:
        if st.button("Convert Script to Audio"):
            audio_file = script_to_audio(st.session_state['script'])
            st.audio(audio_file, format="audio/mp3")
            st.session_state['audio_file'] = audio_file

    # Step 3: Text to Image Generation for Each Scene
    if 'script' in st.session_state:
        if st.button("Generate Images for Scenes"):
            images = []
            scenes = st.session_state['script'].split("\n")
            for i, scene in enumerate(scenes):
                if scene.strip():  # Only process non-empty scenes
                    st.write(f"Generating image for scene {i+1}: {scene}")
                    image_filename = f"images/scene_{i+1}.png"
                    generate_image_from_scene(scene, image_filename)
                    images.append(image_filename)
                    st.image(image_filename, caption=f"Scene {i+1}")
            st.session_state['images'] = images

    # Step 4: Create Movie with Audio and Images
    if 'images' in st.session_state and 'audio_file' in st.session_state:
        if st.button("Create Movie from Script"):
            movie_file = create_movie_with_audio(st.session_state['images'], st.session_state['audio_file'], genre)
            st.video(movie_file)

    # Step 5: Story Generation
    st.header("Generate a Story")
    if st.checkbox("Generate a Story"):
        story_genre = st.text_input("Enter the genre of the story:")
        story_length = st.number_input("Enter the length of the story (in words):", min_value=50, max_value=1000, value=200)
        if st.button("Generate Story"):
            if story_genre and story_length:
                story = generate_story(story_genre, story_length)
                st.subheader("Generated Story:")
                st.text(story)
            else:
                st.warning("Please fill in all fields to generate the story.")

if __name__ == "__main__":
    main()
