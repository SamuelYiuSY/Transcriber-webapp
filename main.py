from flask import Flask, request, send_file, render_template
import whisper
from datetime import timedelta
from moviepy.editor import VideoFileClip
import os

PORT = 5100

app = Flask(__name__)

model = whisper.load_model("base", download_root="whisperModel")
print("Whisper model loaded.")


def convertToTranscript(inputFilePath):
    print("transcribing using Whisper")
    result = model.transcribe(inputFilePath)
    return result

def convertTranscriptToSrt(result, originalFilename):
    print("converting transcript to srt")
    # separate each segments and write to a .srt file
    srtSegment = []
    for eachSegment in result["segments"]:
        startTime = f"{str(timedelta(seconds=int(eachSegment['start'])))}"
        endTime = f"{str(timedelta(seconds=int(eachSegment['end'])))}"
        text = eachSegment["text"]
        id = eachSegment["id"] + 1
        # srtSegment.append(f"{startTime}->{endTime} {text[1:] if text[0] == ' ' else text}\n")
        srtSegment.append(f"{id}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n")

    srtFileName = os.path.join("tempMedia", f"{originalFilename}_transcript.srt")
    srtFile = open(srtFileName, "a")
    for eachSrtSegment in srtSegment:
        srtFile.write(eachSrtSegment)
        print(eachSrtSegment)

    srtFile.close()

    srtFile = open(srtFileName, "rb")   # open the file in binary mode
    return srtFile


# @app.route('/upload', methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        originalFilename = file.filename
        print(f"received {originalFilename}")

        if file:
            # save the uploaded file temporarily
            srtFilePath = os.path.join("tempMedia", originalFilename)
            file.save(srtFilePath)

            transcript = convertToTranscript(srtFilePath)
            srtFile = convertTranscriptToSrt(transcript, originalFilename)

            # return the .srt file to the front end 
            try: 
                return send_file(srtFile, as_attachment=True, download_name=f"{originalFilename}_transcript.srt")
            finally:
                print(f"srtFilePath: {srtFilePath}")

                # remove files from server
                os.remove(srtFilePath)
                srtFileName = os.path.join("tempMedia", f"{originalFilename}_transcript.srt")
                os.remove(srtFileName)


    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=PORT)