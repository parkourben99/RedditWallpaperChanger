import os
import os.path
import random
import sys
import urllib.request
import requests
from os import listdir
from helper import Helper


class BackGroundChanger(object):
    def __init__(self, config, random_image=False):
        self.config = config
        self.image = None
        self.base_url = "https://www.reddit.com/r"

        # if bool(random.getrandbits(1)) and not random_image:
        #     try:
        self.image_url = self.get_image()
        self.image_name = self.get_image_name(self.image_url)
        self.download_image()
        self.image = self.image_name
            # except:
                # self.random_wallpaper()
        # else:
        #     self.random_wallpaper()

    def validate_image(self, sub):
        if sub['over_18'] and not self.config['over_18']:
            return False

        file_name = self.get_image_name(sub['url'])
        file_name = self.config['wallpapers_directory'] + file_name

        file_exts = ('png', 'bmp', 'jpeg', 'jpg')
        if not sub['url'].endswith(file_exts):
            return False

        if file_name == '' or sub['url'] == '':
            return False

        return not os.path.exists(file_name)

    def get_image(self):
        sub_reddit = random.choice(self.config['subs']).strip()
        url = "{}/{}/hot.json".format(self.base_url, sub_reddit)

        response_data = requests.get(url, headers={'User-agent': 'wallpaper changer for linux by /u/parkourben99'})

        images = []

        for post in response_data.json()['data']['children']:
            if self.validate_image(post['data']):
                images.append(post)

        return random.choice(images)['data']['url']

    def get_image_name(self, file_name):
        file_name = file_name.split('/')
        return file_name[len(file_name) - 1]

    def download_image(self):
        local_file = self.config['wallpapers_directory'] + self.image_name
        open(local_file, 'w+').close()
        print('saving image to ' + local_file)
        urllib.request.urlretrieve(self.image_url, local_file)

    def random_wallpaper(self):
        print('Picking a random one from the matrix')
        file_name = random.choice(listdir(self.config['wallpapers_directory']))
        self.image = self.config['wallpapers_directory'] + file_name


if __name__ == "__main__":
    random_image = False

    if len(sys.argv) > 1:
        random_image = True
        print(sys.argv[1])

    helper = Helper()
    changer = BackGroundChanger(helper.get_config(), random_image)

    helper.set_wallpaper(changer.image)
    helper.clean_up()

