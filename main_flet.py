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
        """Mostrar selección de modo de campaña"""
        self.page.clean()
        
        # Contenido principal centrado con elementos de vida
        main_content = ft.Container(
            content=ft.Column([
                # Header profesional con vida
                ft.Container(
                    content=ft.Column([
                        # Ícono corporativo animado
                        ft.Container(
                            content=ft.Text(
                                "📊",
                                size=50,
                                text_align=ft.TextAlign.CENTER
                            ),
                            animate=1000,
                            on_hover=lambda e: self.animate_header_icon_hover(e)
                        ),
                        
                        # Título principal
                        ft.Text(
                            "Selecciona el Modo de Operación",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=self.colors['text'],
                            text_align=ft.TextAlign.CENTER
                        ),
                        
                        # Subtítulo
                        ft.Text(
                            "Elige el tipo de análisis para tu dimensionamiento",
                            size=16,
                            color=self.colors['text_secondary'],
                            text_align=ft.TextAlign.CENTER
                        ),
                        
                        # Línea separadora con acento
                        ft.Container(
                            width=80,
                            height=3,
                            bgcolor=self.colors['accent'],
                            border_radius=2,
                            margin=ft.margin.symmetric(vertical=25)
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10),
                    margin=ft.margin.only(bottom=40),
                    animate=800
                ),
                
                # Cards de selección con vida corporativa
                ft.Row([
                    # Campaña Existente
                    self.create_corporate_mode_card(
                        icon="📈",
                        title="Analizar Campaña Existente",
                        subtitle="Basado en datos históricos",
                        description="Utiliza información real de tu base de datos SQL Server para obtener dimensionamientos precisos y validados.",
                        features=[
                            "Análisis de datos históricos reales",
                            "Validación automática de modelos", 
                            "Múltiples escenarios basados en patrones",
                            "Comparación predicho vs real"
                        ],
                        button_text="Usar Datos Históricos",
                        card_color=self.colors['primary'],
                        on_click=lambda e: self.select_mode('existente')
                    ),
                    
                    # Campaña Nueva
                    self.create_corporate_mode_card(
                        icon="🚀",
                        title="Dimensionar Campaña Nueva",
                        subtitle="Para operaciones sin historial",
                        description="Diseña el dimensionamiento para una nueva campaña utilizando parámetros estimados y mejores prácticas.",
                        features=[
                            "Inputs manuales de volumen y TMO",
                            "Cálculos basados en teoría Erlang C",
                            "Escenarios optimista y conservador", 
                            "Recomendaciones para nueva operación"
                        ],
                        button_text="Nueva Campaña",
                        card_color=self.colors['secondary'],
                        on_click=lambda e: self.select_mode('nueva')
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40),
                
                # Footer informativo con vida
                ft.Container(
                    content=ft.Row([
                        ft.Icon("info", size=16, color=self.colors['accent']),
                        ft.Text(
                            "Ambos modos generan reportes profesionales exportables a Excel",
                            size=14,
                            color=self.colors['text_secondary'],
                            italic=True
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    margin=ft.margin.only(top=40),
                    animate=1200
                )
                
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.padding.all(40),
            bgcolor=self.colors['background']
        )
        
        # Botón logout moderno
        logout_btn = ft.Container(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon("logout", size=18, color=self.colors['text']),
                    ft.Text("Salir", size=14, color=self.colors['text'], weight=ft.FontWeight.W_500)
                ], spacing=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                border_radius=25,
                bgcolor=self.colors['surface'],
                border=ft.border.all(1, self.colors['accent']),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color="#00000008",
                    offset=ft.Offset(0, 2)
                ),
                animate=200,
                on_click=lambda e: self.logout(),
                ink=True
            ),
            alignment=ft.alignment.top_right,
            padding=25
        )
        
        # Layout final
        page_layout = ft.Stack([
            main_content,
            logout_btn
        ])
        
        self.page.add(page_layout)
        self.page.update()

    def create_mode_card(self, title, subtitle, features, color, on_click):
        """Crear card de selección de modo"""
        return ft.Container(
            content=ft.Column([
                # Título
                ft.Text(
                    title,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Subtítulo
                ft.Text(
                    subtitle,
                    size=14,
                    color="#495057",
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Características
                ft.Container(
                    content=ft.Column([
                        ft.Text("✅ Incluye:", weight=ft.FontWeight.BOLD, size=14),
                        *[ft.Text(feature, size=12) for feature in features]
                    ], spacing=5),
                    margin=ft.margin.symmetric(vertical=15)
                ),
                
                # Botón
                ft.ElevatedButton(
                    title.split()[0] + " " + ("Usar Datos Históricos" if "Existente" in title else "Nueva Campaña"),
                    width=280,
                    height=45,
                    bgcolor=color,
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation={"": 3, "hovered": 8}
                    ),
                    on_click=on_click
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15),
            
            width=320,
            padding=25,
            bgcolor="#ffffff",
            border_radius=15,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=f"{color}1a",  # 10% opacity
                offset=ft.Offset(0, 4)
            ),
            animate=300,
            on_hover=lambda e: self.animate_card_hover(e)
        )

    def create_corporate_mode_card(self, icon, title, subtitle, description, features, button_text, card_color, on_click):
        """Crear card corporativa con vida"""
        return ft.Container(
            content=ft.Column([
                # Header con ícono corporativo
                ft.Container(
                    content=ft.Column([
                        # Ícono animado
                        ft.Container(
                            content=ft.Text(
                                icon,
                                size=40,
                                text_align=ft.TextAlign.CENTER
                            ),
                            animate=600,
                            on_hover=lambda e: self.animate_card_icon_hover(e)
                        ),
                        
                        # Título principal
                        ft.Text(
                            title,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=self.colors['text'],
                            text_align=ft.TextAlign.CENTER
                        ),
                        
                        # Subtítulo con color corporativo
                        ft.Text(
                            subtitle,
                            size=14,
                            color=card_color,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Descripción
                ft.Container(
                    content=ft.Text(
                        description,
                        size=13,
                        color=self.colors['text_secondary'],
                        text_align=ft.TextAlign.CENTER
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Lista de características con estilo corporativo
                ft.Container(
                    content=ft.Column([
                        ft.Text("Características principales:", 
                               weight=ft.FontWeight.BOLD, 
                               size=14, 
                               color=card_color),
                        ft.Container(height=8),
                        *[ft.Row([
                            ft.Icon("check_circle", size=16, color=card_color),
                            ft.Text(feature, size=12, color=self.colors['text_secondary'])
                        ], spacing=8) for feature in features]
                    ], spacing=3),
                    padding=ft.padding.all(15),
                    bgcolor=f"{card_color}10",
                    border_radius=10,
                    border=ft.border.all(1, f"{card_color}40"),
                    margin=ft.margin.only(bottom=25)
                ),
                
                # Botón de acción corporativo
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Text(button_text, size=15, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=280,
                        height=45,
                        bgcolor=card_color,
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation={"": 3, "hovered": 8, "pressed": 1}
                        ),
                        on_click=on_click
                    ),
                    animate=300
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            
            # Estilo de la card corporativa
            width=350,
            padding=25,
            bgcolor="#ffffff",
            border_radius=15,
            border=ft.border.all(2, f"{card_color}30"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=f"{card_color}20",
                offset=ft.Offset(0, 4)
            ),
            animate=400,
            on_hover=lambda e: self.animate_corporate_card_hover(e, card_color)
        )

    def create_professional_mode_card(self, title, subtitle, description, features, button_text, on_click):
        """Crear card profesional de selección de modo"""
        return ft.Container(
            content=ft.Column([
                # Header de la card
                ft.Container(
                    content=ft.Column([
                        # Título principal
                        ft.Text(
                            title,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=self.colors['text'],
                            text_align=ft.TextAlign.CENTER
                        ),
                        
                        # Subtítulo
                        ft.Text(
                            subtitle,
                            size=14,
                            color="#6c757d",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Descripción
                ft.Container(
                    content=ft.Text(
                        description,
                        size=13,
                        color=self.colors['text_secondary'],
                        text_align=ft.TextAlign.CENTER
                    ),
                    margin=ft.margin.only(bottom=25)
                ),
                
                # Lista de características
                ft.Container(
                    content=ft.Column([
                        ft.Text("Características principales:", 
                               weight=ft.FontWeight.BOLD, 
                               size=14, 
                               color="#212529"),
                        ft.Container(height=10),
                        *[ft.Row([
                            ft.Icon("check_circle", size=16, color="#28a745"),
                            ft.Text(feature, size=12, color=self.colors['text_secondary'])
                        ], spacing=8) for feature in features]
                    ], spacing=3),
                    padding=ft.padding.all(15),
                    bgcolor="#f8f9fa",
                    border_radius=8,
                    border=ft.border.all(1, "#e9ecef"),
                    margin=ft.margin.only(bottom=25)
                ),
                
                # Botón de acción
                ft.ElevatedButton(
                    button_text,
                    width=280,
                    height=45,
                    bgcolor="#007bff",
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation={"": 2, "hovered": 4}
                    ),
                    on_click=on_click
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            
            # Estilo de la card profesional
            width=350,
            padding=25,
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(1, "#dee2e6"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#00000010",
                offset=ft.Offset(0, 2)
            )
        )

    def create_enhanced_mode_card(self, icon, title, subtitle, description, features, color, gradient_color, button_text, on_click):
        """Crear card de selección de modo mejorada"""
        return ft.Container(
            content=ft.Column([
                # Header de la card con ícono
                ft.Container(
                    content=ft.Column([
                        # Ícono grande
                        ft.Container(
                            content=ft.Text(
                                icon,
                                size=50,
                                text_align=ft.TextAlign.CENTER
                            ),
                            animate=800,
                            on_hover=lambda e: self.animate_card_icon_hover(e)
                        ),
                        
                        # Título principal
                        ft.Text(
                            title,
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                            text_align=ft.TextAlign.CENTER
                        ),
                        
                        # Subtítulo
                        ft.Text(
                            subtitle,
                            size=14,
                            color="#6c757d",
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_400
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Descripción
                ft.Container(
                    content=ft.Text(
                        description,
                        size=13,
                        color=self.colors['text_secondary'],
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_300
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Lista de características mejorada
                ft.Container(
                    content=ft.Column([
                        ft.Text("✨ Características principales:", 
                               weight=ft.FontWeight.BOLD, 
                               size=14, 
                               color=color),
                        ft.Container(height=8),  # Spacer
                        *[ft.Container(
                            content=ft.Text(feature, size=12, color="#495057"),
                            margin=ft.margin.only(bottom=4)
                        ) for feature in features]
                    ], spacing=2),
                    padding=ft.padding.all(15),
                    bgcolor=gradient_color,
                    border_radius=10,
                    border=ft.border.all(1, f"{color}30"),
                    margin=ft.margin.only(bottom=25)
                ),
                
                # Botón de acción principal
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Text(button_text, size=15, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=300,
                        height=50,
                        bgcolor=color,
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation={"": 4, "hovered": 12, "pressed": 2},
                            animation_duration=200
                        ),
                        on_click=on_click
                    ),
                    animate=300
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8),
            
            # Estilo de la card mejorada
            width=380,
            padding=30,
            bgcolor="#ffffff",
            border_radius=18,
            border=ft.border.all(2, f"{color}20"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=f"{color}15",
                offset=ft.Offset(0, 8)
            ),
            animate=400,
            on_hover=lambda e: self.animate_enhanced_card_hover(e, color)
        )

    def animate_card_hover(self, e):
        """Animar card al hover"""
        if e.data == "true":  # Mouse enter
            e.control.elevation = 12
            e.control.scale = 1.02
        else:  # Mouse leave
            e.control.elevation = 4
            e.control.scale = 1.0
        e.control.update()

    def animate_logo_hover(self, e):
        """Animar logo al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.1
            e.control.rotate = 0.1
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.rotate = 0
        e.control.update()

    def animate_icon_hover(self, e):
        """Animar ícono al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.2
            e.control.rotate = 0.2
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.rotate = 0
        e.control.update()

    def animate_card_icon_hover(self, e):
        """Animar ícono de card al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.3
        else:  # Mouse leave
            e.control.scale = 1.0
        e.control.update()

    def animate_enhanced_card_hover(self, e, color):
        """Animar card mejorada al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.03
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=f"{color}25",
                offset=ft.Offset(0, 12)
            )
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=f"{color}15",
                offset=ft.Offset(0, 8)
            )
        e.control.update()

    def animate_header_icon_hover(self, e):
        """Animar ícono del header al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.2
            e.control.rotate = 0.1
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.rotate = 0
        e.control.update()

    def animate_corporate_card_hover(self, e, color):
        """Animar card corporativa al hover"""
        if e.data == "true":  # Mouse enter
            e.control.scale = 1.02
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=f"{color}30",
                offset=ft.Offset(0, 8)
            )
        else:  # Mouse leave
            e.control.scale = 1.0
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=f"{color}20",
                offset=ft.Offset(0, 4)
            )
        e.control.update()

    def select_mode(self, mode):
        """Seleccionar modo de operación"""
        self.modo_operacion = mode
        self.show_analysis_selection()

    def show_analysis_selection(self):
        """Mostrar selección de tipo de análisis"""
        self.page.clean()
        
        tipo_campana = "Campaña Existente" if self.modo_operacion == 'existente' else "Campaña Nueva"
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "🎯 Selecciona el Tipo de Análisis",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors['text'],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    f"Para tu {tipo_campana}",
                    size=16,
                    color="#495057",
                    text_align=ft.TextAlign.CENTER
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=40
        )
        
        # Cards de análisis en fila
        cards_row = ft.Row([
            # Análisis Básico
            self.create_analysis_card(
                title="⚡ Análisis Básico",
                subtitle="Dimensionamiento rápido con Erlang C",
                features=[
                    "• Cálculos instantáneos (< 1 seg)",
                    "• Dimensionamiento preciso",
                    "• Resultados inmediatos", 
                    "• Ideal para análisis rápido"
                ],
                color=self.colors['primary'],
                analysis_type='basico'
            ),
            
            # Análisis Intermedio
            self.create_analysis_card(
                title="📊 Análisis Intermedio", 
                subtitle="Simulación con abandonos incluidos",
                features=[
                    "• Simulaciones con SimPy",
                    "• Incluye abandonos de llamadas",
                    "• Análisis más realista",
                    "• Tiempo: 2-5 segundos"
                ],
                color=self.colors['secondary'],
                analysis_type='intermedio'
            ),
            
            # Análisis Avanzado
            self.create_analysis_card(
                title="🔬 Análisis Avanzado",
                subtitle="Shrinkage + validación automática", 
                features=[
                    "• Validación automática",
                    "• Incluye shrinkage detallado",
                    "• Múltiples escenarios",
                    "• Análisis más completo"
                ],
                color=self.colors['accent'],
                analysis_type='avanzado'
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20)
        
        # Sidebar con información actual
        sidebar = ft.Container(
            content=ft.Column([
                ft.Text("📋 Configuración Actual", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(f"🎯 {tipo_campana}", color="white"),
                    bgcolor="#0d6efd",
                    padding=10,
                    border_radius=8
                ),
                ft.Divider(),
                ft.ElevatedButton(
                    "⬅️ Cambiar Tipo",
                    width=200,
                    on_click=lambda e: self.show_mode_selection()
                ),
                ft.ElevatedButton(
                    "🚪 Cerrar Sesión", 
                    width=200,
                    bgcolor="#6c757d",
                    color="white",
                    on_click=lambda e: self.logout()
                )
            ], spacing=15),
            width=220,
            padding=20,
            bgcolor="#ffffff",
            border_radius=10
        )
        
        # Layout principal
        main_row = ft.Row([
            ft.Container(cards_row, expand=True),
            sidebar
        ], spacing=20)
        
        main_content = ft.Column([
            header,
            ft.Container(main_row, padding=ft.padding.symmetric(horizontal=20), expand=True)
        ], expand=True)
        
        self.page.add(main_content)
        self.page.update()

    def create_analysis_card(self, title, subtitle, features, color, analysis_type):
        """Crear card de selección de análisis"""
        return ft.Container(
            content=ft.Column([
                # Título
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Subtítulo
                ft.Text(
                    subtitle,
                    size=13,
                    color="#495057",
                    text_align=ft.TextAlign.CENTER
                ),
                
                # Características
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{title.split()[0]} Características:", weight=ft.FontWeight.BOLD, size=12),
                        *[ft.Text(feature, size=11) for feature in features]
                    ], spacing=3),
                    margin=ft.margin.symmetric(vertical=12)
                ),
                
                # Botón
                ft.ElevatedButton(
                    f"{title.split()[0]} Usar {title.split()[1]} {title.split()[2]}",
                    width=220,
                    height=40,
                    bgcolor=color,
                    color="white", 
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation={"": 2, "hovered": 6}
                    ),
                    on_click=lambda e: self.select_analysis(analysis_type)
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12),
            
            width=260,
            padding=20,
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=f"{color}26",  # 15% opacity
                offset=ft.Offset(0, 3)
            ),
            animate=250,
            on_hover=lambda e: self.animate_card_hover(e)
        )

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