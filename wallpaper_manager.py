from os import *
from utils import set_wallpaper, get_current_wallpaper
from PIL import Image

img_formats = (".jpg", ".png", ".jpeg")


class WallpaperManager(object):
    """
    Main WallpaperPyngine Module!
    Using:
            wp = WallpaperManager('directory')
    """

    def __init__(self, directory: str):
        self.wp_list = []
        if path.isdir(directory):
            self.directory = directory
            self.__load_wallpaper_list()
            self.selected_wallpaper = self.get_current_wallpaper()
            self.current_wallpaper = self.get_current_wallpaper()
        else:
            raise ValueError(f"{directory} - is not a directory, or have a mistakes.")

    def __is_image(self, filename) -> bool:
        if (
            path.isfile(path.abspath(path.join(self.directory, filename)))
            and path.splitext(filename)[1] in img_formats
        ):
            return True
        else:
            return False

    def __load_wallpaper_list(self):
        files = listdir(self.directory)
        for i in files:
            if self.__is_image(i):

                self.wp_list.append(
                    Wallpaper(
                        path.abspath(path.join(self.directory, i)),
                        self.__get_wallpaper_weight(
                            path.abspath(path.join(self.directory, i))
                        ),
                        self.__get_wallpaper_size(
                            path.abspath(path.join(self.directory, i))
                        ),
                    )
                )
            else:
                print(f"[{i}]" + " is not an image!")

    def get_wallpaper_list(self):
        return self.wp_list

    def reload_wallpaper_list(self) -> None:
        self.wp_list = []
        self.__load_wallpaper_list()

    def get_current_wallpaper(self):
        current = get_current_wallpaper()
        return Wallpaper(
            wallpaper_path=current,
            weigth=self.__get_wallpaper_weight(current),
            size=self.__get_wallpaper_size(current),
        )

    def set_wallpaper(self, src: str) -> bool:
        if set_wallpaper(src):
            return True
        else:
            return False

    def __get_wallpaper_size(self, src: str) -> dict:
        with Image.open(src) as im:
            return {"width": im.width, "height": im.height}

    def __get_wallpaper_weight(self, src: str):
        file_size = format(round(path.getsize(src) / (1024 * 1024), 3))
        return file_size


class Wallpaper(WallpaperManager):
    def __init__(self, wallpaper_path: str, weigth: int, size: dict):
        self.path = wallpaper_path
        self.name = path.basename(wallpaper_path)
        self.weigth = weigth
        self.size = size

    def get_wallpaper_size(self):
        return self.size

    def get_wallpaper_path(self):
        return self.path

    def get_wallpaper_weigth(self):
        return self.weigth

    def get_wallpaper_name(self):
        return self.name
