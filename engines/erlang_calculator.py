"""
Motor de Cálculo Erlang C para Call Center Dimensioner
"""

import math
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configurar logging para este módulo
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ErlangInputs:
    """Parámetros de entrada para Erlang C"""
    calls_per_hour: float          # Llamadas por hora
    average_handle_time: float     # TMO promedio en segundos
    service_level_target: float    # Objetivo de nivel de servicio (0.90 = 90%)
    answer_time_target: int        # Tiempo de respuesta objetivo en segundos
    shrinkage_percentage: float = 15.0  # Shrinkage por defecto

@dataclass 
class ErlangResults:
    """Resultados del cálculo Erlang C"""
    agents_required: int           # Agentes necesarios
    utilization: float            # Utilización de agentes
    service_level: float          # Nivel de servicio logrado
    average_wait_time: float      # Tiempo promedio de espera
    probability_of_wait: float    # Probabilidad de esperar
    agents_with_shrinkage: int    # Agentes considerando shrinkage
    traffic_intensity: float      # Intensidad de tráfico (Erlangs)
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario para fácil acceso"""
        return {
            'agents_required': self.agents_required,
            'utilization': round(self.utilization * 100, 2),
            'service_level': round(self.service_level * 100, 2),
            'average_wait_time': round(self.average_wait_time, 2),
            'probability_of_wait': round(self.probability_of_wait * 100, 2),
            'agents_with_shrinkage': self.agents_with_shrinkage,
            'traffic_intensity': round(self.traffic_intensity, 3)
        }

class ErlangCalculator:
    """Calculadora Erlang C para dimensionamiento de call center"""
    
    def __init__(self):
        self.max_iterations = 1000  # Límite para iteraciones numéricas
        self.precision = 0.0001     # Precisión para convergencia
    
    def calculate_erlang_c(self, inputs: ErlangInputs) -> ErlangResults:
        """
        Calcular dimensionamiento usando fórmula Erlang C
        
        Args:
            inputs: Parámetros de entrada
            
        Returns:
            ErlangResults: Resultados del cálculo
        """
        try:
            print(f"🧮 Calculando Erlang C...")
            print(f"   📞 Llamadas/hora: {inputs.calls_per_hour}")
            print(f"   ⏱️ TMO: {inputs.average_handle_time}s")
            print(f"   🎯 SLA: {inputs.service_level_target*100}% en {inputs.answer_time_target}s")
            
            logger.info(f"🧮 Calculando Erlang C...")
            logger.info(f"   📞 Llamadas/hora: {inputs.calls_per_hour}")
            logger.info(f"   ⏱️ TMO: {inputs.average_handle_time}s")
            logger.info(f"   🎯 SLA: {inputs.service_level_target*100}% en {inputs.answer_time_target}s")
            
            # 1. Calcular intensidad de tráfico (Erlangs)
            traffic_intensity = self._calculate_traffic_intensity(
                inputs.calls_per_hour, 
                inputs.average_handle_time
            )
            print(f"📊 Intensidad de tráfico: {traffic_intensity:.3f} Erlangs")
            
            # 2. Encontrar número mínimo de agentes
            agents_required = self._find_minimum_agents(
                traffic_intensity,
                inputs.service_level_target,
                inputs.answer_time_target
            )
            print(f"👥 Agentes base calculados: {agents_required}")
            
            # 3. Calcular métricas finales
            utilization = traffic_intensity / agents_required
            probability_of_wait = self._calculate_erlang_c_probability(traffic_intensity, agents_required)
            average_wait_time = self._calculate_average_wait_time(
                probability_of_wait, 
                traffic_intensity, 
                agents_required, 
                inputs.average_handle_time
            )
            service_level = self._calculate_service_level(
                probability_of_wait,
                traffic_intensity,
                agents_required,
                inputs.average_handle_time,
                inputs.answer_time_target
            )
            
            # 4. Aplicar shrinkage
            agents_with_shrinkage = self._apply_shrinkage(agents_required, inputs.shrinkage_percentage)
            
            results = ErlangResults(
                agents_required=agents_required,
                utilization=utilization,
                service_level=service_level,
                average_wait_time=average_wait_time,
                probability_of_wait=probability_of_wait,
                agents_with_shrinkage=agents_with_shrinkage,
                traffic_intensity=traffic_intensity
            )
            
            self._log_results(results)
            return results
            
        except Exception as e:
            print(f"❌ Error en cálculo Erlang C: {e}")
            logger.error(f"❌ Error en cálculo Erlang C: {e}")
            raise
    
    def _calculate_traffic_intensity(self, calls_per_hour: float, aht_seconds: float) -> float:
        """Calcular intensidad de tráfico en Erlangs"""
        # Intensidad = (Llamadas/hora * TMO en horas)
        aht_hours = aht_seconds / 3600
        traffic_intensity = calls_per_hour * aht_hours
        logger.debug(f"📊 Intensidad de tráfico: {traffic_intensity:.3f} Erlangs")
        return traffic_intensity
    
    def _find_minimum_agents(self, traffic_intensity: float, sla_target: float, answer_time: int) -> int:
        """Encontrar número mínimo de agentes para cumplir SLA"""
        # Empezar con el mínimo teórico (intensidad de tráfico redondeada hacia arriba)
        min_agents = max(1, math.ceil(traffic_intensity))
        
        for agents in range(min_agents, min_agents + 50):  # Buscar en rango razonable
            prob_wait = self._calculate_erlang_c_probability(traffic_intensity, agents)
            service_level = self._calculate_service_level(
                prob_wait, traffic_intensity, agents, answer_time * 3, answer_time
            )
            
            if service_level >= sla_target:
                logger.debug(f"🎯 Agentes encontrados: {agents} (SL: {service_level*100:.1f}%)")
                return agents
        
        logger.warning(f"⚠️ No se pudo encontrar solución óptima, usando {min_agents + 49}")
        return min_agents + 49
    
    def _calculate_erlang_c_probability(self, traffic_intensity: float, agents: int) -> float:
        """Calcular probabilidad Erlang C (probabilidad de esperar)"""
        try:
            # Fórmula Erlang C: P(W>0) = (A^N / N!) * (N / (N - A)) / sum(A^k / k!) + (A^N / N!) * (N / (N - A))
            if agents <= traffic_intensity:
                return 1.0  # Sobrecarga del sistema
            
            # Calcular suma del denominador
            sum_denominator = 0
            for k in range(agents):
                sum_denominator += (traffic_intensity ** k) / math.factorial(k)
            
            # Calcular término Erlang C
            erlang_c_numerator = (traffic_intensity ** agents) / math.factorial(agents)
            erlang_c_denominator = agents - traffic_intensity
            erlang_c_term = erlang_c_numerator / erlang_c_denominator
            
            # Probabilidad final
            probability = erlang_c_term / (sum_denominator + erlang_c_term)
            
            return min(1.0, max(0.0, probability))  # Asegurar rango [0,1]
            
        except (OverflowError, ZeroDivisionError):
            logger.warning(f"⚠️ Error numérico en Erlang C, usando aproximación")
            return self._erlang_c_approximation(traffic_intensity, agents)
    
    def _erlang_c_approximation(self, traffic_intensity: float, agents: int) -> float:
        """Aproximación numérica para evitar overflow en factorial"""
        try:
            # Usar logaritmos para evitar overflow
            log_prob = agents * math.log(traffic_intensity) - math.lgamma(agents + 1)
            log_prob += math.log(agents) - math.log(agents - traffic_intensity)
            
            # Aproximación del denominador
            max_k = min(agents - 1, int(traffic_intensity + 10))
            log_sum = 0
            
            for k in range(max_k + 1):
                log_term = k * math.log(traffic_intensity) - math.lgamma(k + 1)
                if k == 0:
                    log_sum = log_term
                else:
                    log_sum = log_sum + math.log(1 + math.exp(log_term - log_sum))
            
            log_final_prob = log_prob - math.log(math.exp(log_sum) + math.exp(log_prob))
            
            return min(1.0, max(0.0, math.exp(log_final_prob)))
            
        except:
            # Última aproximación simple
            rho = traffic_intensity / agents
            if rho >= 1:
                return 1.0
            return rho ** agents
    
    def _calculate_average_wait_time(self, prob_wait: float, traffic_intensity: float, 
                                   agents: int, aht_seconds: float) -> float:
        """Calcular tiempo promedio de espera"""
        if agents <= traffic_intensity:
            return float('inf')  # Sistema sobrecargado
        
        # Tiempo promedio de espera = P(W>0) * AHT / (N - A)
        avg_wait = prob_wait * aht_seconds / (agents - traffic_intensity)
        return max(0, avg_wait)
    
    def _calculate_service_level(self, prob_wait: float, traffic_intensity: float,
                               agents: int, aht_seconds: float, target_time: int) -> float:
        """Calcular nivel de servicio (% atendidas en tiempo objetivo)"""
        if agents <= traffic_intensity:
            return 0.0  # Sistema sobrecargado
        
        # SL = 1 - P(W>0) * exp(-(N-A) * T / AHT)
        # Donde T es el tiempo objetivo y AHT es el tiempo promedio de servicio
        exponent = -(agents - traffic_intensity) * target_time / aht_seconds
        service_level = 1 - prob_wait * math.exp(exponent)
        
        return min(1.0, max(0.0, service_level))
    
    def _apply_shrinkage(self, base_agents: int, shrinkage_pct: float) -> int:
        """Aplicar shrinkage al número de agentes"""
        shrinkage_factor = 1 + (shrinkage_pct / 100)
        agents_with_shrinkage = math.ceil(base_agents * shrinkage_factor)
        
        logger.debug(f"👥 Agentes base: {base_agents}, con shrinkage {shrinkage_pct}%: {agents_with_shrinkage}")
        return agents_with_shrinkage
    
    def _log_results(self, results: ErlangResults):
        """Log de resultados para debugging"""
        print("📊 Resultados Erlang C:")
        print(f"   👥 Agentes requeridos: {results.agents_required}")
        print(f"   👥 Con shrinkage: {results.agents_with_shrinkage}")
        print(f"   📈 Utilización: {results.utilization*100:.1f}%")
        print(f"   🎯 Nivel de servicio: {results.service_level*100:.1f}%")
        print(f"   ⏱️ Tiempo promedio espera: {results.average_wait_time:.1f}s")
        print(f"   📊 Probabilidad esperar: {results.probability_of_wait*100:.1f}%")
        
        logger.info("📊 Resultados Erlang C:")
        logger.info(f"   👥 Agentes requeridos: {results.agents_required}")
        logger.info(f"   👥 Con shrinkage: {results.agents_with_shrinkage}")
        logger.info(f"   📈 Utilización: {results.utilization*100:.1f}%")
        logger.info(f"   🎯 Nivel de servicio: {results.service_level*100:.1f}%")
        logger.info(f"   ⏱️ Tiempo promedio espera: {results.average_wait_time:.1f}s")
        logger.info(f"   📊 Probabilidad esperar: {results.probability_of_wait*100:.1f}%")
    
    def analyze_historical_data(self, df: pd.DataFrame) -> Dict:
        """
        Analizar datos históricos para obtener parámetros Erlang C
        
        Args:
            df: DataFrame con columnas ['fecha', 'asesor', 'hora_inicio_contrata', 'tme', 'tmo']
            
        Returns:
            Dict con análisis de volumen, TMO, etc.
        """
        try:
            logger.info("📊 Analizando datos históricos...")
            
            # Convertir timestamps
            df['hora_inicio_contrata'] = pd.to_datetime(df['hora_inicio_contrata'])
            df['hora'] = df['hora_inicio_contrata'].dt.hour
            
            # Análisis de volumen por hora
            volume_by_hour = df.groupby('hora').size()
            avg_calls_per_hour = volume_by_hour.mean()
            peak_hour = volume_by_hour.idxmax()
            peak_volume = volume_by_hour.max()
            
            # Análisis de TMO
            avg_tmo = df['tmo'].mean()
            std_tmo = df['tmo'].std()
            
            # Análisis de TME (para validación posterior)
            avg_tme = df['tme'].mean()
            
            # Agentes únicos por día
            agents_per_day = df.groupby('fecha')['asesor'].nunique()
            avg_agents = agents_per_day.mean()
            
            # Calcular días en el análisis PRIMERO
            date_range_days = (df['fecha'].max() - df['fecha'].min()).days + 1
            
            # Crear diccionario DESPUÉS
            analysis = {
                'total_calls': len(df),
                'date_range': {
                    'start': df['fecha'].min(),
                    'end': df['fecha'].max(),
                    'days': date_range_days
                },
                'volume_analysis': {
                    'avg_calls_per_hour': round(avg_calls_per_hour, 1),
                    'peak_hour': int(peak_hour),
                    'peak_volume': int(peak_volume),
                    'hourly_profile': volume_by_hour.to_dict()
                },
                'tmo_analysis': {
                    'average_seconds': round(avg_tmo, 1),
                    'std_deviation': round(std_tmo, 1),
                    'percentiles': {
                        '50': round(df['tmo'].quantile(0.5), 1),
                        '90': round(df['tmo'].quantile(0.9), 1),
                        '95': round(df['tmo'].quantile(0.95), 1)
                    }
                },
                'tme_analysis': {
                    'average_seconds': round(avg_tme, 1),
                    'percentiles': {
                        '50': round(df['tme'].quantile(0.5), 1),
                        '90': round(df['tme'].quantile(0.9), 1),
                        '95': round(df['tme'].quantile(0.95), 1)
                    }
                },
                'resource_analysis': {
                    'avg_agents_per_day': round(avg_agents, 1),
                    'unique_agents': df['asesor'].nunique(),
                    'calls_per_agent_per_day': round(len(df) / (avg_agents * date_range_days), 1)
                }
            }
            
            self._log_historical_analysis(analysis)
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analizando datos históricos: {e}")
            print(f"❌ Error analizando datos históricos: {e}")
            # Retornar análisis básico en caso de error
            return {
                'total_calls': len(df) if 'df' in locals() else 0,
                'date_range': {'start': None, 'end': None, 'days': 0},
                'volume_analysis': {'avg_calls_per_hour': 0, 'peak_hour': 0, 'peak_volume': 0, 'hourly_profile': {}},
                'tmo_analysis': {'average_seconds': 0, 'std_deviation': 0, 'percentiles': {'50': 0, '90': 0, '95': 0}},
                'tme_analysis': {'average_seconds': 0, 'percentiles': {'50': 0, '90': 0, '95': 0}},
                'resource_analysis': {'avg_agents_per_day': 0, 'unique_agents': 0, 'calls_per_agent_per_day': 0}
            }
    
    def _log_historical_analysis(self, analysis: Dict):
        """Log del análisis histórico"""
        logger.info("📈 Análisis de datos históricos:")
        logger.info(f"   📅 Período: {analysis['date_range']['start']} - {analysis['date_range']['end']}")
        logger.info(f"   📞 Total llamadas: {analysis['total_calls']:,}")
        logger.info(f"   📊 Promedio llamadas/hora: {analysis['volume_analysis']['avg_calls_per_hour']}")
        logger.info(f"   🕐 Hora pico: {analysis['volume_analysis']['peak_hour']}h ({analysis['volume_analysis']['peak_volume']} llamadas)")
        logger.info(f"   ⏱️ TMO promedio: {analysis['tmo_analysis']['average_seconds']}s")
        logger.info(f"   ⏳ TME promedio: {analysis['tme_analysis']['average_seconds']}s")
        logger.info(f"   👥 Agentes promedio/día: {analysis['resource_analysis']['avg_agents_per_day']}")

# Instancia global
erlang_calculator = ErlangCalculator()

def test_erlang_calculator():
    """Función de testing del calculador Erlang C"""
    print("🧪 Iniciando test de Erlang Calculator...")
    logger.info("🧪 Iniciando test de Erlang Calculator...")
    
    # Test con datos de ejemplo
    inputs = ErlangInputs(
        calls_per_hour=450,          # 450 llamadas por hora
        average_handle_time=240,     # 4 minutos TMO
        service_level_target=0.90,   # 90% SLA
        answer_time_target=20,       # 20 segundos
        shrinkage_percentage=15.0    # 15% shrinkage
    )
    
    print(f"📊 Inputs de prueba:")
    print(f"   📞 Llamadas/hora: {inputs.calls_per_hour}")
    print(f"   ⏱️ TMO: {inputs.average_handle_time}s")
    print(f"   🎯 SLA: {inputs.service_level_target*100}%")
    
    try:
        results = erlang_calculator.calculate_erlang_c(inputs)
        
        print("✅ Test completado exitosamente")
        print("📋 Resultados del test:")
        results_dict = results.to_dict()
        for key, value in results_dict.items():
            print(f"   {key}: {value}")
        
        logger.info("✅ Test completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Test fallido: {e}")
        logger.error(f"❌ Test fallido: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar test
    test_erlang_calculator()