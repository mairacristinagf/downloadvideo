from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from pytube import YouTube
import youtube_dl
import requests
from bs4 import BeautifulSoup
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sim'

class UrlVideoForm(FlaskForm):
    url = StringField('URL do vídeo')
    submit = SubmitField('Baixar')

def baixar_video_ph(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_video_xh(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tags = soup.find_all('video')
        if video_tags:
            return video_tags[0]['src']
        else:
            return None
    else:
        return None

def baixar_video_erome(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tags = soup.find_all('source')
        if video_tags:
            return video_tags[0]['src']
        else:
            return None
    else:
        return None

def baixar_video_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    return stream.url

def baixar_video(url):
    if 'pornhub.com' in url:
        return baixar_video_ph(url)
    elif 'xhamster.com' in url:
        return baixar_video_xh(url)
    elif 'erome.com' in url:
        return baixar_video_erome(url)
    elif 'youtube.com' in url or 'youtu.be' in url:
        return baixar_video_youtube(url)
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlVideoForm()
    if form.validate_on_submit():
        url = form.url.data
        video_url = baixar_video(url)
        if video_url:
            return redirect(url_for('download_video', video_url=video_url))
        else:
            return render_template('error.html', message='URL inválida ou não suportada.')
    return render_template('index.html', form=form)

@app.route('/download', methods=['POST', 'GET'])
def download_video():
    form = UrlVideoForm()
    video_url = request.args.get('video_url')
    return render_template('download.html', video_url=video_url, form=form)

if __name__ == '__main__':
    app.run(debug=True)
