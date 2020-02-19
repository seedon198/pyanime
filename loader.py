import time
import pyloader
import urllib
import requests
from bs4 import BeautifulSoup


def progress_callback(progress):
    print(progress.dlable.file_name, '{0:.2f}%'.format(progress.percent))
    return False


def url_resolver(item):
    # item.url = 'http://new.url'
    return item


def get_video_links(): 
    r = requests.get(archive_url)  
    soup = BeautifulSoup(r.content, "lxml")
    links = soup.findAll('a') 
    video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mkv')] 
    return video_links 


if __name__ == '__main__':
    # Create a loader instance
    loader = pyloader.Loader.get_loader()
    loader.configure(
        max_concurrent=3,
        update_interval=15,
        progress_cb=progress_callback,
        url_resolve_cb=url_resolver,
        daemon=False
    )

    # Start the loader
    # Make sure you know how the `daemon` flag
    # affects the liftime of your program
    loader.start()

    # This might not last forever so you will have to replace this link with a working link
    # use google dork intitle:"Index of /" "Anime" to find one with directory listing enabled.
    
    archive_url = "https://storage.kanzaki.ru/ANIME___/One_Piece/"
    video_links = get_video_links()
    for link in video_links:
        item = pyloader.DLable( url = link, 
            target_dir='/Volumes/BRICK/Media/Anime/one_piece', 
            file_name= urllib.parse.unquote(link.split('/')[-1]))
        loader.queue(item)

    # True if both necessary main threads are still alive and kicking
    print('Main Thread Running:', loader.is_alive())
    # True if items are queued and/or downloading
    print('Files Queued & downloading:', loader.is_active())
    # Amount of queued items
    print('Pending Downloads:', loader.queued)
    # Amount of active/downloading items
    print('Active Downloads:', loader.active)
    # The amount of maximum concurrent allowed downloads
    print('Max concurrent:', loader.max_concurrent)
    # Will also trigger new downloads if necessary
    # How often the progress callback will be called in seconds
    print('Update interval:', loader.update_interval)


    # Wait for all downloads to finish
    while loader.is_active():
        time.sleep(0.25)

    loader.exit()
