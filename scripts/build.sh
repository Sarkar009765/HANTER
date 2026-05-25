#!/bin/bash
echo "Building BRO-AI for all platforms..."

cd "$(dirname "$0")/.."

# Build frontend
cd apps/desktop
npm run tauri-build
cd ../..

echo "Build complete! Installers are in apps/desktop/src-tauri/target/release/bundle/"
