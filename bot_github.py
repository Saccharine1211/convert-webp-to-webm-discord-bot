import discord
import subprocess
from moviepy.editor import *
import imageio
import os
import numpy as np

def get_webp_info(file_path):
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the path to webpmux using a relative path
    webpmux_path = os.path.join(current_dir, 'your webpmux.exe path')
    # Run webpmux command to get file information
    result = subprocess.run([webpmux_path, '-info', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running webpmux: {result.stderr.decode('utf-8')}")
        return None
    return result.stdout.decode('utf-8')

def extract_durations(info):
    lines = info.split('\n')
    durations = []
    # Extract duration of each frame
    for line in lines[1:]:
        if 'no' in line:
            parts = line.split()
            duration = int(parts[6])
            durations.append(duration)
    return durations

def calculate_fps(durations):
    # Calculate total duration
    total_duration = sum(durations)
    # Calculate average duration
    average_duration = total_duration / len(durations) if durations else 0
    # Calculate frames per second (fps)
    fps = 1000 / average_duration if average_duration > 0 else 0
    return fps

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for attached .webp files in the message
    for attachment in message.attachments:
        if attachment.url.endswith('.webp'):
            # Save the webp file as a temporary file
            webp_file = 'temp.webp'
            await attachment.save(webp_file)

            # Extract webp file information
            info = get_webp_info(webp_file)
            if info:
                durations = extract_durations(info)
                fps = calculate_fps(durations)
                frame_count = len(durations)

                # Read images and create clips
                reader = imageio.get_reader(webp_file)
                frames = [np.array(frame) for frame in reader]
                clips = [ImageClip(frame, duration=1/fps) for frame in frames[:frame_count]]

                # Concatenate clips to create the final video file
                final_clip = concatenate_videoclips(clips, method="compose")
                webm_file = 'output.webm'
                final_clip.write_videofile(webm_file, codec="libvpx", fps=fps, bitrate="5000k")

                # Send the resulting file to the Discord channel
                await message.reply(file=discord.File(webm_file), mention_author=True)

# Run the bot (Replace 'TOKEN' with your actual bot token)
client.run('TOKEN')