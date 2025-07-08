"""
Configuraciones generales del sistema
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AppSettings:
    """Configuraciones principales de la aplicación"""
    
    # Autenticación
    ACCESS_KEY: str = ""
    SESSION_TIMEOUT_HOURS: int = 8
    
    # Simulación
    SIMULATION_HOURS: int = 24
    WARMUP_HOURS: int = 2
    NUM_REPLICATIONS: int = 10
    RANDOM_SEED: int = 42
    
    # Análisis
    DEFAULT_SLA_TARGET: float = 90.0
    DEFAULT_ANSWER_TIME_SECONDS: int = 20
    DEFAULT_SHRINKAGE_PERCENTAGE: float = 15.0
    MIN_START_TIME: str = "11:45"
    MAX_END_TIME: str = "14:30"
    
    # Intervalos de análisis
    INTERVAL_OPTIONS: list = None
    
    def __post_init__(self):
        if self.INTERVAL_OPTIONS is None:
            self.INTERVAL_OPTIONS = [15, 30, 60]  # minutos
    
    @classmethod
    def from_env(cls) -> 'AppSettings':
        """Cargar configuraciones desde variables de entorno"""
        access_key = os.getenv('ACCESS_KEY')
        if not access_key:
            raise ValueError("ACCESS_KEY es requerido en las variables de entorno")
        
        return cls(
            ACCESS_KEY=access_key,
            SESSION_TIMEOUT_HOURS=int(os.getenv('SESSION_TIMEOUT_HOURS', cls.SESSION_TIMEOUT_HOURS)),
            SIMULATION_HOURS=int(os.getenv('SIMULATION_HOURS', cls.SIMULATION_HOURS)),
            WARMUP_HOURS=int(os.getenv('WARMUP_HOURS', cls.WARMUP_HOURS)),
            NUM_REPLICATIONS=int(os.getenv('NUM_REPLICATIONS', cls.NUM_REPLICATIONS)),
            RANDOM_SEED=int(os.getenv('RANDOM_SEED', cls.RANDOM_SEED)),
            DEFAULT_SLA_TARGET=float(os.getenv('DEFAULT_SLA_TARGET', cls.DEFAULT_SLA_TARGET)),
            DEFAULT_ANSWER_TIME_SECONDS=int(os.getenv('DEFAULT_ANSWER_TIME', cls.DEFAULT_ANSWER_TIME_SECONDS)),
            DEFAULT_SHRINKAGE_PERCENTAGE=float(os.getenv('DEFAULT_SHRINKAGE_PCT', cls.DEFAULT_SHRINKAGE_PERCENTAGE)),
        )

# Instancia global
settings = AppSettings.from_env()