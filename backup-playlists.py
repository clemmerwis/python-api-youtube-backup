
#! python3
import time, os, sys, openpyxl, re, json, re 
import urllib.request
from pathlib import Path
from pytube import YouTube 
 
class Playlist:  
  # attribute
  num_of_playlists = 0 

  # init method or constructor   
  def __init__(self, title, pl_id, api_url):  
    self.title = title
    self.api_url = api_url 
    self.pl_id = pl_id 
    Playlist.num_of_playlists += 1

  # Method   
  def print_title(self):  
    print(self.title)
  
  def get_api_url(self):
    return self.api_url

  def get_title(self):
    return self.title  
  
  def get_id(self):
    return self.pl_id
  
  def create_data_dict(self, url=None):
    if url is None:
      url = self.api_url
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    return data

  def regex_description(self, video_description):
    reg_up_to_newline = re.compile( '.+?((?=\\n)|\n)$' )
    description_mo = reg_up_to_newline.search(video_description)
    if description_mo != None:
      video_description = str(description_mo.group())
    return video_description

  def create_playlist_items_dict(self, looper, data_dict, videos_dict=None):
    if videos_dict == None:
      videos_dict = {}  
    i = 0
    while i < len(data_dict['items']):
      video_id = data_dict['items'][i]['snippet']['resourceId']['videoId']
      video_title = data_dict['items'][i]['snippet']['title']
      video_description = data_dict['items'][i]['snippet']['description']
      video_description = self.regex_description(video_description)
      videos_dict.update({(i + looper): {'id':video_id, 'title':video_title,'desc':video_description} })
      i += 1
    # token, looper = self.check_playlist_pagetoken(looper, data_dict)
    # videos_dict = self.get_all_pages(token, looper, videos_dict)
    token, looper = get_page_token(data_dict, looper)
    return videos_dict, token, looper

  def get_all_pages(self, token, looper, videos_dict):
    while token != '':
      token_in_url = f"&pageToken={token}"
      next_api_playlistsitems_url = self.api_url + token_in_url
      next_playlists_items_data = self.create_data_dict(next_api_playlistsitems_url)
      new_playlist_items = self.create_playlist_items_dict(looper, next_playlists_items_data)
      videos_dict.update(new_playlist_items)
      token = self.check_playlist_pagetoken(next_playlists_items_data)
    return videos_dict

  def check_playlist_pagetoken(self, looper, data=None):
    token = ''
    if data is None: 
      data = self.create_data_dict()
    try:
      token = data['nextPageToken']
      if looper == 0:
        looper = 50
      elif looper == 50:
        looper = 100
      elif looper == 150:
        looper = 200
      elif looper == 200:
        looper = 250
      elif looper == 250:
        looper = 300
      elif looper == 300:
        looper = 400
      elif looper == 400:
        looper = 450
      elif looper == 450:
        looper = 500
      elif looper == 500:
        looper = 550
      elif looper == 550:
        looper = 600
      elif looper == 600:
        looper = 650
      elif looper == 650:
        looper = 700
      elif looper == 700:
        looper = 750
    except:
      token = '' 
    return token, looper

# Functions
def create_playlists_url(channel_id, api_key):
  api_playlists_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=50&channelId={channel_id}&key={api_key}"
  return api_playlists_url

def create_playlistitems_url(playlist_id, api_key):
  playlistitems_api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"
  return playlistitems_api_url

def get_data_dict(url):
  json_url = urllib.request.urlopen(url)
  data = json.loads(json_url.read())
  return data

def create_playlists_dict(data_dict):
  plist_dict = {}  
  i = 0
  while i < len(data_dict['items']):
    plist_title = data_dict['items'][i]['snippet']['title']
    plist_id = data_dict['items'][i]['id']
    plist_dict.update( {plist_title : plist_id} )
    i += 1
  return plist_dict

def scrub_title(stitle):
  stitle = re.sub("[\",?']+", "", stitle)
  stitle = re.sub("[|:]+", "-", stitle)
  return stitle

def get_max_row(active_sheet):
  maxRow = None
  counter = 2 #start on row after header
  while (counter < (active_sheet.max_row + 1)):
    currentA = "A" + str(counter)
    valA = active_sheet[currentA].value
    if valA == None:
      maxRow = int(counter)
      break
    counter = counter + 1

  if maxRow == None:
    maxRow = active_sheet.max_row + 1
  return maxRow

def create_playlist_directory_if_needed(Playlist):
  data_folder = Path(r"C:\Users\clemmer\myComp\code\python\JBS Playlists")
  dir_name = scrub_title(playlist.get_title())
  dir_path = data_folder / dir_name
  # Create directory if don't exist
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)

def download_video(video_api_url, output_path, file_title, filepath, counter):
  filepath = str(filepath) + ".mp4"
  if not os.path.exists(filepath):
    try:
      YouTube(video_api_url).streams.first().download(output_path=output_path,filename=file_title)
    except:
      print("Video " + str(counter) + "did not dl")
  else:
    print(filepath + "\nalready exists")

def get_page_token(data, looper):
  try:
    token = data['nextPageToken']
    if looper == 0:
      looper = 50
    elif looper == 50:
      looper = 100
    elif looper == 150:
      looper = 200
    elif looper == 200:
      looper = 250
    elif looper == 250:
      looper = 300
    elif looper == 300:
      looper = 400
    elif looper == 400:
      looper = 450
    elif looper == 450:
      looper = 500
    elif looper == 500:
      looper = 550
    elif looper == 550:
      looper = 600
    elif looper == 600:
      looper = 650
    elif looper == 650:
      looper = 700
    elif looper == 700:
      looper = 750
  except:
    token = '' 
  return token, looper

# vars
channel_id = 'UCD_PvRz7fvX9WOBL6T4P45Q'
api_key = 'AIzaSyBAdbm6MkWm_2HbDfXnbRWmbKYTRPmOHfY'
# playlist_to_backup = sys.argv[1]
playlist_to_backup = 'JBS Straight Talk'
looper = 0

data_folder = Path(r"C:\Users\clemmer\myComp\code\python\JBS Playlists")
excel_file_name = "masterfile.xlsx"
excel_file = data_folder / excel_file_name
log_file_name = "log.txt"
logfile = data_folder / log_file_name

# Start
# ------
#create files and/or clear contents
file_to_write_to = open(logfile, "a+", encoding='utf-8')
file_to_write_to.truncate(0)
f = file_to_write_to

# start excel
wb = openpyxl.load_workbook(excel_file)
ws = wb.active
maxRow = get_max_row(ws)
print("Excel Start Row: " + str(maxRow))

# Create url for list of playlists belonging to JBS channel ID
playlists_api_url = create_playlists_url(channel_id, api_key)

# create dictionary of playlists' titles & ids
playlists_data = get_data_dict(playlists_api_url) 
playlists_dict = create_playlists_dict(playlists_data)

# start array for playlist objects
playlist_objects = []
for playlist_title, playlist_id in playlists_dict.items(): 
  videos_api_url = create_playlistitems_url(playlist_id, api_key)
  # array of playlist objects
  playlist_objects.append( Playlist(playlist_title, playlist_id, videos_api_url) )

for playlist in playlist_objects:
  videos = ''
  if playlist.get_title() == playlist_to_backup:
    firstpage_data = playlist.create_data_dict()
    videos, token, looper = playlist.create_playlist_items_dict(looper, firstpage_data)
    while token != '':
      token_in_url = f"&pageToken={token}"
      next_api_playlistsitems_url = playlist.get_api_url() + token_in_url
      next_playlists_items_data = playlist.create_data_dict(next_api_playlistsitems_url)
      videos, token, looper = playlist.create_playlist_items_dict(looper, next_playlists_items_data, videos)
  if videos != '':
    print(len(videos))
    create_playlist_directory_if_needed(playlist)
    counter = maxRow
    for v in videos.values():
      if v['title'] == "Private video":
        continue
      playlist_title = playlist.get_title()
      playlist_folder_title = scrub_title(playlist_title)
      file_title = scrub_title(v['title'])
      file_location = data_folder / playlist_folder_title / file_title
      ws["A" + str(counter)].value = playlist_title 
      ws["B" + str(counter)].value = v['title']
      ws["C" + str(counter)].value = v['desc']
      ws["D" + str(counter)].value = str(file_location) + ".mp4"
      # youtube download
      video_url_dl = f"https://www.googleapis.com/youtube/v3/watch?v={v['id']}"
      output_path = data_folder / playlist_folder_title
      download_video(video_url_dl, output_path, file_title, file_location, counter)
      counter += 1

f.close()
wb.save(excel_file)
