@echo off
title building...
color 0a
pyinstaller -F -w -i files\icon.ico --uac-admin --add-data "files;files" main.py
echo ok
pause
