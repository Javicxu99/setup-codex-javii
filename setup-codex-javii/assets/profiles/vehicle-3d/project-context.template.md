# Vehicle 3D Project Context: {{PROJECT_NAME}}

- Date: {{DATE}}
- Profile: {{PROFILE}}
- Primary language: {{PRIMARY_LANGUAGE}}

## Overview

Sistema de deteccion 3D de vehiculos basado solo en camaras.

## Objective

Entrenar, exportar, optimizar y desplegar un baseline de deteccion 3D camera-only para NVIDIA Jetson.

## Success Criteria

- Baseline entrenable en servidor.
- Salida por instancia: clase, score, caja 3D, posicion, dimensiones y orientacion.
- Exportacion temprana y validada a ONNX.
- Optimizacion TensorRT validada.
- Inferencia batch 1 con latencia estable.
- Despliegue realista en Jetson.

## Constraints

- No usar LiDAR como dependencia base.
- No depender de metricas offline como unica prueba de exito.
- Evitar arquitecturas SOTA si bloquean ONNX, TensorRT o Jetson.
- Mantener trazabilidad de datasets, pesos, configs y resultados.

## Architecture

Documentar pipeline en `docs/architecture.md`: datos, entrenamiento, evaluacion, exportacion ONNX, TensorRT y despliegue Jetson.

## Inputs

- Imagenes de camaras.
- Calibracion disponible.
- Anotaciones 3D o conversiones documentadas.

## Outputs

Por instancia:

- clase
- score de confianza
- caja 3D
- posicion
- dimensiones
- orientacion

## Reproducibility

Registrar dataset, split, versiones, seeds, configuraciones, checkpoints y comandos.

## Deployment

El despliegue objetivo es NVIDIA Jetson con batch 1, TensorRT y latencia estable.

## Risks

- Clases con pocos datos o baja calidad.
- Operadores no exportables a ONNX.
- Operadores no soportados o lentos en TensorRT.
- Diferencias numericas entre PyTorch, ONNX y TensorRT.
- Latencia inestable en Jetson.

## Current Status

Completar con el estado real antes de iniciar cambios importantes.

