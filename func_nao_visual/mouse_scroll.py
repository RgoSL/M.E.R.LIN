def mouse_scroll(frame, speed=70):

    def _on_mousewheel(event):
        frame._parent_canvas.xview_scroll(int(-1*(event.delta/120) * speed), "units")

    frame.bind_all("<MouseWheel>", _on_mousewheel)

    frame.bind_all("<Button-4>", lambda e: frame._parent_canvas.yview_scroll(-1, "units"))
    frame.bind_all("<Button-5>", lambda e: frame._parent_canvas.yview_scroll(1, "units"))