import flet as ft 
import settings
from wallpaper_manager import WallpaperManager, Wallpaper
from utils import change_wallpaper, get_current_wallpaper


def main(page: ft.Page):
	wp = WallpaperManager(settings.directory)

	page.title = settings.title
	if settings.center:
		page.window.center()
	page.window.min_width, page.window.min_height = settings.x, settings.y
	
	dlg = ft.AlertDialog(
		title=ft.Text(f"Credits:"),
		content=ft.Text(spans=
				  	[
						ft.TextSpan("Github: github.com/PERL54/wallpaper_pyngine", ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE), on_click=lambda e: page.set_clipboard("https://github.com/PERL54/wallpaper_pyngine"))
					]),
		alignment=ft.alignment.center,
		title_padding=ft.padding.all(25)
	)

	#main_title = ft.Text(f"Wallpaper Pyngine v{settings.version}", size=25, weight=ft.FontWeight.BOLD, on_tap=lambda e: page.open(dlg))
	main_title = ft.Text(size=25, weight=ft.FontWeight.BOLD, spans=[ft.TextSpan(text=f"{settings.title} v{settings.version}", on_click=lambda e: page.open(dlg))])
	active_title = ft.Text(value = "Tap to choose wallpaper!", size=15, selectable=True)
	page.add(
		ft.Column(controls=[
			main_title,
			active_title
		])
	)


	wallpaper_grid = ft.GridView(
		expand = 1,
		runs_count = 5,
		max_extent = 350,
		child_aspect_ratio = 1.0,
		spacing = 5,
		run_spacing = 5
		)
	

	def image_click(e):
		desc_image.src = e.get_wallpaper_path()
		desc_size.value = f"Размер: {e.get_wallpaper_size()['width']} на {e.get_wallpaper_size()['height']} пикс."
		desc_weigth.value = f"Вес: {e.get_wallpaper_weigth()} МБ"
		wp.selected_wallpaper = e
		desc_set_wallpaper_btn_btn.disabled = False
		page.update()


	def image_hover(e):
		active_title.value = e.get_wallpaper_name()
		page.update()


	def reload_wallpaper_grid_btn(e):
		wp.reload_wallpaper_list()
		wallpaper_grid.controls = []
		fill_grid()
		page.update()
		pass
	
	def restore_wallpaper_btn(e):
		desc_image.src = wp.current_wallpaper.get_wallpaper_path()
		desc_size.value = f"Размер: {wp.current_wallpaper.get_wallpaper_size()['width']} на {wp.current_wallpaper.get_wallpaper_size()['height']} пикс."
		desc_weigth.value =f"Вес: {wp.current_wallpaper.get_wallpaper_weigth()} МБ"
		wp.selected_wallpaper = wp.current_wallpaper
		change_wallpaper(wp.current_wallpaper.get_wallpaper_path())
		desc_set_wallpaper_btn_btn.disabled = True
		page.update()


	def set_wallpaper_btn(e):
		change_wallpaper(wp.selected_wallpaper.get_wallpaper_path())
		page.update()


	desc_image  = ft.Image(src=wp.current_wallpaper.get_wallpaper_path(), height=250, fit=ft.ImageFit.FIT_HEIGHT, border_radius=ft.border_radius.all(10))
	desc_size   = ft.Text(value = f"Размер: {wp.current_wallpaper.get_wallpaper_size()['width']} на {wp.current_wallpaper.get_wallpaper_size()['height']} пикс.")
	desc_weigth = ft.Text(value = f"Вес: {wp.current_wallpaper.get_wallpaper_weigth()} МБ")
	desc_set_wallpaper_btn_btn = ft.ElevatedButton(text = "Установить обои", expand=1, on_click=set_wallpaper_btn, disabled=True)
	desc_column = ft.Container(width=350,
							expand=0,
							content=ft.Column(controls=[
														desc_image,
														desc_size,
														desc_weigth,
														ft.Divider(),
														ft.Row(controls = [
															ft.ElevatedButton(text = "Восстановить", expand = 1, on_click=restore_wallpaper_btn),
															desc_set_wallpaper_btn_btn
														]),
														ft.Container(alignment=ft.alignment.bottom_right, expand = 1, content=ft.ElevatedButton(text="Обновить список", on_click=reload_wallpaper_grid_btn, bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE))						
															]
											)
								)


	page.add(
		ft.Row(controls=[
			wallpaper_grid,
			desc_column
			],
			expand=1)
		)
	

	def fill_grid():
		for i in wp.get_wallpaper_list():
			image = ft.Image(
				src = i.get_wallpaper_path(),
				fit = ft.ImageFit.FIT_HEIGHT,
				repeat = ft.ImageRepeat.NO_REPEAT,
				border_radius = ft.border_radius.all(10))
			wallpaper_grid.controls.append(
				ft.GestureDetector(content = image, 
					  			on_tap = lambda e, x = i: image_click(x), 
								on_hover=lambda e, x = i: image_hover(x),
								mouse_cursor=ft.MouseCursor.CLICK)
			)
	fill_grid()
	page.update()


ft.app(main)