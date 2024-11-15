#!/bin/bash

# Variables
REPO_PATH= git config --get remote.origin.url # Cambia esto a la ruta de tu repositorio local
COMMIT_MESSAGE="." # Cambia esto al mensaje que deseas para el commit
BRANCH_NAME="main" # Cambia esto al nombre de la rama si no estás usando 'main'

# Navegar al directorio del repositorio
cd "$REPO_PATH" || { echo "El directorio no existe: $REPO_PATH"; exit 1; }

# Añadir todos los cambios
git add .

# Realizar el commit
git commit -m "$COMMIT_MESSAGE"

# Hacer push a la rama especificada
git push origin "$BRANCH_NAME"

echo "Commit realizado y cambios subidos a la rama '$BRANCH_NAME' en el repositorio."
