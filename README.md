### Description
A full-stack web app that transcribes videos into .srt subtitle files, with a Python Flask backend utilising OpenAI Whisper.

### Demo
Free trial on [Google Cloud](https://transcriber-810769139906.europe-west2.run.app). <br>
Please note that the platform has a cold start delay, which may take a moment when you first access it, and currently only supports file uploads up to 32MB in size. 


### Deployment
Pull the Python image python:3.8-slim before building: `docker pull python:3.8-slim` <br> 

To build this Docker container: `docker build . -t transcriber` <br>

To run the container: `docker run transcriber`

A "Temporary failure in name resolution" error may occur caused by PIP failing to resolve DNS name when a VPN is connected, trying disconnecting the VPN to fix this issue.
