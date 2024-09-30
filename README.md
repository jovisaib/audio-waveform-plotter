# Waveform Video Generator

This Python script takes a `.wav` audio file and generates a waveform video with a green background, designed to fit perfectly over other videos. The video is produced in 1920x1080 resolution (YouTube format) and can be used in video editing software for easy chroma keying.

## Features
- Generates a smooth waveform video for any `.wav` file.
- Full 1920x1080 (YouTube) resolution.
- Green background for chroma keying.
- Efficient memory usage and optimized performance.
- Adjustable frames per second (default: 30 FPS).


## Requirements

Make sure you have Python 3.x installed along with the following dependencies:

You will also need ffmpeg installed on your system.


# tiktok
curl -X POST "http://localhost:8000/create_waveform_video/" \
     -H "accept: application/json" \
     -F "audio_file=@input.wav" \
     -F "width=1080" \
     -F "height=1920" \
     -F "fps=30"