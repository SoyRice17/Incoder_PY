import gui.gui_manager as gui
import util.io_manager as io
import util.init_path as path
import util.config_creator as config

if __name__ == "__main__":
    config.ConfigCreator().create_config()
    gui.GuiManager().run()


