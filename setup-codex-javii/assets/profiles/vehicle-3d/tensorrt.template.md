# TensorRT: {{PROJECT_NAME}}

## Goal

Optimizar el modelo ONNX validado con TensorRT para inferencia batch 1.

## Inputs

- Modelo ONNX validado.
- Shapes de entrada.
- Precision objetivo.
- Dataset o muestras para calibracion si aplica.

## Commands

Registrar comandos de build, conversion y validacion.

## Validation

Comparar salida TensorRT contra ONNX y revisar latencia estable.

## Risks

Registrar plugins necesarios, operadores no soportados, degradacion numerica o memoria insuficiente.

