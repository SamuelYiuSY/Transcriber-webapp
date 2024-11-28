Pull the Python image python:3.8-slim before building: `docker pull python:3.8-slim` <br> 

To build this Docker container: `docker build . -t transcriber` <br>

To run the container: `docker run transcriber`

A "Temporary failure in name resolution" error may occur caused by PIP failing to resolve DNS name when a VPN is connected, trying disconnecting the VPN to fix this issue.