#!/bin/bash
echo "🔧 Correction installation Docker pour Ubuntu 22.04"

# Étape 1: Corriger le problème GPG Google Cloud
echo "📋 Correction du repository Google Cloud..."
sudo mv /etc/apt/sources.list.d/google-cloud-sdk.list /etc/apt/sources.list.d/google-cloud-sdk.list.backup 2>/dev/null || true

# Étape 2: Nettoyer les tentatives précédentes
echo "🧹 Nettoyage..."
sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null || true

# Étape 3: Installation Docker manuelle
echo "📦 Installation Docker..."
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

# Ajouter clé GPG Docker
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Ajouter repository Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter utilisateur au groupe
sudo usermod -aG docker $USER

# Restaurer le repository Google Cloud avec la bonne clé
echo "�� Restauration repository Google Cloud..."
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

# Test final
echo "🔍 Test de l'installation..."
if sudo docker --version; then
    echo "✅ Docker installé avec succès !"
    echo "🎯 Commandes suivantes :"
    echo "   newgrp docker"
    echo "   docker --version"
    echo "   ./airflow_docker_fixed.sh start"
else
    echo "❌ Problème avec l'installation Docker"
fi
