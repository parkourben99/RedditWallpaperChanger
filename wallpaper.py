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
        self.image_url = self.get_image()
        self.image_name = self.get_image_name(self.image_url)
        self.download_image()
        self.set_wallpaper()

    def validate_image(self, sub):
        if sub.over_18 and not self.config['over_18']: return False

        file_name = self.get_image_name(sub.url)
        file_name = self.config['wallpapers_directory'] + file_name

        file_exts = ('png', 'bmp', 'jpeg', 'jpg')
        if not sub.url.endswith(file_exts): return False

        if file_name == '' or sub.url == '': return False

        return not os.path.exists(file_name)

    def get_image(self):
        sub_reddit = random.choice(self.config['subs']).strip()

        reddit = praw.Reddit('wallpaper changer for linux by /u/parkourben99')
        images = reddit.get_subreddit(sub_reddit)

        for sub in images.get_hot(limit=150):
            if self.validate_image(sub):
                print('Downloading image form /r/' + sub_reddit)
                return sub.url

    def get_image_name(self, file_name):
        file_name = file_name.split('/')
        return file_name[len(file_name) - 1]

    def download_image(self):
        local_file = self.config['wallpapers_directory'] + self.image_name
        open(local_file, 'w+').close()
        print('saving image to ' + local_file)
        urllib.request.urlretrieve(self.image_url, local_file)

    def set_wallpaper(self):
        image_path = self.config['wallpapers_directory'] + self.image_name
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + image_path)


class ChooseRandomWallPaper(object):
    def __init__(self, config):
        self.config = config
        print('Picking a random one from the matrix')
        self.set_wallpaper(self.choose_wallPaper())

    def choose_wallPaper(self):
        fileName = random.choice(listdir(self.config['wallpapers_directory']))
        return self.config['wallpapers_directory'] + fileName

    def set_wallpaper(self, image):
        print('loading new wallpaper' + image)
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + image)


if __name__ == "__main__":
    helper = Helper()
    config_settings = helper.get_config()

    try:
        if random.choice([1, 2]) == 1:
            BackGroundChanger(config_settings)
        else:
            ChooseRandomWallPaper(config_settings)
    except Exception as e:
        ChooseRandomWallPaper(config_settings)

    helper.clean_up(config_settings)

