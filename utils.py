import ctypes
import platform

def change_wallpaper(src):
	if platform.system() == "Windows":
		if ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, src, 3):
			return True
		else: 
			return False
	else:
		raise Exception("Currently, this version of Wallpaper Pyngine support only Windows")

def get_current_wallpaper() -> str:
	path = ctypes.create_unicode_buffer(260)
	ctypes.windll.user32.SystemParametersInfoW(0x0073, ctypes.sizeof(path), path, 0)
	return str(path.value)
