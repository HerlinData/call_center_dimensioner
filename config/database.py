"""
Configuración de conexión a SQL Server
"""

import os
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    
    server: str = ""
    database: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    driver: str = "ODBC Driver 17 for SQL Server"
    trusted_connection: bool = True
    connection_timeout: int = 30
    command_timeout: int = 60
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Cargar configuración desde variables de entorno"""
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_DATABASE')
        
        if not server or not database:
            raise ValueError("DB_SERVER y DB_DATABASE son requeridos en las variables de entorno")
        
        return cls(
            server=server,
            database=database,
            username=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            trusted_connection=os.getenv('DB_TRUSTED_CONNECTION', 'true').lower() == 'true',
            connection_timeout=int(os.getenv('DB_CONNECTION_TIMEOUT', '30')),
            command_timeout=int(os.getenv('DB_COMMAND_TIMEOUT', '60'))
        )
    
    def get_connection_string(self) -> str:
        """Generar string de conexión"""
        if self.trusted_connection:
            conn_str = (
                f"mssql+pyodbc://@{self.server}/{self.database}"
                f"?driver={self.driver.replace(' ', '+')}&trusted_connection=yes"
            )
        else:
            conn_str = (
                f"mssql+pyodbc://{self.username}:{self.password}@{self.server}"
                f"/{self.database}?driver={self.driver.replace(' ', '+')}"
            )
        return conn_str
    
    def create_engine(self) -> Engine:
        """Crear engine de SQLAlchemy"""
        try:
            conn_str = self.get_connection_string()
            logger.info(f"🔗 Intentando conectar a: {self.server}/{self.database}")
            
            engine = create_engine(
                conn_str,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_size=int(os.getenv('CONNECTION_POOL_SIZE', '5')),
                max_overflow=int(os.getenv('CONNECTION_POOL_SIZE', '5')),
                connect_args={
                    'timeout': self.connection_timeout,
                    'command_timeout': self.command_timeout
                }
            )
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Conexión a base de datos establecida correctamente")
            return engine
        except Exception as e:
            logger.error(f"❌ Error conectando a base de datos: {e}")
            # No mostrar la cadena de conexión completa por seguridad
            logger.error(f"🔗 Servidor: {self.server}, Base de datos: {self.database}")
            raise

# Instancia global
db_config = DatabaseConfig.from_env()