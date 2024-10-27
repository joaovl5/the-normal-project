#!/usr/bin/fish

# Clean previous builds
rm -rf dist __pycache__ build release/windows
rm release/windows.zip start.spec

# Build vue
scripts/build.fish

# Build python app
mkdir -p release/windows/bin

echo "Rodando build electron e python em paralelo..."

# wine python -m eel start.py web -i logo.ico --noconsole
wine cxfreeze -c start.py --target-dir dist_start --icon logo.ico --include-files .env,web --base-name gui &
# Electron builder
pnpm run build:w

wait

cp -r dist_start/* release/windows/
cp -r web release/windows/
cp .env release/windows/
cp -r dist/win-unpacked/* release/windows/bin

# UPX compression
# upx release/windows/start.exe 
# upx release/windows/bin/launchernormal.exe

# Compress archive
cd release/windows/
zip -r ../windows.zip .
