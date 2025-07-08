"""
Analizador de Datos Integrado - SQL Server + Erlang C
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import sys
from pathlib import Path

# Agregar paths
sys.path.append(str(Path(__file__).parent.parent))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

try:
    from data.sql_connector import sql_connector
    from engines.erlang_calculator import erlang_calculator, ErlangInputs, ErlangResults
except ImportError as e:
    logger.error(f"❌ Error importando módulos: {e}")
    print(f"❌ Error importando módulos: {e}")
    exit(1)

class DataAnalyzer:
    """Analizador integrado de datos históricos y dimensionamiento"""
    
    def __init__(self):
        self.sql_connector = sql_connector
        self.erlang_calculator = erlang_calculator
        
    def analyze_campaign_complete(self, 
                                 start_date: date, 
                                 end_date: date,
                                 sla_target: float = 0.90,
                                 answer_time_target: int = 20,
                                 shrinkage_pct: float = 15.0) -> Dict:
        """
        Análisis completo de campaña: datos históricos + dimensionamiento + validación
        
        Args:
            start_date: Fecha inicio análisis
            end_date: Fecha fin análisis
            sla_target: Objetivo SLA (0.90 = 90%)
            answer_time_target: Tiempo respuesta objetivo en segundos
            shrinkage_pct: Porcentaje de shrinkage
            
        Returns:
            Dict con análisis completo
        """
        try:
            print(f"🔍 Iniciando análisis completo de campaña...")
            print(f"📅 Período: {start_date} - {end_date}")
            print(f"🎯 SLA objetivo: {sla_target*100}% en {answer_time_target}s")
            
            # 1. Obtener datos históricos
            print("📊 1. Obteniendo datos históricos...")
            df = self.sql_connector.get_campaign_data(start_date, end_date)
            
            if len(df) == 0:
                raise ValueError("No se encontraron datos para el período especificado")
            
            # 2. Análisis de datos históricos
            print("📈 2. Analizando patrones históricos...")
            historical_analysis = self.erlang_calculator.analyze_historical_data(df)
            
            # 3. Análisis por intervalos (hora pico vs promedio)
            print("⏰ 3. Analizando por intervalos...")
            interval_analysis = self._analyze_by_intervals(df)
            
            # 4. Dimensionamiento con Erlang C
            print("🧮 4. Calculando dimensionamiento...")
            dimensioning_results = self._calculate_dimensioning_scenarios(
                historical_analysis, interval_analysis, sla_target, answer_time_target, shrinkage_pct
            )
            
            # 5. Validación contra TME real
            print("✅ 5. Validando contra datos reales...")
            validation_results = self._validate_against_reality(df, dimensioning_results)
            
            # 6. Recomendaciones
            print("💡 6. Generando recomendaciones...")
            recommendations = self._generate_recommendations(
                historical_analysis, dimensioning_results, validation_results
            )
            
            # 7. Compilar resultados finales
            complete_analysis = {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'days_analyzed': (end_date - start_date).days + 1
                },
                'targets': {
                    'sla_target': sla_target * 100,
                    'answer_time_target': answer_time_target,
                    'shrinkage_percentage': shrinkage_pct
                },
                'historical_analysis': historical_analysis,
                'interval_analysis': interval_analysis,
                'dimensioning_results': dimensioning_results,
                'validation_results': validation_results,
                'recommendations': recommendations,
                'summary': self._create_executive_summary(
                    historical_analysis, dimensioning_results, validation_results
                )
            }
            
            self._log_complete_results(complete_analysis)
            
            return complete_analysis
            
        except Exception as e:
            logger.error(f"❌ Error en análisis completo: {e}")
            print(f"❌ Error en análisis completo: {e}")
            raise
    
    def _analyze_by_intervals(self, df: pd.DataFrame) -> Dict:
        """Análisis detallado por intervalos de tiempo"""
        try:
            df['hora_inicio_contrata'] = pd.to_datetime(df['hora_inicio_contrata'])
            df['hora'] = df['hora_inicio_contrata'].dt.hour
            df['intervalo_15min'] = (df['hora_inicio_contrata'].dt.minute // 15) * 15
            
            # Análisis por hora - CORREGIDO: evitar duplicación de columnas
            hourly_stats = df.groupby('hora').agg({
                'asesor': ['count', 'nunique'],  # Llamadas y agentes únicos
                'tmo': ['mean', 'std'],
                'tme': ['mean', 'std']
            }).round(2)
            
            # Renombrar columnas con estructura jerárquica corregida
            hourly_stats.columns = ['llamadas', 'agentes_activos', 'tmo_promedio', 'tmo_std', 'tme_promedio', 'tme_std']
            
            # Encontrar hora pico
            peak_hour = hourly_stats['llamadas'].idxmax()
            peak_volume = hourly_stats.loc[peak_hour, 'llamadas']
            
            # Análisis por intervalos de 15 minutos (hora pico)
            peak_hour_data = df[df['hora'] == peak_hour]
            interval_15min = peak_hour_data.groupby('intervalo_15min').agg({
                'asesor': 'count',
                'tmo': 'mean',
                'tme': 'mean'
            }).round(2)
            
            # Capturar TMO de hora pico para usar en escenarios
            peak_hour_tmo = float(hourly_stats.loc[peak_hour, 'tmo_promedio'])
            
            return {
                'hourly_profile': hourly_stats.to_dict('index'),
                'peak_hour': {
                    'hour': int(peak_hour),
                    'volume': int(peak_volume),
                    'tmo_avg': peak_hour_tmo,  # TMO específico de hora pico
                    'tme_avg': float(hourly_stats.loc[peak_hour, 'tme_promedio']),
                    'agents_active': int(hourly_stats.loc[peak_hour, 'agentes_activos'])
                },
                'peak_hour_tmo': peak_hour_tmo,  # NUEVO: TMO específico para escenarios
                'interval_15min_peak': interval_15min.to_dict('index'),
                'busiest_intervals': {
                    'top_3_hours': hourly_stats.nlargest(3, 'llamadas')[['llamadas', 'tmo_promedio']].to_dict('index')
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en análisis por intervalos: {e}")
            return {}
    
    def _calculate_dimensioning_scenarios(self, historical_analysis: Dict, interval_analysis: Dict,
                                        sla_target: float, answer_time: int, 
                                        shrinkage_pct: float) -> Dict:
        """Calcular múltiples escenarios de dimensionamiento"""
        try:
            scenarios = {}
            
            # Escenario 1: Promedio histórico
            avg_volume = historical_analysis['volume_analysis']['avg_calls_per_hour']
            avg_tmo = historical_analysis['tmo_analysis']['average_seconds']
            
            inputs_avg = ErlangInputs(
                calls_per_hour=avg_volume,
                average_handle_time=avg_tmo,
                service_level_target=sla_target,
                answer_time_target=answer_time,
                shrinkage_percentage=shrinkage_pct
            )
            
            scenarios['promedio'] = self.erlang_calculator.calculate_erlang_c(inputs_avg)
            
            # Escenario 2: Hora pico - CORREGIDO: usar TMO específico de hora pico
            peak_volume = historical_analysis['volume_analysis']['peak_volume']
            # Obtener TMO de hora pico desde interval_analysis
            peak_tmo = interval_analysis.get('peak_hour_tmo', avg_tmo)  # Usar TMO específico de hora pico
            
            inputs_peak = ErlangInputs(
                calls_per_hour=peak_volume,
                average_handle_time=peak_tmo,  # TMO específico de hora pico
                service_level_target=sla_target,
                answer_time_target=answer_time,
                shrinkage_percentage=shrinkage_pct
            )
            
            scenarios['hora_pico'] = self.erlang_calculator.calculate_erlang_c(inputs_peak)
            
            # Escenario 3: Conservador (percentil 90 de volumen)
            hourly_volumes = list(historical_analysis['volume_analysis']['hourly_profile'].values())
            p90_volume = np.percentile(hourly_volumes, 90)
            
            inputs_conservative = ErlangInputs(
                calls_per_hour=p90_volume,
                average_handle_time=avg_tmo,
                service_level_target=sla_target,
                answer_time_target=answer_time,
                shrinkage_percentage=shrinkage_pct
            )
            
            scenarios['conservador'] = self.erlang_calculator.calculate_erlang_c(inputs_conservative)
            
            # Escenario 4: Optimista (percentil 75)
            p75_volume = np.percentile(hourly_volumes, 75)
            
            inputs_optimistic = ErlangInputs(
                calls_per_hour=p75_volume,
                average_handle_time=avg_tmo,
                service_level_target=sla_target,
                answer_time_target=answer_time,
                shrinkage_percentage=shrinkage_pct
            )
            
            scenarios['optimista'] = self.erlang_calculator.calculate_erlang_c(inputs_optimistic)
            
            return {
                'scenarios': {k: v.to_dict() for k, v in scenarios.items()},
                'volume_stats': {
                    'promedio': avg_volume,
                    'hora_pico': peak_volume,
                    'percentil_90': p90_volume,
                    'percentil_75': p75_volume
                },
                'tmo_info': {
                    'promedio_usado': avg_tmo,
                    'pico_usado': peak_tmo,
                    'escenario_pico_corregido': True  # Confirmar corrección aplicada
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error calculando escenarios: {e}")
            return {}
    
    def _validate_against_reality(self, df: pd.DataFrame, dimensioning_results: Dict) -> Dict:
        """Validar resultados de dimensionamiento contra datos reales"""
        try:
            # Estadísticas reales de TME
            real_tme_stats = {
                'promedio': df['tme'].mean(),
                'mediana': df['tme'].median(),
                'percentil_90': df['tme'].quantile(0.9),
                'std': df['tme'].std()
            }
            
            # Calcular SLA real (asumiendo objetivo de 20s)
            answer_time_target = 20
            calls_answered_in_time = (df['tme'] <= answer_time_target).sum()
            real_sla = (calls_answered_in_time / len(df)) * 100
            
            # Agentes reales promedio por día
            real_agents_per_day = df.groupby('fecha')['asesor'].nunique().mean()
            
            # Comparar con escenarios calculados
            comparisons = {}
            for scenario_name, scenario_results in dimensioning_results['scenarios'].items():
                predicted_wait = scenario_results['average_wait_time']
                predicted_sla = scenario_results['service_level']
                predicted_agents = scenario_results['agents_with_shrinkage']
                
                comparisons[scenario_name] = {
                    'tme_predicho_vs_real': {
                        'predicho': predicted_wait,
                        'real': real_tme_stats['promedio'],
                        'diferencia_absoluta': abs(predicted_wait - real_tme_stats['promedio']),
                        'precision_pct': 100 - abs((predicted_wait - real_tme_stats['promedio']) / real_tme_stats['promedio'] * 100)
                    },
                    'sla_predicho_vs_real': {
                        'predicho': predicted_sla,
                        'real': real_sla,
                        'diferencia_absoluta': abs(predicted_sla - real_sla)
                    },
                    'agentes_predicho_vs_real': {
                        'predicho': predicted_agents,
                        'real': real_agents_per_day,
                        'diferencia': predicted_agents - real_agents_per_day
                    }
                }
            
            return {
                'real_stats': {
                    'tme_stats': real_tme_stats,
                    'sla_real': real_sla,
                    'agentes_promedio_dia': real_agents_per_day,
                    'total_llamadas_analizadas': len(df)
                },
                'comparisons': comparisons,
                'best_scenario': self._find_best_scenario(comparisons)
            }
            
        except Exception as e:
            logger.error(f"❌ Error en validación: {e}")
            return {}
    
    def _find_best_scenario(self, comparisons: Dict) -> Dict:
        """Encontrar el escenario con mejor precisión"""
        try:
            best_scenario = None
            best_precision = -1
            
            for scenario_name, comparison in comparisons.items():
                precision = comparison['tme_predicho_vs_real']['precision_pct']
                if precision > best_precision:
                    best_precision = precision
                    best_scenario = scenario_name
            
            return {
                'nombre': best_scenario,
                'precision_tme': best_precision,
                'detalles': comparisons.get(best_scenario, {})
            }
            
        except Exception as e:
            logger.error(f"❌ Error encontrando mejor escenario: {e}")
            return {}
    
    def _generate_recommendations(self, historical_analysis: Dict, 
                                dimensioning_results: Dict, 
                                validation_results: Dict) -> Dict:
        """Generar recomendaciones basadas en el análisis"""
        try:
            recommendations = {
                'dimensionamiento': [],
                'operacional': [],
                'mejoras': []
            }
            
            best_scenario = validation_results.get('best_scenario', {})
            
            # Recomendaciones de dimensionamiento
            if best_scenario.get('nombre'):
                scenario_name = best_scenario['nombre']
                scenario_data = dimensioning_results['scenarios'][scenario_name]
                
                recommendations['dimensionamiento'].append({
                    'tipo': 'Escenario Recomendado',
                    'descripcion': f"Usar escenario '{scenario_name}' como base",
                    'agentes_recomendados': scenario_data['agents_with_shrinkage'],
                    'justificacion': f"Mejor precisión TME: {best_scenario['precision_tme']:.1f}%"
                })
            
            # Recomendaciones operacionales
            peak_hour = historical_analysis['volume_analysis']['peak_hour']
            recommendations['operacional'].append({
                'tipo': 'Horario Crítico',
                'descripcion': f"Reforzar dotación en hora {peak_hour}h",
                'detalle': f"Volumen pico: {historical_analysis['volume_analysis']['peak_volume']} llamadas/hora"
            })
            
            # Análisis de TMO
            avg_tmo = historical_analysis['tmo_analysis']['average_seconds']
            if avg_tmo > 300:  # Más de 5 minutos
                recommendations['mejoras'].append({
                    'tipo': 'Optimización TMO',
                    'descripcion': f"TMO promedio alto: {avg_tmo:.0f}s",
                    'sugerencia': 'Considerar capacitación para reducir tiempo de manejo'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generando recomendaciones: {e}")
            return {}
    
    def _create_executive_summary(self, historical_analysis: Dict, 
                                dimensioning_results: Dict, 
                                validation_results: Dict) -> Dict:
        """Crear resumen ejecutivo"""
        try:
            best_scenario = validation_results.get('best_scenario', {})
            scenario_name = best_scenario.get('nombre', 'promedio')
            recommended_scenario = dimensioning_results['scenarios'][scenario_name]
            
            return {
                'agentes_recomendados': recommended_scenario['agents_with_shrinkage'],
                'escenario_base': scenario_name,
                'precision_modelo': best_scenario.get('precision_tme', 0),
                'volumen_analizado': historical_analysis['total_calls'],
                'periodo_dias': historical_analysis['date_range']['days'],
                'sla_actual_estimado': validation_results['real_stats']['sla_real'],
                'tme_promedio_real': validation_results['real_stats']['tme_stats']['promedio'],
                'agentes_actuales_promedio': validation_results['real_stats']['agentes_promedio_dia']
            }
            
        except Exception as e:
            logger.error(f"❌ Error creando resumen ejecutivo: {e}")
            return {}
    
    def _log_complete_results(self, analysis: Dict):
        """Log completo de resultados"""
        try:
            print("\n" + "="*80)
            print("📊 RESUMEN EJECUTIVO - ANÁLISIS COMPLETO")
            print("="*80)
            
            summary = analysis['summary']
            print(f"📅 Período analizado: {analysis['period']['days_analyzed']} días")
            print(f"📞 Llamadas analizadas: {summary['volumen_analizado']:,}")
            print(f"👥 Agentes recomendados: {summary['agentes_recomendados']}")
            print(f"🎯 Escenario base: {summary['escenario_base']}")
            print(f"✅ Precisión del modelo: {summary['precision_modelo']:.1f}%")
            print(f"📈 SLA actual estimado: {summary['sla_actual_estimado']:.1f}%")
            print(f"⏳ TME promedio real: {summary['tme_promedio_real']:.1f}s")
            print(f"👥 Agentes actuales promedio: {summary['agentes_actuales_promedio']:.1f}")
            
            print("\n📋 ESCENARIOS CALCULADOS:")
            for scenario_name, scenario_data in analysis['dimensioning_results']['scenarios'].items():
                print(f"   {scenario_name.upper()}: {scenario_data['agents_with_shrinkage']} agentes | SL: {scenario_data['service_level']:.1f}%")
            
            print("\n💡 RECOMENDACIONES PRINCIPALES:")
            for rec in analysis['recommendations']['dimensionamiento']:
                print(f"   • {rec['descripcion']}")
            
            print("="*80)
            
        except Exception as e:
            logger.error(f"❌ Error en log de resultados: {e}")

# Instancia global
data_analyzer = DataAnalyzer()

def test_integration():
    """Test de integración completo"""
    print("🧪 Iniciando test de integración SQL + Erlang C...")
    
    try:
        # Usar fechas de los datos disponibles
        start_date = date(2025, 5, 15)
        end_date = date(2025, 5, 16)
        
        print(f"📅 Analizando período: {start_date} - {end_date}")
        
        # Ejecutar análisis completo
        results = data_analyzer.analyze_campaign_complete(
            start_date=start_date,
            end_date=end_date,
            sla_target=0.90,
            answer_time_target=20,
            shrinkage_pct=15.0
        )
        
        print("\n✅ Test de integración completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Test de integración fallido: {e}")
        logger.error(f"❌ Test de integración fallido: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar test de integración
    test_integration()