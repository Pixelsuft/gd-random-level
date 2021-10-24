@echo off
title building...
color 0a
del files\random_level_ui.py
pyuic5 random_level_ui.ui -o files\random_level_ui.py -x
echo ok
