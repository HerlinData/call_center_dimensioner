"""
Script para ejecutar la aplicación Streamlit
"""

import subprocess
import sys
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

def run_streamlit_app():
    """Ejecutar la aplicación Streamlit"""
    try:
        # Verificar que el archivo de la app existe
        app_file = Path("ui/streamlit_app.py")
        if not app_file.exists():
            raise FileNotFoundError(f"Archivo de aplicación no encontrado: {app_file}")
        
        # Configuración de Streamlit desde variables de entorno
        port = os.getenv('APP_PORT', '8501')
        host = os.getenv('APP_HOST', 'localhost')
        primary_color = os.getenv('THEME_PRIMARY_COLOR', '#da7756')
        bg_color = os.getenv('THEME_BACKGROUND_COLOR', '#ffffff')
        secondary_bg = os.getenv('THEME_SECONDARY_BACKGROUND_COLOR', '#f0f2f6')
        text_color = os.getenv('THEME_TEXT_COLOR', '#262730')
        
        config_args = [
            f"--server.port={port}",
            f"--server.address={host}",
            f"--theme.primaryColor={primary_color}",
            f"--theme.backgroundColor={bg_color}",
            f"--theme.secondaryBackgroundColor={secondary_bg}",
            f"--theme.textColor={text_color}"
        ]
        
        # Comando para ejecutar Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_file)
        ] + config_args
        
        logger.info("Iniciando aplicación Streamlit...")
        logger.info(f"Comando: {' '.join(cmd)}")
        
        # Ejecutar la aplicación
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error ejecutando Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_streamlit_app()