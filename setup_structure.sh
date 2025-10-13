#!/bin/bash

echo "🚀 Setting up Fitfilter project structure..."

# Root-level folders
mkdir -p static media docs requirements
echo "📁 Created: static/, media/, docs/, requirements/"

# App-level static and templates structure
for app in accounts affiliates products recommendations reviews; do
  mkdir -p $app/static/$app $app/templates/$app
  echo "📂 Ensured folders for app: $app"
done

# Utility, environment, and deployment files
touch fitfilter_project/utils.py .env.example Procfile
echo "🧩 Created: utils.py, .env.example, and Procfile"

# Base static structure
mkdir -p static/css static/js static/img
touch static/css/base.css static/js/main.js
echo "🎨 Added base CSS/JS folders and placeholder files"

# Requirements setup
echo "# Base dependencies" > requirements/base.txt
echo "# Dev-specific dependencies" > requirements/dev.txt
echo "# Production dependencies" > requirements/prod.txt
echo "🧱 Added requirements structure"

# Docs placeholder
echo "# Fitfilter Project Documentation" > docs/README.md
echo "🗒️  Added documentation placeholder"

# Permissions
chmod +x setup_structure.sh

echo "✅ Structure setup complete. You're good to go!"
