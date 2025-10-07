pyinstaller --onefile src/client.py
pyinstaller --onefile src/server.py
cp -r src/font dist/
cp src/client.conf dist/
cp src/server.conf dist/