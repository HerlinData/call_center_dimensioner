# 📞 Call Center Dimensioner

## 🎯 Descripción

Sistema de dimensionamiento inteligente para call centers telecom inbound. Aplicación web moderna desarrollada con **Flet** que permite a supervisores y gerentes realizar análisis precisos de capacidad basados en datos históricos reales.

## ✨ Características Principales

- 🎨 **Interfaz moderna** con colores corporativos
- 📊 **Análisis basado en datos reales** de SQL Server
- ⚡ **Múltiples tipos de análisis** (Básico, Intermedio, Avanzado)
- 🧮 **Motores de cálculo** (Erlang C + SimPy)
- 📈 **Visualizaciones interactivas** con Plotly
- 📄 **Exportación** a Excel con gráficos
- 🔒 **Sistema de autenticación** seguro

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar o descargar el proyecto
cd call_center_dimensioner

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus credenciales:
# ACCESS_KEY=tu_clave_segura
# DB_SERVER=tu_servidor_sql
# DB_DATABASE=tu_base_datos
# etc.
```

### 3. Ejecutar
```bash
# Opción 1: Script automático (recomendado)
python run_flet.py

# Opción 2: Directo
python main_flet.py

# Opción 3: Punto de entrada
python main.py
```

### 4. Acceder
- **URL**: http://localhost:8502
- **Login**: Tu ACCESS_KEY configurada en .env

## 🎨 Esquema de Colores

- **⚡ Análisis Básico**: Azul (#2196f3) - Velocidad y eficiencia
- **📊 Análisis Intermedio**: Verde (#4caf50) - Equilibrio y crecimiento  
- **🔬 Análisis Avanzado**: Morado (#9c27b0) - Ciencia y precisión
- **📊 Campaña Existente**: Terracota (#da7756) - Color corporativo
- **🚀 Campaña Nueva**: Naranja (#ff9800) - Energía e innovación

## 📁 Estructura del Proyecto

```
call_center_dimensioner/
├── main_flet.py              # ✨ Aplicación principal
├── run_flet.py               # 🚀 Script de inicio automático  
├── main.py                   # 🔗 Punto de entrada
├── ui/
│   └── flet_dashboard.py     # 📊 Dashboard principal
├── config/                   # ⚙️ Configuración y autenticación
│   ├── auth.py               # 🔐 Sistema de autenticación
│   ├── database.py           # 🗄️ Configuración BD
│   └── settings.py           # ⚙️ Configuración general
├── data/                     # 📊 Conectores y análisis
│   ├── sql_connector.py      # 🔌 Conexión SQL Server
│   └── data_analyzer.py      # 📈 Análisis de datos
├── engines/                  # 🧮 Motores de cálculo
│   └── erlang_calculator.py  # ⚡ Cálculos Erlang C + SimPy
├── reports/                  # 📄 Generación de reportes
├── logs/                     # 📝 Archivos de log
└── requirements.txt          # 📦 Dependencias
```

## 🗄️ Configuración de Base de Datos

### Estructura de Tabla Requerida
```sql
-- Tabla principal con 5 columnas mínimas
CREATE TABLE tu_tabla_call_center (
    usuarios VARCHAR(50),           -- Identificador del asesor
    fecha_hora DATETIME,           -- Timestamp completo
    fecha DATE,                    -- Fecha de la llamada
    tme INT,                       -- Tiempo de espera (segundos)
    tmo INT                        -- Tiempo de manejo (segundos)
);
```

### Variables de Entorno (.env)
```bash
# Autenticación
ACCESS_KEY=tu_clave_segura_aqui
JWT_SECRET_KEY=tu_clave_jwt_secreta

# Base de Datos
DB_SERVER=tu_servidor_sql
DB_DATABASE=tu_base_datos
DB_USERNAME=tu_usuario_sql
DB_PASSWORD=tu_password_seguro
DB_TABLE_NAME=tu_tabla_datos
DB_TRUSTED_CONNECTION=true
```

## 🎯 Tipos de Análisis

### ⚡ Análisis Básico (Erlang C)
- Cálculos instantáneos (< 1 segundo)
- Dimensionamiento preciso
- Ideal para análisis rápido

### 📊 Análisis Intermedio (SimPy)
- Simulaciones con abandonos
- Análisis más realista
- Tiempo: 2-5 segundos

### 🔬 Análisis Avanzado (SimPy + Validación)
- Validación automática
- Shrinkage detallado
- Múltiples escenarios
- Análisis más completo

## 📊 Escenarios de Dimensionamiento

| Escenario | Descripción | Uso Recomendado |
|-----------|------------|-----------------|
| **PROMEDIO** | Volumen promedio histórico | Dimensionamiento estándar |
| **HORA PICO** | Volumen máximo detectado | Cobertura completa |
| **CONSERVADOR** | Percentil 90 de volumen | Operaciones críticas |
| **OPTIMISTA** | Percentil 75 de volumen | Optimización de costos |

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flet'"
```bash
pip install flet>=0.21.0
```

### Error: Puerto 8502 ocupado
```bash
# Editar main_flet.py (última línea):
ft.app(target=main, view=ft.WEB_BROWSER, port=8503)
```

### Error: Conexión a base de datos
```bash
# Verificar configuración en .env
# Comprobar conectividad de red
# Validar credenciales SQL
```

### Error: Archivo .env no encontrado
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## 📈 Funcionalidades

### ✅ Implementadas
- 🔐 Sistema de autenticación seguro
- 🎯 Selección de modo (Campaña Existente/Nueva)
- ⚡ Selección de análisis (Básico/Intermedio/Avanzado)
- 📊 Dashboard principal con controles
- 📅 Configuración de fechas y parámetros
- 🎨 Interfaz visual con colores corporativos
- 🔔 Notificaciones (éxito/error/carga)
- 📊 Conexión automática a SQL Server

### 🚧 En Desarrollo
- 📈 Visualizaciones detalladas con Plotly
- 📄 Exportación completa de reportes
- 📊 Vista de resultados con tabs
- 🔬 Dashboard específico para campaña nueva

## 🏢 Contexto de Negocio

- **Sector**: Telecom
- **Tipo**: Call Centers Inbound  
- **Usuarios**: Supervisores y gerentes
- **Granularidad**: Análisis por intervalos de 15/30/60 minutos
- **Objetivo**: Dimensionamiento rápido y preciso basado en datos reales

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs: `tail -f logs/app.log`
2. Verificar configuración en `.env`
3. Comprobar conectividad a SQL Server
4. Validar estructura de tabla de datos

## 🎉 Beneficios

- ✅ **Toma de decisiones** basada en evidencia
- ⚡ **Análisis rápido** en lugar de cálculos manuales
- 📊 **Reportes automáticos** con justificaciones técnicas
- 💰 **Identificación de eficiencias** operativas
- 🎯 **Cumplimiento de SLA** optimizado
- 🎨 **Interfaz profesional** sin problemas de CSS

---

**Call Center Dimensioner** - Sistema profesional para optimización de operaciones telefónicas 📞✨