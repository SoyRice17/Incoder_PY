class EntryManager:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager
        
    def set_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(fg="gray")
        entry.bind("<FocusIn>", lambda event: self._on_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self._on_focus_out(event, entry, placeholder))
        
    def _on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            entry.config(fg="black")
            
    def _on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")