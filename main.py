"""
Call Center Dimensioner - Aplicación Flet
Sistema de dimensionamiento para call centers con interfaz moderna
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Punto de entrada principal - redirige a Flet"""
    print("🏢 Call Center Dimensioner")
    print("🚀 Iniciando aplicación Flet...")
    print("=" * 40)
    
    try:
        # Ejecutar la aplicación Flet
        subprocess.run([sys.executable, "main_flet.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error ejecutando la aplicación")
        print("💡 Intenta: python run_flet.py")
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")

if __name__ == "__main__":
    main()