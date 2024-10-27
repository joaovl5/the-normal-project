#!/bin/bash
echo "Informe o ID da versão: "
read version_id

file_path=".env"

sed -i "s/^VERSION=.*/VERSION=$version_id/" "$file_path"

scripts/build-windows.fish

mv release/windows.zip release/$version_id.zip