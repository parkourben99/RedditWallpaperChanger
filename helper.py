import os
from configparser import ConfigParser
from os import listdir
from gi.repository import Notify, GdkPixbuf


class Helper(object):
    def get_config(self):
        config_file_path = os.path.dirname(os.path.realpath(__file__)) + '/config.ini'
        if not os.path.exists(config_file_path):
            return self.check_config(None)

        config_reader = ConfigParser()
        config_reader.read(config_file_path)

        config = {}
        config['wallpapers_directory'] = config_reader.get('settings', 'wallpapers_directory')
        config['refresh_rate'] = config_reader.get('settings', 'refresh_rate')
        config['subs'] = config_reader.get('settings', 'subs')
        config['only_local'] = config_reader.get('settings', 'only_local')
        config['over_18'] = config_reader.get('settings', 'allow_nsfw')

        if not config['subs'] == "":
            config['subs'] = config['subs'].split(',')

        return self.check_config(config)

    def check_config(self, config):
        if config is None:
            config = {}
            config['wallpapers_directory'] = '~/Pictures/RedditWallpapers/'
            config['refresh_rate'] = 120
            config['subs'] = ['wallpapers']
            config['only_local'] = False
            config['over_18'] = False

        config['wallpapers_directory'] = config['wallpapers_directory'].replace('~', os.path.expanduser("~"))
        os.system("mkdir -p " + config['wallpapers_directory'])

        if len(config['subs']) <= 0:
            config['subs'] = ['wallpapers']

        if not str(config['refresh_rate']).isdigit():
            config['refresh_rate'] = 120

        if config['only_local'] == '':
            config['only_local'] = False

        if config['over_18'] == '':
            config['over_18'] = False

        return config

    def set_wallpaper(self, image):
        print('loading new wallpaper' + image)
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + image)
        self.send_notifaction()

    def send_notifaction(self):
        Notify.init("Wallpaper Changer")
        notification = Notify.Notification.new(
            'New wallpaper has been set!',
            #'this is the body',
        )

        image = GdkPixbuf.Pixbuf.new_from_file(os.path.dirname(os.path.realpath(__file__)) + '/alien.png')
        notification.set_image_from_pixbuf(image)

        notification.show()

    def clean_up(self):
        config = self.get_config()
        all_files = listdir(config['wallpapers_directory'])

        for image in all_files:
            file = config['wallpapers_directory'] + image

            if os.stat(file).st_size == 0:
                os.remove(file)
