Sistema de Inventario de Poleras (Tkinter + SQLite)

por Maleza Felipe-Godoy-Fuenzalida Desarrollador


1. 📌 Descripción General

Aplicación de escritorio desarrollada en Python utilizando Tkinter para la interfaz gráfica y una base de datos (SQLite) para la persistencia de datos.

Permite:

Gestionar stock de poleras por modelo
Controlar tallas y ubicaciones (local / bodega)
Visualizar inventario en formato tipo Excel
Resumen automático por talla
Filtrar y buscar productos
Ajustar stock en tiempo real


2. 🧱 Arquitectura del Proyecto
musubi-hr-inventario/
│
├── main.py
├── db/
│   └── conexion.py
├── servicios/
│   └── inventario_servicios.py
├── ui/
│   ├── app.py
│   ├── tabla.py
│   ├── formulario.py
│   ├── resumen.py
│   └── state.py
3. 🔄 Flujo de la Aplicación
main.py
   ↓
crear_tablas()
   ↓
iniciar_app()
   ↓
UI (formulario + tabla + controles + resumen)
   ↓
servicios (lógica)
   ↓
base de datos
4. 📂 Descripción de Archivos
🔹 main.py

Punto de entrada del sistema.

def main():
    crear_tablas()
    iniciar_app()
🔹 db/conexion.py

Responsable de:

Crear base de datos
Crear tablas si no existen
🔹 servicios/inventario_servicios.py

Contiene la lógica de negocio:

Funciones principales:

agregar_stock()
obtener_stock()
eliminar_modelo()

Ejemplo:

def agregar_stock(modelo, categoria, talla, ubicacion, cantidad):
🔹 ui/state.py

Maneja el estado global de la app:

modelo_seleccionado = None
talla_seleccionada = None
categoria_actual = "Musica"
busqueda_modelo = ""
mostrar_sin_stock = False
🔹 ui/app.py

Orquesta toda la interfaz:

Responsabilidades:

Crear ventana principal
Definir layout
Conectar componentes
def actualizar_todo():
    cargar_tabla()
    cargar_resumen()
🔹 ui/formulario.py

Contiene:

1. Formulario superior
Agregar nuevas poleras
2. Control de stock
Buscar modelo
Ajustar stock (+ / -)
Eliminar modelo
🔹 ui/tabla.py

Componente más importante.

Responsable de:

Renderizar inventario tipo Excel
Mostrar stock por talla
Mostrar local (verde) / bodega (rojo)
Manejar selección de celdas
Características:
Scroll vertical
Header fijo
Expansión automática
Interacción con mouse
🔹 ui/resumen.py

Muestra:

Totales por talla
Separación local / bodega
Total general

Ejemplo:

M
Local: 13
Bodega: 6
Total: 19


5. 🎨 Diseño de Interfaz
Layout principal:
[ FORMULARIO SUPERIOR ]

[ TABLA INVENTARIO (EXPANDIBLE) ]

[ CONTROL DE STOCK ]

[ RESUMEN ]
6. ⚙️ Funcionalidades Clave
✔ Agregar stock

Desde formulario superior

✔ Modificar stock

Desde control inferior (+ / -)

✔ Selección de celda

Click en tabla:

Define modelo + talla activa
✔ Búsqueda en tiempo real

Filtra por nombre de modelo

✔ Eliminación

Elimina modelo completo

✔ Resumen automático

Se recalcula en cada cambio

7. 🚀 Rendimiento

Optimizado mediante:

Evitar recarga completa innecesaria
Uso de state global
Render controlado de widgets
Scroll con canvas

8. 📦 Empaquetado

Generado como .exe con:

pyinstaller --onefile --windowed --icon=icono.ico main.py


9. 🧠 Posibles Mejoras Futuras
Sistema de ventas (descontar stock)
Historial de movimientos
Exportación a Excel
Multiusuario
Alertas de stock bajo
Dashboard con gráficos

10. 🛠 Requisitos
Python 3.x
Tkinter (incluido)
SQLite (incluido)


11. 🧪 Uso Básico
Ejecutar aplicación
Agregar productos
Seleccionar celda
Ajustar stock
Consultar resumen
