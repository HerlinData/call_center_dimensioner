#!/usr/bin/env python3
"""
Archivo de inicio para la aplicación web Flet
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

import flet as ft
from main_flet import main

if __name__ == "__main__":
    print("🚀 Iniciando Call Center Dimensioner - Modo Web")
    print("📱 Abriendo en navegador...")
    print("🌐 URL: http://localhost:8502")
    print("🔑 Login con tu clave configurada en .env")
    print("\n" + "="*50)
    
    # Crear directorios necesarios
    Path("logs").mkdir(exist_ok=True)
    
    # Iniciar aplicación web
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8502,
        host="0.0.0.0"
    )