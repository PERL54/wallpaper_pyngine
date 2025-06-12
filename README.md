# Wallpaper Pyngine (pet-project)
![Screenshot of program](https://i.ibb.co/KzjWYZHn/2025-06-11-185608.png)
### Wallpaper Pyngine v0.2.1 preview
----------
This simple program written using Python and Flet allows you to change wallpapers on Desktop. Now Wallpaper Pyngine supports only Windows. But in future, i swear, i add Linux distro support!


| File | Functions |
| ---- | --------- |
| ui.py | all Flet elements and UI logic |
|settings.py | program configuration file (min/max size, names, version and etc.) |
|wallpaper_manager.py | main wallpaper detect logic |
|utils.py | functions to change wallpaper and get current wallpaper |
|main.py | root of program. |



# Using
```bash
#First thing first check have you install Python or not
python -version

#After this:
pip install flet 

#Finally 
python main.py
```
---
Check `settings.py` and change `settings.directory` where you will put your wallpapers. By default it's `wallpapers` inside the main folder.

### What i want to do:
1. Add `drag&drop` support to add new pics to your folder via program.
2. ~~Open `preview window` when you click to image.~~
3. Maaaaybe add `browser to find pics in web` with your current screen size.
4. Add `multi-language support`.
5. "Compile" project to `one .exe file`.
6. ~~Add `requirements.txt` file and make setup more `friendly`.~~