from flask import Flask, render_template, request 
from flask_cors import CORS, cross_origin
import requests as req
import re, json
from bs4 import BeautifulSoup as bs
import youtube_extract as yt

app  = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/ytVids',methods=['POST','GET']) # route to show the youtube videos in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:            
            channel_url = request.form['content'].replace(" ","")
            res = req.get(channel_url, headers = yt.header, cookies={'CONSENT':'YES+1'})
            
            if res.ok:
                soup = bs(res.text, "html.parser")                
                G = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

                json_data = json.loads(G)
                 
                tabs = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]
                tabs = tabs['tabRenderer']['content']['richGridRenderer']['contents']

                videos_list = []
                for tab in tabs[:5]:
                    vid = tab['richItemRenderer']['content']['videoRenderer']
                    videos_list.append(vid)   

                top5urls = yt.get_video_url(videos_list)
                top5thumbnails = yt.get_video_thumbnail(videos_list)
                top5titles = yt.get_video_title(videos_list)
                top5views = yt.get_video_views(videos_list)
                top5post= yt.get_video_post(videos_list)
                top5publish_dates = yt.get_video_publish_date(top5post)

                videos = []
                for i in range(len(top5urls)):
                    vid_detail = {
                            'Title': top5titles[i], 
                            'Publish_Date': top5publish_dates[i], 
                            'Total_Views': top5views[i],
                            'Video_URL': top5urls[i],
                            'Thumbnail_URL': top5thumbnails[i]
                            }
                    
                    videos.append(vid_detail)

                return render_template('results.html', videos=videos)
            else:
                print("Plesae check the URL")
                return "Please check the URL"
        except Exception as e:
            print(f'The Exception message is: {e}')
            return f'Exception: {e}'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
