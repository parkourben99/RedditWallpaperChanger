import os
import os.path
import random
import praw
import urllib.request
from os import listdir
from helper import Helper


class BackGroundChanger(object):
    def __init__(self, config):
        self.config = config
        self.image_url = self.getImage()
        self.image_name = self.getImageName(self.image_url)
        self.downloadImage()
        self.setWallpaper()

    def validateImage(self, sub):
        if sub.over_18 and not self.config['over_18']: return False

        file_name = self.getImageName(sub.url)
        file_name = self.config['wallpapers_directory'] + file_name

        file_exts = ('png', 'bmp', 'jpeg', 'jpg')
        if not sub.url.endswith(file_exts): return False

        if file_name == '' or sub.url == '': return False

        return not os.path.exists(file_name)

    def getImage(self):
        subreddit = random.choice(self.config['subs']).strip()

        reddit = praw.Reddit('wallpaper changer for linux by /u/parkourben99')
        images = reddit.get_subreddit(subreddit)

        for sub in images.get_hot(limit=150):
            if self.validateImage(sub):
                print('Downloading image form /r/' + subreddit)
                return sub.url

    def getImageName(self, fileName):
        file_name = fileName.split('/')
        return file_name[len(file_name) - 1]

    def downloadImage(self):
        local_file = self.config['wallpapers_directory'] + self.image_name
        open(local_file, 'w+').close()
        print('saving image to ' + local_file)
        urllib.request.urlretrieve(self.image_url, local_file)

    def setWallpaper(self):
        image_path = self.config['wallpapers_directory'] + self.image_name
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + image_path)


class ChooseRandomWallPaper(object):
    def __init__(self, config):
        self.config = config
        print('Picking a random one from the matrix')
        self.setWallpaper(self.chooseWallPaper())

    def chooseWallPaper(self):
        fileName = random.choice(listdir(self.config['wallpapers_directory']))
        return self.config['wallpapers_directory'] + fileName

    def setWallpaper(self, imagePath):
        print('loading new wallpaper' + imagePath)
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + imagePath)


if __name__ == "__main__":
    helper = Helper()
    configSettings = helper.get_config()

    try:
        if random.choice([1, 2]) == 1:
            BackGroundChanger(configSettings)
        else:
            ChooseRandomWallPaper(configSettings)
    except Exception as e:
        ChooseRandomWallPaper(configSettings)

    helper.clean_up(configSettings)