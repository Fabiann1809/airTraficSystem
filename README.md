# Sistema de Control de Tráfico Aéreo (ATC)

Simulador de control de tráfico aéreo desarrollado como proyecto universitario de
**Estructuras de Datos**. Implementa 6 estructuras de datos desde cero en Python puro,
sin librerías externas, con interfaz gráfica Tkinter y modo consola CLI.

---

## Requisitos

- Python 3.10 o superior
- Tkinter (incluido en la instalación estándar de Python)
- Sin dependencias externas

---

## Ejecución

```bash
# Interfaz gráfica (Tkinter)
python main.py

# Modo consola (CLI)
python main.py --cli
```

---

## Arquitectura

El proyecto sigue una arquitectura en capas monolítica:

```
Presentation Layer  →  GUI (Tkinter) / CLI (terminal)
Application Layer   →  ATCOrchestrator (Facade)
Domain Layer        →  Entidades + Estructuras de datos
```

```
atc_project/
├── main.py                          # Punto de entrada
└── core/
    ├── application/
    │   └── atc_orchestrator.py      # Fachada principal del sistema
    ├── domain/
    │   ├── entities/                # Aircraft, Incident, Quadrant
    │   └── mechanisms/              # Las 6 estructuras de datos
    └── presentation/
        ├── terminal_interface.py    # Modo CLI
        └── gui/                     # Ventana principal y paneles
```

---

## Estructuras de datos implementadas

Todas implementadas manualmente, sin usar `collections.deque`, `queue.Queue`
ni ningún módulo de estructuras de datos de Python.

| Estructura           | Archivo              | Rol en el sistema                    |
|----------------------|----------------------|--------------------------------------|
| Array estático       | airfield_tracker.py  | Estado de las 4 pistas de aterrizaje |
| Cola FIFO            | landing_sequence.py  | Aviones en espera para aterrizar     |
| Pila LIFO            | incident_handler.py  | Gestión de emergencias activas       |
| Lista doble          | flight_path.py       | Waypoints del plan de vuelo          |
| Lista circular doble | airspace_scanner.py  | Ciclo de monitoreo de cuadrantes     |
| Lista simple         | event_log.py         | Log cronológico de eventos           |

---

## Entidades del dominio

| Entidad    | Campos principales                                              |
|------------|-----------------------------------------------------------------|
| `Aircraft` | flight_id, origin, destination, fuel_level (0-100), priority   |
| `Incident` | incident_id, severity_level (1-3), description, timestamp      |
| `Quadrant` | quadrant_id, name, aircraft_count                              |

> Un avión con `fuel_level < 20` se marca automáticamente como `priority = "emergency"`.

---

## Funcionalidades

| Operación                  | Descripción                                              |
|----------------------------|----------------------------------------------------------|
| Agregar avión a cola       | Enqueue en la cola FIFO, prioridad automática por fuel   |
| Aterrizar siguiente avión  | Dequeue + asignación a la primera pista libre            |
| Liberar pista              | Marca la pista como disponible nuevamente                |
| Reportar emergencia        | Push en la pila LIFO con ID autogenerado                 |
| Resolver emergencia        | Pop del incidente más reciente                           |
| Navegar plan de vuelo      | Avanzar, retroceder y reiniciar en la lista doble        |
| Ciclar radar               | Rotación infinita entre cuadrantes (lista circular)      |
| Ver log de eventos         | Recorrido unidireccional de la lista simple              |

---

## Interfaz gráfica

La ventana principal se divide en 3 columnas:

- **Izquierda:** estado de las 4 pistas (verde = libre, rojo = ocupada) + radar activo
- **Centro:** cola de espera FIFO + pila de emergencias LIFO
- **Derecha:** plan de vuelo con waypoints + log de eventos en tiempo real
- **Barra inferior:** último evento del log + estadísticas en vivo (pistas, cola, emergencias)

---

## Datos de prueba iniciales

Al iniciar el sistema se cargan automáticamente:

- **5 waypoints:** BOG-01, CLO-02, MDE-03, CTG-04, BAQ-05
- **3 aviones en cola:** AV001 (normal), AV002 (emergency, fuel=15), AV003 (normal)
- **1 emergencia activa:** Severidad 2 — "Fallo en tren de aterrizaje AV002"

---


