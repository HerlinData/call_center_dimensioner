"""
Dashboard principal para Flet - Call Center Dimensioner
"""

import flet as ft
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import logging
import sys
from pathlib import Path
import io
import base64
import kaleido
import plotly.io as pio
import tempfile
import os

# Agregar path para imports
sys.path.append(str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

class MainDashboard:
    def __init__(self, app_instance):
        self.app = app_instance
        self.page = app_instance.page
        self.colors = app_instance.colors
        
        # Variables del dashboard
        self.start_date = None
        self.end_date = None
        self.sla_target = 90
        self.answer_time_target = 20
        self.shrinkage_pct = 15
        self.date_range_info = None
        self.analysis_results = None

    def show(self):
        """Mostrar dashboard principal"""
        self.page.clean()
        
        # Obtener información de fechas disponibles
        self.load_date_range()
        
        # Header con título
        header = self.create_header()
        
        # Sidebar con controles
        sidebar = self.create_sidebar()
        
        # Área principal de contenido
        main_content = self.create_main_content()
        
        # Layout principal
        main_layout = ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(main_content, expand=True)
        ], expand=True)
        
        # Container principal
        page_content = ft.Column([
            header,
            ft.Divider(height=1),
            main_layout
        ], expand=True)
        
        self.page.add(page_content)
        self.page.update()

    def create_header(self):
        """Crear header del dashboard"""
        return ft.Container(
            content=ft.Row([
                # Título
                ft.Column([
                    ft.Text(
                        "📊 Dimensionador - Datos Históricos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=self.colors['text']
                    ),
                    ft.Text(
                        "Análisis inteligente basado en datos reales de SQL Server",
                        size=14,
                        color="#495057"
                    )
                ], spacing=5),
                
                # Botones de navegación
                ft.Row([
                    ft.ElevatedButton(
                        "🔄 Cambiar Análisis",
                        bgcolor="#6c757d",
                        color="white",
                        on_click=lambda e: self.app.show_analysis_selection()
                    ),
                    ft.ElevatedButton(
                        "⬅️ Cambiar Tipo",
                        bgcolor="#6c757d",
                        color="white", 
                        on_click=lambda e: self.app.show_mode_selection()
                    ),
                    ft.ElevatedButton(
                        "🚪 Cerrar Sesión",
                        bgcolor=self.colors['error'],
                        color="white",
                        on_click=lambda e: self.app.logout()
                    )
                ], spacing=10)
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#ffffff"
        )

    def create_sidebar(self):
        """Crear sidebar con controles"""
        return ft.Container(
            content=ft.Column([
                # Título del sidebar
                ft.Text(
                    "📊 Dimensionador",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['primary']
                ),
                
                ft.Divider(),
                
                # Sección de fechas
                ft.Text("📅 Período de Análisis", size=16, weight=ft.FontWeight.BOLD),
                
                # Date pickers
                ft.Row([
                    ft.Column([
                        ft.Text("Inicio", size=12, color="#495057"),
                        ft.TextField(
                            value=str(self.start_date) if self.start_date else "",
                            width=120,
                            content_padding=ft.padding.all(8),
                            ref=ft.Ref[ft.TextField]()
                        )
                    ], spacing=5),
                    ft.Column([
                        ft.Text("Fin", size=12, color="#495057"),
                        ft.TextField(
                            value=str(self.end_date) if self.end_date else "",
                            width=120,
                            content_padding=ft.padding.all(8),
                            ref=ft.Ref[ft.TextField]()
                        )
                    ], spacing=5)
                ], spacing=10),
                
                ft.Divider(),
                
                # Parámetros SLA
                ft.Text("🎯 Parámetros SLA", size=16, weight=ft.FontWeight.BOLD),
                
                ft.Row([
                    ft.Column([
                        ft.Text("SLA %", size=12, color="#495057"),
                        ft.Dropdown(
                            width=100,
                            value=str(self.sla_target),
                            options=[
                                ft.dropdown.Option("80", "80%"),
                                ft.dropdown.Option("85", "85%"),
                                ft.dropdown.Option("90", "90%"),
                                ft.dropdown.Option("95", "95%")
                            ],
                            on_change=lambda e: setattr(self, 'sla_target', int(e.control.value))
                        )
                    ], spacing=5),
                    ft.Column([
                        ft.Text("Tiempo (s)", size=12, color="#495057"),
                        ft.Dropdown(
                            width=100,
                            value=str(self.answer_time_target),
                            options=[
                                ft.dropdown.Option("15", "15s"),
                                ft.dropdown.Option("20", "20s"),
                                ft.dropdown.Option("25", "25s"),
                                ft.dropdown.Option("30", "30s")
                            ],
                            on_change=lambda e: setattr(self, 'answer_time_target', int(e.control.value))
                        )
                    ], spacing=5)
                ], spacing=10),
                
                # Shrinkage
                ft.Text("⚙️ Shrinkage (%)", size=14, color="#495057"),
                ft.Dropdown(
                    width=220,
                    value=str(self.shrinkage_pct),
                    options=[
                        ft.dropdown.Option("10", "10%"),
                        ft.dropdown.Option("15", "15%"),
                        ft.dropdown.Option("20", "20%"),
                        ft.dropdown.Option("25", "25%")
                    ],
                    on_change=lambda e: setattr(self, 'shrinkage_pct', int(e.control.value))
                ),
                
                ft.Container(height=20),  # Spacer
                
                # Botón principal
                ft.ElevatedButton(
                    "🚀 Ejecutar Análisis",
                    width=220,
                    height=50,
                    bgcolor=self.colors['primary'],
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation={"": 3, "hovered": 6}
                    ),
                    on_click=lambda e: self.execute_analysis()
                ),
                
                ft.Divider(),
                
                # Información compacta
                self.create_info_section()
                
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            width=260,
            padding=20,
            bgcolor="#ffffff",
            border=ft.border.all(1, "#d6d8db")
        )

    def create_info_section(self):
        """Crear sección de información"""
        if not self.date_range_info:
            return ft.Container()
            
        return ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("📊 Registros", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{self.date_range_info.get('total_registros', 0):,}", size=14)
                ]),
                ft.Column([
                    ft.Text("👥 Asesores", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(str(self.date_range_info.get('total_asesores', 0)), size=14)
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Text(
                f"📅 {self.date_range_info.get('fecha_min', '')} → {self.date_range_info.get('fecha_max', '')}",
                size=10,
                color="#6c757d"
            )
        ], spacing=8)

    def create_main_content(self):
        """Crear área principal de contenido"""
        if self.analysis_results:
            return self.create_results_view()
        else:
            return self.create_welcome_view()

    def create_welcome_view(self):
        """Crear vista de bienvenida"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "👋 Bienvenido al Dimensionador Call Center",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Cards de información si hay datos disponibles
                self.create_stats_cards() if self.date_range_info else ft.Container(),
                
                # Instrucciones
                ft.Container(
                    content=ft.Column([
                        ft.Text("🎯 Cómo usar el sistema:", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("1. 📅 Selecciona el período de análisis en el panel izquierdo"),
                        ft.Text("2. ⚙️ Ajusta los parámetros de SLA y shrinkage según tus necesidades"),
                        ft.Text("3. 🚀 Ejecuta el análisis para obtener dimensionamiento basado en datos reales"),
                        ft.Text("4. 📊 Revisa los resultados y escenarios recomendados"),
                        ft.Text("5. 📄 Exporta los reportes en Excel para presentaciones"),
                        
                        ft.Container(height=20),
                        
                        ft.Text("✨ Características principales:", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("- Análisis en tiempo real con datos de SQL Server"),
                        ft.Text("- Múltiples escenarios de dimensionamiento"),
                        ft.Text("- Validación automática contra datos históricos reales"),
                        ft.Text("- Recomendaciones inteligentes basadas en análisis estadístico"),
                        ft.Text("- Exportación a Excel con gráficos integrados")
                    ], spacing=8),
                    padding=20,
                    bgcolor="#e7f1ff",
                    border_radius=10,
                    border=ft.border.all(1, "#9ec5fe")
                )
                
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30),
            padding=40,
            alignment=ft.alignment.center,
            expand=True
        )

    def create_stats_cards(self):
        """Crear cards de estadísticas"""
        if not self.date_range_info:
            return ft.Container()
            
        return ft.Row([
            self.create_stat_card(
                "📞 Total Registros", 
                f"{self.date_range_info.get('total_registros', 0):,}",
                "#0d6efd"
            ),
            self.create_stat_card(
                "👥 Total Asesores",
                str(self.date_range_info.get('total_asesores', 0)),
                "#198754"
            ),
            self.create_stat_card(
                "📅 Fecha Inicio",
                str(self.date_range_info.get('fecha_min', '')),
                "#fd7e14"
            ),
            self.create_stat_card(
                "📅 Fecha Fin", 
                str(self.date_range_info.get('fecha_max', '')),
                "#6f42c1"
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20)

    def create_stat_card(self, title, value, color):
        """Crear card de estadística individual"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, color="#495057", text_align=ft.TextAlign.CENTER),
                ft.Text(
                    value, 
                    size=24, 
                    weight=ft.FontWeight.BOLD, 
                    color=color,
                    text_align=ft.TextAlign.CENTER
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8),
            width=200,
            height=100,
            padding=15,
            bgcolor="#ffffff",
            border_radius=10,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=f"{color}1a",  # 10% opacity
                offset=ft.Offset(0, 2)
            )
        )

    def create_results_view(self):
        """Crear vista de resultados del análisis"""
        if not self.analysis_results:
            return self.create_welcome_view()
            
        try:
            # Obtener resultados del análisis
            results = self.analysis_results
            
            # Crear tabs de resultados
            tabs = ft.Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="📊 Escenarios",
                        content=self.create_scenarios_tab(results)
                    ),
                    ft.Tab(
                        text="📈 Gráficos", 
                        content=self.create_charts_tab(results)
                    ),
                    ft.Tab(
                        text="💡 Recomendaciones",
                        content=self.create_recommendations_tab(results)
                    ),
                    ft.Tab(
                        text="📄 Exportar",
                        content=self.create_export_tab(results)
                    )
                ],
                expand=True
            )
            
            return ft.Container(
                content=ft.Column([
                    # Header de resultados
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(
                                    "📊 Resultados del Análisis",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colors['text']
                                ),
                                ft.Text(
                                    f"Período: {self.start_date} → {self.end_date}",
                                    size=14,
                                    color=self.colors['text_secondary']
                                )
                            ]),
                            ft.ElevatedButton(
                                "🔄 Nuevo Análisis",
                                bgcolor=self.colors['primary'],
                                color="white",
                                on_click=lambda e: self.clear_results()
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.only(bottom=20)
                    ),
                    
                    # Métricas principales
                    self.create_summary_metrics(results),
                    
                    # Tabs con resultados detallados
                    tabs
                ], spacing=15),
                padding=20,
                expand=True
            )
            
        except Exception as e:
            logger.error(f"Error creando vista de resultados: {e}")
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        "❌ Error mostrando resultados",
                        size=20,
                        color=self.colors['error']
                    ),
                    ft.Text(str(e), size=14),
                    ft.ElevatedButton(
                        "🔄 Reintentar",
                        on_click=lambda e: self.execute_analysis()
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )

    def create_summary_metrics(self, results):
        """Crear métricas resumen principales"""
        try:
            # Extraer métricas principales del resumen
            summary = results.get('summary', {})
            
            metrics = [
                ("👥 Agentes Recomendados", f"{summary.get('agentes_recomendados', 0)}", self.colors['primary']),
                ("🎯 Escenario Base", summary.get('escenario_base', 'N/A').upper(), self.colors['secondary']),
                ("✅ Precisión Modelo", f"{summary.get('precision_modelo', 0):.1f}%", self.colors['accent']),
                ("📈 SLA Actual Est.", f"{summary.get('sla_actual_estimado', 0):.1f}%", "#6c757d"),
                ("⏳ TME Promedio Real", f"{summary.get('tme_promedio_real', 0):.1f}s", "#6c757d"),
                ("📞 Llamadas Analizadas", f"{summary.get('volumen_analizado', 0):,}", "#6c757d")
            ]
            
            return ft.Container(
                content=ft.ResponsiveRow([
                    self.create_metric_card(title, value, color)
                    for title, value, color in metrics
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                padding=ft.padding.symmetric(vertical=20),
                bgcolor="#ffffff",
                border_radius=10,
                border=ft.border.all(1, "#e9ecef")
            )
            
        except Exception as e:
            logger.error(f"Error creando métricas resumen: {e}")
            return ft.Container()

    def create_metric_card(self, title, value, color):
        """Crear card de métrica individual"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=12, color="#6c757d", text_align=ft.TextAlign.CENTER),
                ft.Text(
                    value, 
                    size=20, 
                    weight=ft.FontWeight.BOLD, 
                    color=color,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            width=150,
            padding=15,
            bgcolor="#ffffff",
            border_radius=8,
            border=ft.border.all(1, f"{color}40")
        )

    def create_scenarios_tab(self, results):
        """Crear tab de escenarios"""
        scenarios = results.get('dimensioning_results', {}).get('scenarios', {})
        best_scenario_name = results.get('validation_results', {}).get('best_scenario', {}).get('nombre', '').lower()

        scenario_cards = []
        for name, data in scenarios.items():
            is_recommended = name.lower() == best_scenario_name
            border_color = self.colors['primary'] if is_recommended else "#e9ecef"
            bg_color = "#f0f8ff" if is_recommended else "#ffffff" # Light blue for recommended

            card_content = ft.Column([
                ft.Text(
                    f"{name.upper()} {'⭐ RECOMENDADO' if is_recommended else ''}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['primary'] if is_recommended else self.colors['text']
                ),
                ft.Divider(),
                ft.Text(f"👥 Agentes: {data.get('agents_with_shrinkage', 0)}", size=14),
                ft.Text(f"📈 Utilización: {data.get('utilization', 0):.1f}%", size=14),
                ft.Text(f"🎯 Nivel Servicio: {data.get('service_level', 0):.1f}%", size=14),
                ft.Text(f"⏱️ Tiempo Espera: {data.get('average_wait_time', 0):.1f}s", size=14),
                ft.Text(f"📊 Prob. Esperar: {data.get('probability_of_wait', 0):.1f}%", size=14),
                ft.Text(f"🔥 Intensidad: {data.get('traffic_intensity', 0):.1f} Erlangs", size=14),
            ], spacing=8)

            scenario_cards.append(
                ft.Container(
                    content=card_content,
                    padding=20,
                    bgcolor=bg_color,
                    border_radius=10,
                    border=ft.border.all(2, border_color),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color=f"{border_color}1a",
                        offset=ft.Offset(0, 2)
                    ),
                    expand=True
                )
            )

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "📊 Escenarios de Dimensionamiento",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text']
                ),
                ft.Text(
                    "Resultados detallados por escenario. El escenario recomendado se basa en la mayor precisión de TME.",
                    size=14,
                    color=self.colors['text_secondary']
                ),
                ft.ResponsiveRow(scenario_cards, spacing=20, run_spacing=20)
            ], spacing=15),
            padding=20
        )

    def create_charts_tab(self, results):
        """Crear tab de gráficos"""
        if not self.analysis_results:
            return ft.Container(
                content=ft.Text("No hay resultados de análisis para mostrar gráficos.", size=14),
                padding=20,
                bgcolor="#f8f9fa",
                border_radius=8
            )

        scenarios = results.get('dimensioning_results', {}).get('scenarios', {})
        targets = results.get('targets', {})
        
        chart_elements = []

        if scenarios:
            df_scenarios = pd.DataFrame.from_dict(scenarios, orient='index')
            df_scenarios.index.name = 'Escenario'
            df_scenarios = df_scenarios.reset_index()

            # Gráfico 1: Agentes Requeridos por Escenario
            fig1 = px.bar(
                df_scenarios,
                x='Escenario',
                y='agents_with_shrinkage',
                title='👥 Agentes Requeridos por Escenario',
                labels={'agents_with_shrinkage': 'Agentes'},
                color_discrete_sequence=[self.colors['primary']]
            )
            fig1.update_layout(title_x=0.5)
            img_bytes1 = fig1.to_image(format="png")
            encoded_img1 = base64.b64encode(img_bytes1).decode('utf-8')
            chart_elements.append(ft.Image(src_base64=encoded_img1, fit=ft.ImageFit.CONTAIN, expand=True))

            # Gráfico 2: Nivel de Servicio vs Tiempo de Espera
            fig2 = px.scatter(
                df_scenarios,
                x='average_wait_time',
                y='service_level',
                text='Escenario',
                size='agents_with_shrinkage',
                title='🎯 Nivel de Servicio vs Tiempo de Espera',
                labels={'average_wait_time': 'Tiempo de Espera (s)', 'service_level': 'Nivel de Servicio (%)'},
                color_discrete_sequence=[self.colors['accent']]
            )
            fig2.update_traces(textposition='top center')
            fig2.update_layout(title_x=0.5)
            
            # Añadir línea de SLA objetivo
            if 'sla_target' in targets:
                fig2.add_hline(y=targets['sla_target'], line_dash="dash", line_color="red",
                               annotation_text=f"SLA Objetivo: {targets['sla_target']:.0f}%",
                               annotation_position="bottom right")

            img_bytes2 = fig2.to_image(format="png")
            encoded_img2 = base64.b64encode(img_bytes2).decode('utf-8')
            chart_elements.append(ft.Image(src_base64=encoded_img2, fit=ft.ImageFit.CONTAIN, expand=True))

        else:
            chart_elements.append(ft.Text("No hay datos de escenarios para generar gráficos.", size=14))

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "📈 Visualizaciones",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text']
                ),
                ft.Text("Gráficos generados a partir de los resultados del análisis.", size=14, color=self.colors['text_secondary']),
                ft.Column(chart_elements, expand=True)
            ], spacing=15),
            padding=20,
            expand=True
        )

    def create_recommendations_tab(self, results):
        """Crear tab de recomendaciones"""
        if not self.analysis_results:
            return ft.Container(
                content=ft.Text("No hay resultados de análisis para mostrar recomendaciones.", size=14),
                padding=20,
                bgcolor="#f8f9fa",
                border_radius=8
            )

        recommendations = results.get('recommendations', {})
        validation = results.get('validation_results', {})
        best_scenario = validation.get('best_scenario', {})

        recommendation_elements = []

        # Recomendaciones de dimensionamiento
        if recommendations.get('dimensionamiento'):
            recommendation_elements.append(ft.Text("#### 🎯 Dimensionamiento", size=16, weight=ft.FontWeight.BOLD))
            for rec in recommendations['dimensionamiento']:
                recommendation_elements.append(ft.Container(
                    content=ft.Column([
                        ft.Text(f"**{rec.get('tipo', '')}:** {rec.get('descripcion', '')}", size=14, selectable=True),
                        ft.Text(f"*Justificación: {rec.get('justificacion', '')}*", size=12, color=self.colors['text_secondary'], selectable=True)
                    ], spacing=2),
                    padding=ft.padding.only(left=10, bottom=5)
                ))

        # Recomendaciones operacionales
        if recommendations.get('operacional'):
            recommendation_elements.append(ft.Text("#### ⚙️ Operacionales", size=16, weight=ft.FontWeight.BOLD))
            for rec in recommendations['operacional']:
                recommendation_elements.append(ft.Container(
                    content=ft.Column([
                        ft.Text(f"**{rec.get('tipo', '')}:** {rec.get('descripcion', '')}", size=14, selectable=True),
                        ft.Text(f"*Detalle: {rec.get('detalle', '')}*", size=12, color=self.colors['text_secondary'], selectable=True)
                    ], spacing=2),
                    padding=ft.padding.only(left=10, bottom=5)
                ))

        # Oportunidades de mejora
        if recommendations.get('mejoras'):
            recommendation_elements.append(ft.Text("#### 🚀 Oportunidades de Mejora", size=16, weight=ft.FontWeight.BOLD))
            for rec in recommendations['mejoras']:
                recommendation_elements.append(ft.Container(
                    content=ft.Column([
                        ft.Text(f"**{rec.get('tipo', '')}:** {rec.get('descripcion', '')}", size=14, selectable=True),
                        ft.Text(f"*Sugerencia: {rec.get('sugerencia', '')}*", size=12, color=self.colors['text_secondary'], selectable=True)
                    ], spacing=2),
                    padding=ft.padding.only(left=10, bottom=5)
                ))

        # Validación del modelo
        if best_scenario.get('nombre'):
            precision = best_scenario.get('precision_tme', 0)
            status_text = "Precisión del modelo: "
            if precision > 80:
                status_text += f"Excelente ({precision:.1f}%) ✅"
                status_color = self.colors['success']
            elif precision > 60:
                status_text += f"Aceptable ({precision:.1f}%) ⚠️"
                status_color = self.colors['accent']
            else:
                status_text += f"Requiere calibración ({precision:.1f}%) ❌"
                status_color = self.colors['error']
            
            recommendation_elements.append(ft.Text("#### ✅ Validación del Modelo", size=16, weight=ft.FontWeight.BOLD))
            recommendation_elements.append(ft.Text(status_text, size=14, color=status_color, selectable=True))
            recommendation_elements.append(ft.Text(f"Escenario más preciso: {best_scenario.get('nombre', 'N/A').upper()}", size=12, color=self.colors['text_secondary'], selectable=True))

        if not recommendation_elements:
            recommendation_elements.append(ft.Text("No se generaron recomendaciones para este análisis.", size=14))

        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "💡 Recomendaciones Inteligentes",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text']
                ),
                ft.Text("Sugerencias y validaciones basadas en el análisis de datos.", size=14, color=self.colors['text_secondary']),
                ft.Column(recommendation_elements, spacing=10, expand=True)
            ], spacing=15),
            padding=20,
            expand=True
        )

    def create_export_tab(self, results):
        """Crear tab de exportación"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "📄 Exportar Resultados",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text']
                ),
                ft.Text("Descarga reportes en diferentes formatos", size=14, color=self.colors['text_secondary']),
                
                # Opciones de exportación
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon("file_download", size=20),
                                ft.Text("Descargar Excel", size=14)
                            ], spacing=8),
                            bgcolor=self.colors['primary'],
                            color="white",
                            width=200,
                            on_click=lambda e: self.export_excel()
                        ),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon("table_chart", size=20),
                                ft.Text("Descargar CSV", size=14)
                            ], spacing=8),
                            bgcolor=self.colors['secondary'],
                            color="white",
                            width=200,
                            on_click=lambda e: self.export_csv()
                        )
                    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor="#f8f9fa",
                    border_radius=8
                )
            ], spacing=15),
            padding=20
        )

    def clear_results(self):
        """Limpiar resultados y volver a vista de bienvenida"""
        self.analysis_results = None
        self.update_main_content()

    def export_excel(self):
        """Exportar resultados a Excel"""
        if not self.analysis_results:
            self.show_error("❌ No hay resultados para exportar.")
            return

        try:
            from reports.excel_generator import ExcelGenerator
            generator = ExcelGenerator(self.analysis_results)
            
            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                file_path = tmp_file.name
                generator.generate_report(file_path)
            
            self.page.launch_url(f"file:///{file_path}")
            self.show_success("✅ Reporte Excel generado y descargado.")

        except Exception as e:
            logger.error(f"Error exportando a Excel: {e}")
            self.show_error(f"❌ Error al generar Excel: {e}")

    def export_csv(self):
        """Exportar resultados a CSV"""
        if not self.analysis_results:
            self.show_error("❌ No hay resultados para exportar.")
            return

        try:
            scenarios = self.analysis_results.get('dimensioning_results', {}).get('scenarios', {})
            if not scenarios:
                self.show_error("❌ No hay datos de escenarios para exportar a CSV.")
                return

            df_export = pd.DataFrame([
                {
                    'Escenario': name,
                    'Agentes_Requeridos': data.get('agents_required', 0),
                    'Agentes_Con_Shrinkage': data.get('agents_with_shrinkage', 0),
                    'Nivel_Servicio_Pct': data.get('service_level', 0),
                    'Tiempo_Espera_Seg': data.get('average_wait_time', 0),
                    'Utilizacion_Pct': data.get('utilization', 0),
                    'Probabilidad_Esperar_Pct': data.get('probability_of_wait', 0),
                    'Intensidad_Trafico': data.get('traffic_intensity', 0)
                }
                for name, data in scenarios.items()
            ])

            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='') as tmp_file:
                file_path = tmp_file.name
                df_export.to_csv(file_path, index=False)
            
            self.page.launch_url(f"file:///{file_path}")
            self.show_success("✅ Datos CSV generados y descargados.")

        except Exception as e:
            logger.error(f"Error exportando a CSV: {e}")
            self.show_error(f"❌ Error al generar CSV: {e}")

    def load_date_range(self):
        """Cargar rango de fechas disponibles"""
        try:
            from data.sql_connector import sql_connector
            self.date_range_info = sql_connector.get_available_date_range()
            
            if self.date_range_info:
                self.start_date = self.date_range_info['fecha_min']
                self.end_date = self.date_range_info['fecha_max']
                
        except Exception as e:
            logger.error(f"Error cargando rango de fechas: {e}")
            self.show_error(f"❌ Error conectando con la base de datos: {e}")

    def execute_analysis(self):
        """Ejecutar análisis completo"""
        try:
            # Mostrar indicador de carga
            self.show_loading("⏳ Ejecutando análisis...")
            
            # Importar el analizador de datos
            from data.data_analyzer import data_analyzer
            
            # Ejecutar análisis
            results = data_analyzer.analyze_campaign_complete(
                start_date=self.start_date,
                end_date=self.end_date,
                sla_target=self.sla_target / 100,
                answer_time_target=self.answer_time_target,
                shrinkage_pct=self.shrinkage_pct
            )
            
            self.analysis_results = results
            
            # Actualizar vista con resultados
            self.update_main_content()
            
            self.show_success("✅ Análisis completado exitosamente")
            
        except Exception as e:
            logger.error(f"Error en análisis: {e}")
            self.show_error(f"❌ Error en el análisis: {e}")

    def update_main_content(self):
        """Actualizar el contenido principal"""
        # Limpiar y recrear el contenido principal
        # TODO: Implementar actualización dinámica
        self.show()

    def show_loading(self, message):
        """Mostrar indicador de carga"""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.ProgressRing(width=16, height=16, stroke_width=2),
                ft.Text(message, color="white")
            ], spacing=10),
            bgcolor="#0d6efd"
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        snack = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=self.colors['success']
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def show_error(self, message):
        """Mostrar mensaje de error"""
        snack = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=self.colors['error']
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()