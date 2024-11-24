import dearpygui.dearpygui as dpg
def StatusBar():
    with dpg.child_window(tag="StatusBar", label="Status Bar", width=800, height=30, no_scrollbar=True, border=False, pos=(0, 0)):
        dpg.add_text("Estado: En ejecución", tag="status_text", pos=(10, 5))
        width = dpg.get_viewport_width()
        dpg.add_button(label="X", callback=lambda: dpg.stop_dearpygui(), width=20, height=20, pos=(width-30, 5))

        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(callback=drag_handler, user_data="status_text")
        dpg.bind_item_handler_registry("status_text", "drag_handler")


def drag_handler(sender, app_data):
    mouse_pos = dpg.get_mouse_pos()
    viewport_pos = dpg.get_viewport_pos()
    global_pos = (mouse_pos[0] + viewport_pos[0], mouse_pos[1] + viewport_pos[1])
    dpg.set_viewport_pos(global_pos)
    