import gui.guiManager as gui
import util.IOManager as io
import util.initPATH as path
import util.config_creator as config

if __name__ == "__main__":
    config.ConfigCreator().create_config()
    gui.GuiManager().run()


