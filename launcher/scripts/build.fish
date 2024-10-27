#!/usr/bin/fish

cp .env vue/quasar-project
cd vue/quasar-project
pnpm run build
rm -rf ../../web/*
cp -r dist/spa/* ../../web/
cd ../..
