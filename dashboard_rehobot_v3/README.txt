# Dashboard Rehobot v3 – navegación por herramientas y edición

## Ejecutar
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```
Si no puedes activar el entorno:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Novedades
- Cada objetivo tiene una ruta visual secuencial de sus herramientas.
- Selector para abrir una herramienta a la vez (ABC, Slotting, Kanban; análisis de operaciones, POE, 5S; OWAS, tiempos, movimientos; Kardex, ubicaciones, ABC, conteo cíclico).
- Gráficas específicas por herramienta: radar 5S, distribución OWAS, tiempo por actividad, Sankey de secuencia, treemap ABC, evolución de saldos y tableros Kanban.
- Tablas editables en la aplicación; algunas permiten descargar el CSV editado.
- Indicadores antes/después editables y gráficas que se actualizan con los cambios de la sesión.
- Identidad de color individual para cada objetivo.
- Flujo de caja se mantiene como módulo consolidado.

## Límites importantes
La edición es de sesión: no altera el Excel fuente ni guarda cambios al cerrar la aplicación. Usa los botones de descarga CSV para conservar tablas editadas.
Algunas gráficas de ruta son esquemas de proceso, no planos a escala. Los datos OWAS se muestran según los registros disponibles en la hoja de desarrollo. La hoja de desarrollo económico del objetivo 4 y Resultados-Indicadores difieren en la devolución oportuna; se conserva 70% en el resumen de indicadores y debe validarse el 75% de la hoja económica.
