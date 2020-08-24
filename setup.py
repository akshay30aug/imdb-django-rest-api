import os

packages = ['django','djangorestframework','python3-venv','requests','bs4','pillow']

for i in packages:
	os.system("python3 -m pip install "+i)
