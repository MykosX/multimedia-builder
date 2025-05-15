@echo off
REM Set environment variables for FFmpeg

REM Define the path to FFmpeg
SET FFMPEG_PATH=d:\tools\installed\2_dev\ffmpeg

REM Add FFmpeg to the system PATH for this session
SET PATH=%FFMPEG_PATH%;%PATH%

REM Optionally, print the FFmpeg version to confirm it's working
ffmpeg -version

REM You can add more environment variables below if needed

REM End of script
