from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import numpy as np
from pydub import AudioSegment
from moviepy.editor import *
import tempfile
import os

app = FastAPI()

def create_waveform_image(audio_samples, duration, frame_idx, fps=30, height=1080, width=1920, color=(255, 165, 0), bg_color=(0, 255, 0)):
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


@app.post("/create_waveform_video/")
async def create_waveform_video_api(
    audio_file: UploadFile = File(...),
    fps: int = 30,
    width: int = 1920,
    height: int = 1080
):
    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input:
        temp_input.write(await audio_file.read())
        temp_input_path = temp_input.name

    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_output_path = temp_output.name
    temp_output.close()

    try:
        # Create the waveform video
        create_waveform_video(temp_input_path, temp_output_path, fps=fps, resolution=(width, height))

        # Return the video file
        return FileResponse(temp_output_path, media_type="video/mp4", filename="waveform_video.mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary files
        os.unlink(temp_input_path)
        os.unlink(temp_output_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)