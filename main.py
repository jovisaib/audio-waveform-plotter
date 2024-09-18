import numpy as np
from pydub import AudioSegment
from moviepy.editor import *

def create_waveform_image(audio_samples, duration, frame_idx, fps=30, height=1080, width=1920, color=(255, 255, 255), bg_color=(0, 255, 0)):
    total_frames = int(fps * duration)
    samples_per_frame = len(audio_samples) // total_frames

    start_idx = frame_idx * samples_per_frame
    end_idx = start_idx + samples_per_frame
    frame_samples = audio_samples[start_idx:end_idx]

    waveform = (frame_samples / np.max(np.abs(audio_samples)) * (height // 2)).astype(np.int32)

    image = np.full((height, width, 3), bg_color, dtype=np.uint8)

    x_coords = np.linspace(0, width - 1, num=len(waveform), dtype=np.int32)

    mid = height // 2
    for x, y in zip(x_coords, waveform):
        image[mid:mid+y, x] = color  # Draw the positive part of the waveform
        image[mid+y:mid, x] = color  # Draw the negative part of the waveform

    return image

# Creates the video
def create_waveform_video(audio_file, output_file, fps=30, resolution=(1920, 1080)):
    audio = AudioSegment.from_wav(audio_file)
    samples = np.array(audio.get_array_of_samples())
    duration = audio.duration_seconds

    def make_frame(t):
        frame_idx = int(t * fps)
        return create_waveform_image(samples, duration, frame_idx, fps=fps, height=resolution[1], width=resolution[0])

    video_clip = VideoClip(make_frame, duration=duration)
    
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)

    final_clip.write_videofile(output_file, fps=fps)

audio_file = "input.wav"
output_file = "waveform_video.mp4"

create_waveform_video(audio_file, output_file)
