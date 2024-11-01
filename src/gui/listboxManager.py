class ListboxManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        
    def delete_selected_file_name(self, event) -> None:
        delete_name = self.gui_instance.selected_file_name_listbox.get(self.gui_instance.selected_file_name_listbox.curselection())
        if not delete_name:
            return
        for i in range(self.gui_instance.selected_file_name_listbox.size()):
            if self.gui_instance.selected_file_name_listbox.get(i) == delete_name:
                self.gui_instance.selected_file_name_listbox.delete(i)
                break

    def insert_input_file_name_entry(self, event) -> None:
        input_name = self.gui_instance.file_listbox.get(self.gui_instance.file_listbox.curselection())
        self.gui_instance.input_file_name_entry.insert(0, input_name)
