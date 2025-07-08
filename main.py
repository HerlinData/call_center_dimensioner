"""
Punto de entrada principal del sistema
"""

import sys
import os
import logging
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Función principal"""
    try:
        logger.info("Iniciando Call Center Dimensioner...")
        
        # Verificar dependencias
        check_dependencies()
        
        # Crear directorios necesarios
        create_directories()
        
        # Inicializar aplicación
        logger.info("Sistema iniciado correctamente")
        
    except Exception as e:
        logger.error(f"Error iniciando la aplicación: {e}")
        sys.exit(1)

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'sqlalchemy', 
        'pyodbc', 'simpy', 'scipy', 'plotly', 'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Paquetes faltantes: {missing_packages}")
        logger.error("Ejecuta: pip install -r requirements.txt")
        raise ImportError(f"Paquetes faltantes: {missing_packages}")

def create_directories():
    """Crear directorios necesarios"""
    directories = [
        'logs',
        'reports/output',
        'tests/data',
        'docs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio creado/verificado: {directory}")

if __name__ == "__main__":
    main()