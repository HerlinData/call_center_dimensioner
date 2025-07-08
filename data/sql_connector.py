"""
Conector SQL Server para Call Center Dimensioner
"""

import pandas as pd
import logging
from sqlalchemy import create_engine, text
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLConnector:
    """Conector para base de datos SQL Server"""
    
    def __init__(self):
        # Configuración desde variables de entorno
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_DATABASE')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.table_name = os.getenv('DB_TABLE_NAME', 'default_table')
        self.trusted_connection = os.getenv('DB_TRUSTED_CONNECTION', 'true').lower() == 'true'
        self.connection_timeout = int(os.getenv('DB_CONNECTION_TIMEOUT', '30'))
        self.command_timeout = int(os.getenv('DB_COMMAND_TIMEOUT', '60'))
        self.max_records = int(os.getenv('MAX_RECORDS_PER_QUERY', '50000'))
        
        # Validar configuración requerida
        if not self.server or not self.database:
            raise ValueError("DB_SERVER, DB_DATABASE son requeridos en variables de entorno")
        
        self.engine = None
        
        # Mapeo de columnas: nombre_real -> nombre_estandar
        self.column_mapping = {
            'usuarios': 'asesor',
            'fecha_hora': 'hora_inicio_contrata', 
            'fecha': 'fecha',
            'tmo': 'tmo',
            'tme': 'tme'
        }
        
        self.required_columns = ['fecha', 'asesor', 'hora_inicio_contrata', 'tme', 'tmo']
        
    def connect(self):
        """Establecer conexión con la base de datos"""
        try:
            # String de conexión basado en configuración
            if self.trusted_connection:
                conn_str = (
                    f"mssql+pyodbc://@{self.server}/{self.database}"
                    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
                )
            else:
                conn_str = (
                    f"mssql+pyodbc://{self.username}:{self.password}@{self.server}"
                    f"/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
                )
            
            logger.info(f"🔗 Conectando a: {self.server}/{self.database}")
            
            self.engine = create_engine(
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
            
            # Test de conexión
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                logger.info(f"✅ Conexión a {self.database} establecida correctamente")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando a SQL Server: {e}")
            logger.error(f"🔗 Servidor: {self.server}, Base de datos: {self.database}")
            logger.error("💡 Verifica:")
            logger.error(f"   - Servidor: {self.server}")
            logger.error(f"   - Base de datos: {self.database}")
            logger.error("   - Permisos de acceso")
            logger.error("   - ODBC Driver 17 instalado")
            return False
    
    def test_table_access(self) -> bool:
        """Verificar acceso a la tabla y columnas"""
        try:
            if not self.engine:
                if not self.connect():
                    return False
            
            # Query de prueba con mapeo de columnas (usando text() para consultas parametrizadas)
            query = text("""
            SELECT TOP 3
                usuarios as asesor,
                fecha_hora as hora_inicio_contrata,
                fecha as fecha,
                tmo as tmo,
                tme as tme
            FROM [{database}].[dbo].[{table_name}]
            """.format(database=self.database, table_name=self.table_name))
            
            logger.info(f"🔍 Probando acceso a tabla: {self.table_name}")
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn)
                
            logger.info(f"✅ Tabla {self.table_name} accesible")
            logger.info(f"📊 Columnas mapeadas: {list(result.columns)}")
            logger.info(f"📈 Registros de muestra: {len(result)}")
            
            # Mostrar muestra de datos
            if len(result) > 0:
                logger.info("📋 Muestra de datos:")
                for idx, row in result.iterrows():
                    logger.info(f"   {row['fecha']} | {row['asesor']} | TMO: {row['tmo']}s | TME: {row['tme']}s")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error accediendo a tabla {self.table_name}: {e}")
            logger.error("💡 Verifica que las columnas existan en la tabla:")
            logger.error("   - usuarios, fecha_hora, fecha, tmo, tme")
            return False
    
    def get_campaign_data(self, 
                         start_date: date, 
                         end_date: date,
                         campaign_filter: Optional[str] = None) -> pd.DataFrame:
        """
        Obtener datos de campaña con las 5 columnas requeridas
        
        Args:
            start_date: Fecha inicio
            end_date: Fecha fin  
            campaign_filter: Filtro adicional (opcional)
        
        Returns:
            DataFrame con las 5 columnas: fecha, asesor, hora_inicio_contrata, tme, tmo
        """
        try:
            if not self.engine:
                if not self.connect():
                    raise ConnectionError("No se pudo establecer conexión")
            
            # Validar filtro de campaña si se especifica
            if campaign_filter:
                # Validar que el filtro no contenga caracteres peligrosos
                if any(char in campaign_filter for char in [';', '--', '/*', '*/', 'xp_', 'sp_']):
                    raise ValueError("Filtro de campaña contiene caracteres no permitidos")
            
            # Construir query con TOP si hay límite de registros
            if self.max_records:
                top_clause = f"TOP {self.max_records} "
            else:
                top_clause = ""
            
            # Query con mapeo de columnas usando parámetros seguros
            base_query = f"""
            SELECT {top_clause}
                usuarios as asesor,
                fecha_hora as hora_inicio_contrata,
                fecha as fecha,
                tme as tme,
                tmo as tmo
            FROM [{self.database}].[dbo].[{self.table_name}]
            WHERE fecha >= :start_date
            AND fecha <= :end_date
            """.format(database=self.database, table_name=self.table_name)
            
            # Agregar filtro de campaña si se especifica
            if campaign_filter:
                base_query += f" AND {campaign_filter}"
            
            # Agregar ORDER BY al final
            base_query += " ORDER BY fecha, fecha_hora"
            
            query = text(base_query)
            
            logger.info(f"🔍 Ejecutando query para rango: {start_date} - {end_date}")
            logger.debug(f"Query: {query}")
            
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params={
                    'start_date': start_date,
                    'end_date': end_date
                })
            
            logger.info(f"📊 Datos obtenidos: {len(df)} registros")
            
            # Validaciones básicas
            if len(df) == 0:
                logger.warning("⚠️ No se encontraron datos para el rango especificado")
                return df
            
            # Verificar tipos de datos
            self._validate_data_types(df)
            
            # Mostrar estadísticas básicas
            self._show_data_stats(df)
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos: {e}")
            raise
    
    def get_available_date_range(self) -> Dict[str, Any]:
        """Obtener rango de fechas disponibles en la tabla"""
        try:
            if not self.engine:
                if not self.connect():
                    raise ConnectionError("No se pudo establecer conexión")
            
            query = text("""
            SELECT 
                MIN(fecha) as fecha_min,
                MAX(fecha) as fecha_max,
                COUNT(*) as total_registros,
                COUNT(DISTINCT usuarios) as total_asesores
            FROM [{database}].[dbo].[{table_name}]
            """.format(database=self.database, table_name=self.table_name))
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn)
            
            return {
                'fecha_min': result.iloc[0]['fecha_min'],
                'fecha_max': result.iloc[0]['fecha_max'], 
                'total_registros': result.iloc[0]['total_registros'],
                'total_asesores': result.iloc[0]['total_asesores']
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo rango de fechas: {e}")
            raise
    
    def get_sample_data(self, limit: int = 10) -> pd.DataFrame:
        """Obtener datos de muestra para testing"""
        try:
            if not self.engine:
                if not self.connect():
                    raise ConnectionError("No se pudo establecer conexión")
            
            # Validar límite para evitar consultas excesivas
            if limit > 1000:
                limit = 1000
                logger.warning("Límite reducido a 1000 registros por seguridad")
            
            query = text("""
            SELECT TOP :limit
                usuarios as asesor,
                fecha_hora as hora_inicio_contrata,
                fecha as fecha,
                tme as tme,
                tmo as tmo
            FROM [{database}].[dbo].[{table_name}]
            ORDER BY fecha DESC, fecha_hora DESC
            """.format(database=self.database, table_name=self.table_name))
            
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params={'limit': limit})
            
            logger.info(f"📊 Muestra obtenida: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo muestra: {e}")
            raise
    
    def get_campaign_summary(self, days_back: int = 30) -> Dict[str, Any]:
        """Obtener resumen de campaña de los últimos N días"""
        try:
            if not self.engine:
                if not self.connect():
                    raise ConnectionError("No se pudo establecer conexión")
            
            # Validar días para evitar consultas excesivas
            if days_back > 365:
                days_back = 365
                logger.warning("Días reducidos a 365 por seguridad")
            
            query = text("""
            SELECT 
                COUNT(*) as total_llamadas,
                COUNT(DISTINCT usuarios) as asesores_activos,
                AVG(CAST(tmo as FLOAT)) as tmo_promedio,
                AVG(CAST(tme as FLOAT)) as tme_promedio,
                MIN(fecha) as fecha_min,
                MAX(fecha) as fecha_max
            FROM [{database}].[dbo].[{table_name}]
            WHERE fecha >= DATEADD(day, :days_back, GETDATE())
            """.format(database=self.database, table_name=self.table_name))
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn, params={'days_back': -days_back})
            
            if len(result) > 0:
                return {
                    'total_llamadas': int(result.iloc[0]['total_llamadas']),
                    'asesores_activos': int(result.iloc[0]['asesores_activos']),
                    'tmo_promedio': float(result.iloc[0]['tmo_promedio']) if result.iloc[0]['tmo_promedio'] else 0,
                    'tme_promedio': float(result.iloc[0]['tme_promedio']) if result.iloc[0]['tme_promedio'] else 0,
                    'fecha_min': result.iloc[0]['fecha_min'],
                    'fecha_max': result.iloc[0]['fecha_max']
                }
            return {}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo resumen: {e}")
            raise
    
    def _validate_data_types(self, df: pd.DataFrame):
        """Validar tipos de datos de las columnas"""
        try:
            # Convertir fecha si no es datetime
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'])
            
            # Convertir hora_inicio_contrata si no es datetime
            if 'hora_inicio_contrata' in df.columns:
                df['hora_inicio_contrata'] = pd.to_datetime(df['hora_inicio_contrata'])
            
            # Verificar que tme y tmo sean numéricos
            for col in ['tme', 'tmo']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            logger.debug("✅ Validación de tipos de datos completada")
            
        except Exception as e:
            logger.warning(f"⚠️ Error en validación de tipos: {e}")
    
    def _show_data_stats(self, df: pd.DataFrame):
        """Mostrar estadísticas básicas de los datos"""
        try:
            logger.info("📊 Estadísticas de datos:")
            logger.info(f"   📅 Rango fechas: {df['fecha'].min()} - {df['fecha'].max()}")
            logger.info(f"   👥 Asesores únicos: {df['asesor'].nunique()}")
            logger.info(f"   ⏱️ TMO promedio: {df['tmo'].mean():.1f}s")
            logger.info(f"   ⏳ TME promedio: {df['tme'].mean():.1f}s")
            
        except Exception as e:
            logger.debug(f"Error mostrando estadísticas: {e}")
    
    def close(self):
        """Cerrar conexión"""
        if self.engine:
            self.engine.dispose()
            logger.info("🔒 Conexión cerrada")

# Instancia global
sql_connector = SQLConnector()

def test_connection():
    """Función de testing"""
    logger.info("🧪 Iniciando test de conexión a SQL Server...")
    logger.info(f"🎯 Objetivo: {sql_connector.server}/{sql_connector.database}")
    
    # Test 1: Conexión básica
    if not sql_connector.connect():
        logger.error("❌ Test fallido: No se pudo conectar")
        return False
    
    # Test 2: Acceso a tabla
    if not sql_connector.test_table_access():
        logger.error("❌ Test fallido: No se pudo acceder a la tabla")
        return False
    
    # Test 3: Obtener rango de fechas
    try:
        date_range = sql_connector.get_available_date_range()
        logger.info(f"📅 Rango disponible: {date_range['fecha_min']} - {date_range['fecha_max']}")
        logger.info(f"📊 Total registros: {date_range['total_registros']:,}")
        logger.info(f"👥 Total asesores: {date_range['total_asesores']}")
    except Exception as e:
        logger.error(f"❌ Test fallido obteniendo rango: {e}")
        return False
    
    # Test 4: Resumen de campaña
    try:
        summary = sql_connector.get_campaign_summary(7)  # Últimos 7 días
        logger.info("📈 Resumen últimos 7 días:")
        logger.info(f"   📞 Llamadas: {summary.get('total_llamadas', 0):,}")
        logger.info(f"   👥 Asesores: {summary.get('asesores_activos', 0)}")
        logger.info(f"   ⏱️ TMO: {summary.get('tmo_promedio', 0):.1f}s")
        logger.info(f"   ⏳ TME: {summary.get('tme_promedio', 0):.1f}s")
    except Exception as e:
        logger.error(f"❌ Test fallido obteniendo resumen: {e}")
        return False
    
    logger.info("✅ Todos los tests pasaron correctamente")
    logger.info("🚀 Conector SQL Server listo para usar")
    return True

if __name__ == "__main__":
    # Ejecutar tests
    test_connection()