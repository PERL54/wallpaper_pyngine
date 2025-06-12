import flet as ft
import settings
from wallpaper_manager import WallpaperManager, Wallpaper
from utils import set_wallpaper


def main(page: ft.Page):
    # ========= Init ==================
    wp = WallpaperManager(settings.directory)

    page.title = settings.title
    if settings.center:
        page.window.center()
    page.window.min_width, page.window.min_height = settings.x, settings.y

    # ========= Credits Dialog =======
    dlg = ft.AlertDialog(
        title=ft.Text(f"Credits:"),
        content=ft.Text(
            spans=[
                ft.TextSpan(
                    "Github: github.com/PERL54/wallpaper_pyngine",
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    on_click=lambda e: page.set_clipboard(
                        "https://github.com/PERL54/wallpaper_pyngine"
                    ),
                )
            ]
        ),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )

    # ========== Header Titles =========
    main_title = ft.Text(
        size=25,
        weight=ft.FontWeight.BOLD,
        spans=[
            ft.TextSpan(
                text=f"{settings.title} v{settings.version}",
                on_click=lambda e, s: page.open(dlg),
            )
        ],
    )
    active_title = ft.Text(value="Tap to choose wallpaper!", size=15, selectable=True)

    page.add(ft.Column(controls=[main_title, active_title]))

    # ========= Wallpapers Image Grid ========
    wallpaper_grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=350,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    # ======== Callback Button Funcs ==========
    def image_click(e):
        wp.selected_wallpaper = e
        desc_set_wallpaper_btn_btn.disabled = False
        change_description(e)
        page.update()

    def image_hover(e):
        active_title.value = e.get_wallpaper_name()
        page.update()

    def reload_wallpaper_grid_btn(e):
        wp.reload_wallpaper_list()
        wallpaper_grid.controls = []
        fill_grid()
        page.update()

    def restore_wallpaper_btn(e):
        change_description(wp.current_wallpaper)
        set_wallpaper(wp.current_wallpaper.get_wallpaper_path())
        wp.selected_wallpaper = wp.current_wallpaper
        desc_set_wallpaper_btn_btn.disabled = True
        page.update()

    def set_wallpaper_btn(e):
        set_wallpaper(wp.selected_wallpaper.get_wallpaper_path())
        page.update()

    def desc_image_click(e):
        image_dlg = ft.AlertDialog(
            title=e.get_wallpaper_name(),
            actions=[
                ft.ElevatedButton(
                    text="Закрыть",
                    on_click=lambda e: page.close(image_dlg),
                    bgcolor=ft.Colors.RED_400,
                    color=ft.Colors.WHITE,
                )
            ],
            content=ft.Image(e.get_wallpaper_path(), fit=ft.ImageFit.COVER),
        )
        page.open(image_dlg)

    def change_description(wallpaper: Wallpaper):
        desc_image.src = wallpaper.get_wallpaper_path()
        desc_size.value = f"Размер: {wallpaper.get_wallpaper_size()['width']} на {wallpaper.get_wallpaper_size()['height']} пикс."
        desc_weigth.value = f"Вес: {wallpaper.get_wallpaper_weigth()} МБ"
        desc_image_container.on_tap = lambda e, x=wallpaper: desc_image_click(x)

    # =========== Right Column ==============
    desc_image = ft.Image(
        src=wp.current_wallpaper.get_wallpaper_path(),
        height=250,
        fit=ft.ImageFit.FIT_HEIGHT,
        border_radius=ft.border_radius.all(10),
    )
    desc_image_container = ft.GestureDetector(
        content=desc_image, on_tap=lambda e, x=wp.current_wallpaper: desc_image_click(x)
    )
    desc_size = ft.Text(
        value=f"Размер: {wp.current_wallpaper.get_wallpaper_size()['width']} на {wp.current_wallpaper.get_wallpaper_size()['height']} пикс."
    )
    desc_weigth = ft.Text(
        value=f"Вес: {wp.current_wallpaper.get_wallpaper_weigth()} МБ"
    )
    desc_set_wallpaper_btn_btn = ft.ElevatedButton(
        text="Установить обои", expand=1, on_click=set_wallpaper_btn, disabled=True
    )

    desc_column = ft.Container(
        width=350,
        expand=0,
        content=ft.Column(
            controls=[
                desc_image_container,
                desc_size,
                desc_weigth,
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Восстановить",
                            expand=1,
                            on_click=restore_wallpaper_btn,
                        ),
                        desc_set_wallpaper_btn_btn,
                    ]
                ),
                ft.Container(
                    alignment=ft.alignment.bottom_right,
                    expand=1,
                    content=ft.ElevatedButton(
                        text="Обновить список",
                        on_click=reload_wallpaper_grid_btn,
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
            ]
        ),
    )

    page.add(ft.Row(controls=[wallpaper_grid, desc_column], expand=1))

    # ============== Fill grid by images ===============
    # ==== Used when app init and update list files ====
    def fill_grid():
        for i in wp.get_wallpaper_list():
            image = ft.Image(
                src=i.get_wallpaper_path(),
                fit=ft.ImageFit.FIT_HEIGHT,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
            wallpaper_grid.controls.append(
                ft.GestureDetector(
                    content=image,
                    on_tap=lambda e, x=i: image_click(x),
                    on_hover=lambda e, x=i: image_hover(x),
                    mouse_cursor=ft.MouseCursor.CLICK,
                )
            )

    fill_grid()
    page.update()
