# youtube base url for video
yt_base_url = 'https://www.youtube.com/watch?v='

# user-agent
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}


def get_video_url(lst):
    """ Fetching videoId """
    vid_urls = []
    for vid in lst:
        link = yt_base_url + vid['videoId']
        vid_urls.append(link)
    
    return vid_urls

def get_video_thumbnail(lst):
    """ Fetching video thumbnail """
    vid_thumbs = []
    for vid in lst:
        thumb = vid['thumbnail']['thumbnails'][-1]['url'].split('?')[0]
        vid_thumbs.append(thumb)
    
    return vid_thumbs

def get_video_title(lst):
    """ Fetching video title """
    vid_titles = []
    for vid in lst:
        title = vid['title']['runs'][0]['text']
        vid_titles.append(title)
    
    return vid_titles

def get_video_views(lst):
    """ Fetching total number of views of video """
    vid_views = []
    for vid in lst:
        view = vid['viewCountText']['simpleText']
        vid_views.append(view)
    
    return vid_views

def get_video_post(lst):
    """ Fetching the time of video publish on channel """
    vid_post = []
    for vid in lst:
        post = vid['publishedTimeText']['simpleText']
        vid_post.append(post)
    
    return vid_post 

def get_video_publish_date(lst):
    """ 
    This function convert the absolute time into relative time.
    It will show the actual date of video uploaded.
    """
    from datetime import datetime as dt
    from datetime import timedelta as td

    today = dt.now()
    date_lst = []
    
    for p in lst:
        upload_dt = today
        num, val, _ = p.split()
        num = int(num)
        if val.startswith('hour'):
            upload_dt = today - td(hours=num)
        elif val.startswith('day'):
            upload_dt = today - td(days=num)
        elif val.startswith('week'):
            upload_dt = today - td(weeks=num) 
        elif val.startswith('month'):
            upload_dt = today - td(days=num*30) 
        elif val.startswith('year'):
            upload_dt = today - td(days=num*365) 

        date_lst.append(upload_dt.strftime("%d %b %Y"))
        
    return date_lst
