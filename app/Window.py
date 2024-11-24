import dearpygui.dearpygui as dpg
from app.components.StatusBar import StatusBar


def Window():
    with dpg.window(tag="WindowP", label="Ventana principal", width=800, height=600, collapsed=False,no_resize=True, no_move=False):
        StatusBar()


