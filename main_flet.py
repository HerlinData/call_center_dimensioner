"""
Call Center Dimensioner - Aplicación Flet
Sistema de dimensionamiento para call centers con interfaz moderna
"""

import flet as ft
import sys
from pathlib import Path
import logging

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

class CallCenterApp:
    def __init__(self):
        self.current_user = None
        self.modo_operacion = None  # 'existente' o 'nueva'
        self.tipo_analisis = None   # 'basico', 'intermedio', 'avanzado'
        
        # Paleta de colores profesional
        self.colors = {
            'primary': '#DA7756',          # Claude Orange (primario)
            'secondary': '#2E3A59',        # Navy profundo
            'accent': '#56D6C3',           # Turquesa suave
            'background': '#F4F4F4',       # Fondo gris muy claro
            'surface': '#ffffff',          # Superficie blanca
            'text': '#333333',             # Texto antracita
            'text_secondary': '#6c757d',   # Texto secundario
            'success': '#28a745',          # Verde éxito
            'warning': '#ffc107',          # Amarillo advertencia
            'error': '#dc3545'             # Rojo error
        }

    def main(self, page: ft.Page):
        """Función principal de la aplicación"""
        # Configuración de la página
        page.title = "Call Center Dimensioner - AMG"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = self.colors['background']
        page.window_width = 1200
        page.window_height = 800
        page.window_min_width = 800
        page.window_min_height = 600
        
        # Tema personalizado
        page.theme = ft.Theme(
            color_scheme_seed=self.colors['primary'],
            use_material3=True
        )
        
        self.page = page
        
        # Iniciar con pantalla de login
        self.show_login()
        
        page.update()

    def show_login(self):
        """Mostrar pantalla de login"""
        self.page.clean()
        
        # Fondo degradado
        background = ft.Container(
            content=ft.Stack([
                # Círculos decorativos de fondo
                ft.Container(
                    width=300,
                    height=300,
                    bgcolor=f"{self.colors['primary']}10",
                    border_radius=150,
                    left=-100,
                    top=-100
                ),
                ft.Container(
                    width=200,
                    height=200,
                    bgcolor=f"{self.colors['accent']}08",
                    border_radius=100,
                    right=-50,
                    bottom=-50
                ),
                
                # Container principal centrado
                ft.Container(
                    content=ft.Column([
                        # Header con logo animado
                        ft.Container(
                            content=ft.Column([
                                # Logo principal con efecto
                                ft.Container(
                                    content=ft.Text(
                                        "🎯",
                                        size=80,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    animate=1000,
                                    on_hover=lambda e: self.animate_logo_hover(e)
                                ),
                                
                                # Título principal
                                ft.Text(
                                    "AMG TELECOM",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colors['primary'],
                                    text_align=ft.TextAlign.CENTER
                                ),
                                
                                # Subtítulo elegante
                                ft.Text(
                                    "Sistema de Dimensionamiento Call Center",
                                    size=16,
                                    color="#495057",
                                    text_align=ft.TextAlign.CENTER,
                                    weight=ft.FontWeight.W_300
                                ),
                                
                                # Línea decorativa
                                ft.Container(
                                    width=120,
                                    height=2,
                                    bgcolor=self.colors['primary'],
                                    border_radius=1,
                                    margin=ft.margin.symmetric(vertical=20)
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8),
                            margin=ft.margin.only(bottom=40),
                            animate=800
                        ),
                        
                        # Card de login elegante
                        ft.Container(
                            content=ft.Column([
                                # Título del formulario
                                ft.Text(
                                    "🔐 Acceso Seguro",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colors['text'],
                                    text_align=ft.TextAlign.CENTER
                                ),
                                
                                ft.Container(height=20),  # Spacer
                                
                                # Campo de contraseña mejorado
                                ft.TextField(
                                    label="Clave de acceso",
                                    password=True,
                                    width=280,
                                    border_radius=15,
                                    content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                    hint_text="Ingresa tu clave",
                                    prefix_icon="lock_outline",
                                    border_color=self.colors['primary'],
                                    focused_border_color=self.colors['primary'],
                                    ref=ft.Ref[ft.TextField](),
                                    on_submit=lambda e: self.handle_login(),
                                    autofocus=True
                                ),
                                
                                ft.Container(height=25),  # Spacer
                                
                                # Botón de login mejorado
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Row([
                                            ft.Icon("login", size=20),
                                            ft.Text("INGRESAR", size=16, weight=ft.FontWeight.BOLD)
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                        width=280,
                                        height=55,
                                        bgcolor=self.colors['primary'],
                                        color="white",
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=15),
                                            elevation={"": 4, "hovered": 12, "pressed": 8},
                                            animation_duration=200
                                        ),
                                        on_click=lambda e: self.handle_login()
                                    ),
                                    animate=200
                                ),
                                
                                ft.Container(height=20),  # Spacer
                                
                                # Información de seguridad
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon("security", size=16, color="#6c757d"),
                                        ft.Text(
                                            "Conexión segura encriptada",
                                            size=12,
                                            color="#6c757d"
                                        )
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                    margin=ft.margin.only(top=10)
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5),
                            
                            # Estilo de la card
                            width=360,
                            padding=35,
                            bgcolor="#ffffff",
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=25,
                                color="#00000015",
                                offset=ft.Offset(0, 8)
                            ),
                            border=ft.border.all(1, "#e9ecef"),
                            animate=600
                        ),
                        
                        # Footer informativo
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon("phone", size=16, color="#6c757d"),
                                    ft.Text("Telecom Operations", size=12, color="#6c757d")
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                                
                                ft.Text(
                                    "© 2024 AMG - Sistema Profesional de Dimensionamiento",
                                    size=10,
                                    color="#adb5bd",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], spacing=5),
                            margin=ft.margin.only(top=30),
                            animate=1000
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=25),
                    
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=ft.padding.all(40)
                )
            ]),
            expand=True,
            bgcolor="#f8f9fa"
        )
        
        self.page.add(background)
        self.page.update()
        
        # Guardar referencia al campo de contraseña
        self.password_field = background.content.controls[2].content.controls[1].content.controls[2]

    def handle_login(self):
        """Manejar el login"""
        password = self.password_field.value
        
        # Importar el sistema de autenticación para Flet
        try:
            from config.auth_flet import auth_manager
            success, message = auth_manager.authenticate(password)
            if success:
                self.current_user = "authenticated"
                self.show_mode_selection()
            else:
                self.show_error(message)
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            self.show_error("❌ Error en el sistema de autenticación")

    def show_error(self, message):
        """Mostrar mensaje de error"""
        # Crear SnackBar para mostrar error
        snack = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=self.colors['error']
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def show_mode_selection(self):
        """Mostrar selección de modo de campaña con el estilo profesional."""
        self.page.clean()
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "📊 Selecciona el Modo de Operación",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text'],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Elige si analizarás una campaña existente o dimensionarás una nueva",
                    size=16,
                    color=self.colors['text_secondary'],
                    text_align=ft.TextAlign.CENTER
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=40
        )
        
        # Cards de selección en fila
        cards_row = ft.Row([
            # Campaña Existente
            self.create_selection_card(
                title="📈 Campaña Existente",
                subtitle="Análisis basado en datos históricos",
                features=[
                    "• Conexión a SQL Server",
                    "• Validación automática de modelos",
                    "• Múltiples escenarios (promedio, pico, etc.)",
                    "• Ideal para optimizar operaciones actuales"
                ],
                color=self.colors['primary'],
                button_text="Analizar Existente",
                on_click_handler=lambda e: self.select_mode('existente')
            ),
            
            # Campaña Nueva
            self.create_selection_card(
                title="🚀 Campaña Nueva", 
                subtitle="Dimensionamiento para nuevas operaciones",
                features=[
                    "• Inputs manuales de volumen y TMO",
                    "• Cálculos basados en Erlang C",
                    "• Escenarios optimista y conservador",
                    "• Ideal para planificar nuevos servicios"
                ],
                color=self.colors['secondary'],
                button_text="Dimensionar Nueva",
                on_click_handler=lambda e: self.select_mode('nueva')
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40)
        
        # Layout principal
        main_content = ft.Column([
            header,
            ft.Container(cards_row, padding=ft.padding.symmetric(horizontal=50), expand=True, alignment=ft.alignment.center)
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Botón de logout
        logout_btn = ft.Container(
            content=ft.TextButton("Cerrar Sesión", icon="logout", on_click=lambda e: self.logout()),
            alignment=ft.alignment.top_right,
            padding=20
        )

        page_layout = ft.Stack([
            main_content,
            logout_btn
        ])

        self.page.add(page_layout)
        self.page.update()

    def select_mode(self, mode):
        """Seleccionar modo de operación"""
        self.modo_operacion = mode
        self.show_analysis_selection()

    def show_analysis_selection(self):
        """Mostrar selección de tipo de análisis"""
        self.page.clean()
        
        tipo_campana = "Campaña Existente" if self.modo_operacion == 'existente' else "Campaña Nueva"
        
        # Header
        header = ft.Column([
            ft.Text(
                "🎯 Selecciona el Tipo de Análisis",
                size=48,
                weight=ft.FontWeight.BOLD,
                color=self.colors['text'],
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                f"Para tu {tipo_campana}",
                size=24,
                weight=ft.FontWeight.W_500,
                color="#495057",
                text_align=ft.TextAlign.CENTER
            )
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8)
        
        # Cards de análisis en fila
        cards_row = ft.Row([
            # Análisis Básico
            self.create_analysis_specific_card(
                title="⚡ Análisis Básico",
                subtitle="Dimensionamiento rápido con Erlang C",
                features=[
                    "• Cálculos instantáneos (< 1 seg)",
                    "• Dimensionamiento preciso",
                    "• Resultados inmediatos", 
                    "• Ideal para análisis rápido"
                ],
                color=self.colors['primary'],
                button_text="Seleccionar Básico",
                on_click_handler=lambda e: self.select_analysis('basico')
            ),
            
            # Análisis Intermedio
            self.create_analysis_specific_card(
                title="📊 Análisis Intermedio", 
                subtitle="Simulación con abandonos incluidos",
                features=[
                    "• Simulaciones con SimPy",
                    "• Incluye abandonos de llamadas",
                    "• Análisis más realista",
                    "• Tiempo: 2-5 segundos"
                ],
                color=self.colors['secondary'],
                button_text="Seleccionar Intermedio",
                on_click_handler=lambda e: self.select_analysis('intermedio')
            ),
            
            # Análisis Avanzado
            self.create_analysis_specific_card(
                title="🔬 Análisis Avanzado",
                subtitle="Shrinkage + validación automática", 
                features=[
                    "• Validación automática",
                    "• Incluye shrinkage detallado",
                    "• Múltiples escenarios",
                    "• Análisis más completo"
                ],
                color=self.colors['accent'],
                button_text="Seleccionar Avanzado",
                on_click_handler=lambda e: self.select_analysis('avanzado')
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50)
        
        # Botón para volver
        back_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon("arrow_back", size=20),
                ft.Text("Cambiar Modo de Operación", size=14, weight=ft.FontWeight.W_500)
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            width=280,
            height=50,
            bgcolor="#000000",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation={"": 4, "hovered": 8}
            ),
            on_click=lambda e: self.show_mode_selection()
        )

        # Layout principal
        main_content = ft.Column([
            ft.Container(expand=True),  # Spacer superior
            header,
            ft.Container(height=25),    # Separación específica entre header y tarjetas
            cards_row,
            ft.Container(height=25),    # Separación específica entre tarjetas y botón
            back_button,
            ft.Container(expand=True)   # Spacer inferior
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, expand=True)
        
        self.page.add(main_content)
        self.page.update()

    def create_selection_card(self, title, subtitle, features, color, button_text, on_click_handler):
        """Crear una card de selección profesional y reutilizable."""
        
        # Animación de hover
        def animate_card_hover(e):
            if e.data == "true":
                e.control.shadow.blur_radius = 20
                e.control.shadow.color = f"{color}40"
                e.control.scale = ft.transform.Scale(1.03)
            else:
                e.control.shadow.blur_radius = 6
                e.control.shadow.color = f"{color}26"
                e.control.scale = ft.transform.Scale(1)
            e.control.update()

        return ft.Container(
            content=ft.Column([
                # Título
                ft.Text(
                    title,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Subtítulo
                ft.Text(
                    subtitle,
                    size=16,
                    color="#495057",
                    text_align=ft.TextAlign.CENTER,
                    height=60 # Increased height for more space
                ),
                
                ft.Divider(height=1, color="#eeeeee"),

                # Características
                ft.Container(
                    content=ft.Column([
                        *[ft.Row([
                            ft.Icon(name="check_circle_outline", color=self.colors['success'], size=18),
                            ft.Text(feature.replace("• ",""), size=14, expand=True)
                        ], spacing=12) for feature in features]
                    ], spacing=10),
                    margin=ft.margin.symmetric(vertical=25),
                    height=180 # Increased height for more features/spacing
                ),
                
                # Botón
                ft.ElevatedButton(
                    button_text,
                    width=280,
                    height=55,
                    bgcolor=color,
                    color="white", 
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation={"hovered": 10}
                    ),
                    on_click=on_click_handler
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            
            width=350,
            padding=30,
            bgcolor="#ffffff",
            border_radius=18,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=3,
                blur_radius=10,
                color=f"{color}40",
                offset=ft.Offset(0, 5)
            ),
            animate_scale=ft.Animation(300, "ease"),
            on_hover=animate_card_hover
        )

    def create_analysis_specific_card(self, title, subtitle, features, color, button_text, on_click_handler):
        """Crear una card de selección profesional y reutilizable para el tipo de análisis."""
        
        # Animación de hover
        def animate_card_hover(e):
            if e.data == "true":
                e.control.shadow.blur_radius = 20
                e.control.shadow.color = f"{color}40"
                e.control.scale = ft.transform.Scale(1.03)
            else:
                e.control.shadow.blur_radius = 6
                e.control.shadow.color = f"{color}26"
                e.control.scale = ft.transform.Scale(1)
            e.control.update()

        return ft.Container(
            content=ft.Column([
                # Título
                ft.Text(
                    title,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Subtítulo
                ft.Text(
                    subtitle,
                    size=16,
                    color="#495057",
                    text_align=ft.TextAlign.CENTER,
                    height=None
                ),
                
                ft.Divider(height=1, color="#eeeeee"),

                # Características
                ft.Container(
                    content=ft.Column([
                        *[ft.Row([
                            ft.Icon(name="check_circle_outline", color=self.colors['success'], size=18),
                            ft.Text(feature.replace("• ",""), size=15, expand=True)
                        ], spacing=12) for feature in features]
                    ], spacing=12),
                    margin=ft.margin.symmetric(vertical=25),
                    height=None,
                    expand=True  # Permite que las características ocupen el espacio disponible
                ),
                
                # Botón
                ft.ElevatedButton(
                    button_text,
                    width=320,
                    height=50,
                    bgcolor=color,
                    color="white", 
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation={"hovered": 10}
                    ),
                    on_click=on_click_handler
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25),  # Spacing aumentado proporcionalmente
            
            width=450,
            height=450,  # Altura aumentada proporcionalmente
            padding=35,
            bgcolor="#ffffff",
            border_radius=15,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=8,
                color=f"{color}30",
                offset=ft.Offset(0, 4)
            ),
            animate_scale=ft.Animation(300, "ease"),
            on_hover=animate_card_hover
        )

    def animate_logo_hover(self, e):
        """Animar logo al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.1
            e.control.rotate = 0.1
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.rotate = 0
        e.control.update()

    def select_analysis(self, analysis_type):
        """Seleccionar tipo de análisis"""
        self.tipo_analisis = analysis_type
        
        if self.modo_operacion == 'existente':
            self.show_main_dashboard()
        else:
            self.show_new_campaign_dashboard()

    def show_main_dashboard(self):
        """Mostrar dashboard principal para campaña existente"""
        try:
            from ui.flet_dashboard import MainDashboard
            dashboard = MainDashboard(self)
            dashboard.show()
        except Exception as e:
            logger.error(f"Error cargando dashboard: {e}")
            self.show_error(f"❌ Error cargando dashboard: {e}")

    def show_new_campaign_dashboard(self):
        """Mostrar dashboard para campaña nueva"""
        self.page.clean()
        
        # TODO: Implementar dashboard de campaña nueva
        placeholder = ft.Container(
            content=ft.Column([
                ft.Text(
                    "🚀 Dashboard - Campaña Nueva",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Dashboard en desarrollo...",
                    size=16,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.ElevatedButton(
                    "⬅️ Volver",
                    on_click=lambda e: self.show_analysis_selection()
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.page.add(placeholder)
        self.page.update()

    def logout(self):
        """Cerrar sesión"""
        self.current_user = None
        self.modo_operacion = None
        self.tipo_analisis = None
        self.show_login()


def main(page: ft.Page):
    """Función principal para Flet"""
    app = CallCenterApp()
    app.main(page)


if __name__ == "__main__":
    # Crear directorios necesarios
    Path("logs").mkdir(exist_ok=True)
    
    logger.info("Iniciando Call Center Dimensioner con Flet...")
    ft.app(target=main, view=ft.WEB_BROWSER, port=8502)