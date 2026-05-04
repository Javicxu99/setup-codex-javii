# {{PROJECT_NAME}}

Proyecto Codex con perfil `vehicle-3d`: deteccion 3D camera-only de vehiculos.

## Mision

Construir un sistema entrenable, exportable, optimizable y desplegable en NVIDIA Jetson para deteccion 3D de vehiculos usando solo camaras.

## Reglas clave

- No usar LiDAR como dependencia base.
- No basta con buenas metricas offline: el exito exige ejecucion real en Jetson.
- Priorizar reproducibilidad, trazabilidad, latencia estable y despliegue.
- No elegir arquitectura solo por SOTA si complica ONNX, TensorRT o Jetson.
- Exportar temprano a ONNX y validar antes de avanzar a TensorRT.
- Si ONNX falla, no seguir a TensorRT hasta resolverlo.
- Trabajar con batch 1 como restriccion de despliegue.
- Si una clase tiene pocos datos o mala calidad, reportarlo como riesgo.

## Clases objetivo

- coche
- furgoneta
- camion
- autobus
- moto
- remolque/trailer

## Salida por instancia

- clase
- score de confianza
- caja 3D
- posicion
- dimensiones
- orientacion

## Validacion

- Entrenamiento reproducible en servidor.
- Evaluacion trazable por clase.
- Exportacion ONNX validada.
- Optimizacion TensorRT validada.
- Inferencia batch 1 comprobada en Jetson o entorno equivalente.

## Respuesta

Responder con resumen, archivos tocados, validacion ejecutada, riesgos de datos/despliegue y siguiente paso tecnico.

