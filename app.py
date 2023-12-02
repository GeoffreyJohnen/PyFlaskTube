from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import time
from pathlib import Path
app = Flask(__name__)

# Sample list of applications
applications = [
    {'name': 'YouTube Downloader', 'route': 'youtube_downloader'},
    # Add more applications as needed
]

def get_sorted_streams(youtube_url):
    try:
        video = YouTube(youtube_url)
        # Filter only video streams
        video_streams = video.streams.filter(only_video=True, file_extension='mp4')
        # Sort streams by quality (highest resolution first)
        sorted_streams = sorted(video_streams, key=lambda x: int(x.resolution.split('p')[0]), reverse=True)
        return sorted_streams, video  # Return both streams and video
    except Exception as e:
        return [], None

@app.route('/')
def index():
    return render_template('index.html', applications=applications)

@app.route('/youtube_downloader', methods=['GET', 'POST'])
def youtube_downloader():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')
        
        try:
            streams, video = get_sorted_streams(youtube_url)
            if not video or not streams:
                raise Exception("Could not retrieve video information or streams")



            if 'download' in request.form:
                selected_stream_index = int(request.form.get('selected_stream'))
                selected_stream = streams[selected_stream_index-1]
                # Set the download path (modify as needed)
                download_path = Path("downloads")
                download_path.mkdir(exist_ok=True)
                # Download the selected stream
                file_path = Path(f"{video.title}_{selected_stream.resolution}.mp4")
                selected_stream.download(output_path=download_path,filename=file_path)
                # Return the file for download
                return send_file(download_path.joinpath(file_path), as_attachment=True)
            return render_template('youtube_downloader.html', streams=streams, youtube_url=youtube_url)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            return render_template('youtube_downloader.html', error_message=error_message)

    return render_template('youtube_downloader.html', streams=None, youtube_url=None)

if __name__ == '__main__':
    app.run(debug=True)
