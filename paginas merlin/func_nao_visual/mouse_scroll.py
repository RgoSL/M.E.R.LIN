def mouse_scroll(frame, speed=70):

    def _on_mousewheel(event):
        # rola o canvas interno do CTkScrollableFrame
        frame._parent_canvas.xview_scroll(int(-1*(event.delta/120) * speed), "units")

    # Windows e Mac usam <MouseWheel>
    frame.bind_all("<MouseWheel>", _on_mousewheel)

    # Linux usa <Button-4> e <Button-5>
    frame.bind_all("<Button-4>", lambda e: frame._parent_canvas.yview_scroll(-1, "units"))
    frame.bind_all("<Button-5>", lambda e: frame._parent_canvas.yview_scroll(1, "units"))
