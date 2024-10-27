#!/usr/bin/fish
scripts/build.fish
mkdir -p release/linux/bin
python -m eel start.py web --onefile --noconsole
cp dist/start release/linux/
npm run build
cp -r dist/linux-unpacked/* release/linux/bin