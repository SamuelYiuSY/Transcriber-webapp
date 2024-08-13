from flask import Flask, request, send_file, render_template
import whisper
from datetime import timedelta
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

model = whisper.load_model("base")
print("Whisper model loaded.")

def convert_to_mp3(input_file):

    input_path = os.path.join("tempConvertedAudioDir", input_file.filename)
    print(f"temp_dir: {input_path}")


    input_file.save(input_path)
    print(input_file.filename)

    # Determine if the file is MP3 or MP4
    if input_file.filename.lower().endswith('.mp4'):
        print("received a mp4 file")

        # Extract audio from MP4 and convert to MP3
        print(f"converting {input_file.filename} into a mp3 file")
        video = VideoFileClip(input_path)
        outputFilename = str(input_file.filename[:-4])+".mp3"
        video.audio.write_audiofile(outputFilename)
        return outputFilename
    elif input_file.filename.lower().endswith('.mp3'):
        print("received a mp3 file")
        return input_file.filename
    else:
        # Unsupported file format
        print("received an unsupported file")
        raise ValueError("Unsupported file format")

def convertMp3ToTranscript(input_file_path):
    print("transcribing using Whisper")
    result = model.transcribe(input_file_path)
    return result

def convertTranscriptToSrt(result, originalFilename):
    print("converting transcript to srt")
    # separate each segments and write to a .srt file
    srtSegment = []
    for eachSegment in result["segments"]:
        startTime = f"{str(timedelta(seconds=int(eachSegment['start'])))}"
        endTime = f"{str(timedelta(seconds=int(eachSegment['end'])))}"
        text = eachSegment["text"]
        srtSegment.append(f"{startTime}->{endTime} {text[1:] if text[0] == ' ' else text}\n")
    
    srtFileName = os.path.join("tempMedia", f"{originalFilename}_transcript.srt")
    # with open(srtFileName, "a") as srtFile:
    srtFile = open(srtFileName, "a")
    for eachSrtSegment in srtSegment:
        srtFile.write(eachSrtSegment)
        print(eachSrtSegment)

    srtFile.close()

    srtFile = open(srtFileName, "rb")   # open the file in binary mode
    return srtFile


# @app.route('/upload', methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        originalFilename = file.filename
        print(f"received {originalFilename}")

        if file:
            # save the uploaded file temporarily
            tempFilePath = os.path.join("tempMedia", originalFilename)
            file.save(tempFilePath)

            # process the file using testFunction()
            srtFilePath = convertMp3ToTranscript(tempFilePath)

            srtFile = convertTranscriptToSrt(srtFilePath, originalFilename)

            # return the .srt file to the front end 
            return send_file(srtFile, as_attachment=True, download_name=f"{originalFilename}_transcript.srt")


        # output_audio_path = convert_to_mp3(file)
        # # return output_audio_path
        # result = convertMp3ToTranscript(output_audio_path)
        # transcriptFile = convertTranscriptToSrt(result)
        # return send_file(transcriptFile, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)