# Sistema de Control de Tráfico Aéreo (ATC)

## Descripción
Simulador de control de tráfico aéreo que demuestra el uso de 6 estructuras
de datos implementadas manualmente en Python puro.

## Requisitos
- Python 3.10 o superior
- Tkinter (incluido en la instalación estándar de Python)
- Sin dependencias externas

## Ejecución
```bash
python main.py          # Interfaz gráfica (Tkinter)
python main.py --cli    # Modo consola (CLI)
```

## Estructuras de datos implementadas
| Estructura           | Archivo              | Rol en el sistema                         |
|----------------------|----------------------|-------------------------------------------|
| Array estático       | airfield_tracker.py  | Estado de las 4 pistas de aterrizaje      |
| Cola FIFO            | landing_sequence.py  | Aviones en espera para aterrizar          |
| Pila LIFO            | incident_handler.py  | Comandos de emergencia                    |
| Lista doble          | flight_path.py       | Waypoints del plan de vuelo               |
| Lista circular doble | airspace_scanner.py  | Monitoreo de cuadrantes de radar          |
| Lista simple         | event_log.py         | Log cronológico de eventos                |

## Operaciones disponibles
- Agregar avión a cola (fuel < 20 se marca automáticamente como emergencia)
- Aterrizar el siguiente avión y asignarle una pista libre
- Reportar y resolver emergencias (LIFO)
- Navegar waypoints del plan de vuelo en ambas direcciones
- Ciclar entre cuadrantes del radar
- Consultar log de eventos del sistema
