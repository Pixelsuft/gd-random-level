import os
import sys
import random
import gd
from asyncio import run
from PyQt5 import QtWidgets, QtGui
from files.random_level_ui import Ui_MainWindow


client = gd.Client()
is_compiled = not ('python' in sys.executable.lower().strip())
cur_path = os.path.dirname(__file__)


def register_exception(exception):
    if is_compiled:
        return
    print(f'Exception: {exception}')


def on_quit(exit_code: int = 0):
    if exit_code == 0:
        return 0
    print(f'App crashed with error code: {exit_code}')
    return 1


def generate_button_click():
    min_val = ui.minidBox.value()
    max_val = ui.maxidBox.value()
    if min_val > max_val:
        max_val, min_val = min_val, max_val
    level_id = 0
    level_ = None
    while True:
        try:
            level_id = random.randint(min_val, max_val)
            level_ = run(client.get_level(level_id))
            break
        except Exception as err_:
            register_exception(err_)
            continue
    clipboard = app.clipboard()
    clipboard.clear(mode=clipboard.Clipboard)
    clipboard.setText(str(level_id), mode=clipboard.Clipboard)
    if level_.difficulty.name == 'AUTO':
        difficulty_path = 'difficulty_auto_btn_001.png'
    elif level_.difficulty.name == 'NA':
        difficulty_path = 'difficulty_00_btn_001.png'
    elif level_.difficulty.name == 'EXTREME_DEMON':
        difficulty_path = 'difficulty_10_btn_001.png'
    elif level_.difficulty.name.endswith('_DEMON'):
        difficulty_path = f'difficulty_0{str(level_.difficulty.value + 5)}_btn_001.png'
    else:
        difficulty_path = f'difficulty_0{str(level_.difficulty.value)}_btn_001.png'
    difficulty_img = QtGui.QPixmap(os.path.join(cur_path, 'files', difficulty_path))
    ui.difficultIcon.setPixmap(difficulty_img)
    ui.nameLabel.setText(level_.name)
    ui.authorLabel.setText('By: ' + level_.creator.name)
    like_prefix = '' if level_.rating >= 0 else 'dis'
    like_img = QtGui.QPixmap(os.path.join(cur_path, 'files', f'GJ_{like_prefix}likesIcon_001.png'))
    ui.likeIcon.setPixmap(like_img)
    ui.likeLabel.setText(str(level_.rating))
    ui.downloadsLabel.setText(str(level_.downloads))
    ui.lengthLabel.setText(level_.length.title)
    ui.idLabel.setText('Level ID: ' + str(level_id))
    ui.musicLabel.setText(level_.song.name)
    ui.musicauthorLabel.setText('By: ' + level_.song.author)
    ui.musicidLabel.setText('Song ID: ' + str(level_.song.id))
    if level_.stars > 0:
        ui.starsLabel.setText(str(level_.stars))
        ui.starsLabel.setVisible(True)
        ui.starsIcon.setVisible(True)
    else:
        ui.starsLabel.setVisible(False)
        ui.starsIcon.setVisible(False)
    ui.descEdit.setHtml(
        '''<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px;
 margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'''.strip() +
        level_.description.strip() +
        '</p></body></html>'.strip()
    )


def on_init():
    ui.generateButton.clicked.connect(generate_button_click)


app = QtWidgets.QApplication([__file__])
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
on_init()
MainWindow.show()
sys.exit(on_quit(app.exec_()))
