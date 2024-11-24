import dearpygui.dearpygui as dpg
from app.Window import Window

dpg.create_context()
dpg.create_viewport(title="MainWindow", width=800, height=600, vsync=True, decorated=False, resizable=False)

Window()
dpg.set_primary_window("WindowP", True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()