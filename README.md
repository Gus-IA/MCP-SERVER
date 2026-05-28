# 📘 Introduction to Model Context Protocol (MCP)

Este repositorio contiene apuntes y resumen del curso **Introduction to Model Context Protocol**, creado por Anthropic.

👉 Curso original: https://anthropic.skilljar.com/introduction-to-model-context-protocol

---

## 🧠 Descripción

El **Model Context Protocol (MCP)** es un estándar abierto que permite conectar modelos de lenguaje con herramientas externas, APIs y fuentes de datos de forma estructurada, segura y escalable.

Su objetivo es simplificar la integración entre modelos de IA y sistemas externos mediante una arquitectura unificada.

---

## 🚀 Contenidos del curso

### 🔌 ¿Qué es MCP y por qué existe?
- Estándar para integrar LLMs con herramientas externas
- Reduce el problema de múltiples integraciones (N × M)
- Mejora la escalabilidad de sistemas basados en IA

### 🏗️ Arquitectura MCP
- **MCP Host**: aplicación principal que usa el modelo
- **MCP Client**: intermediario de comunicación
- **MCP Server**: expone herramientas, recursos y prompts

### 🧩 Componentes principales
- **Tools**: funciones que el modelo puede ejecutar
- **Resources**: datos accesibles para el modelo
- **Prompts**: instrucciones reutilizables

### 🔄 Flujo de comunicación
- El usuario realiza una petición
- El cliente MCP gestiona la solicitud
- El servidor responde con herramientas o datos
- El modelo genera la respuesta final

### 📡 Comunicación
- Basado en JSON-RPC
- Soporta diferentes mecanismos de transporte
- Permite comunicación estructurada entre cliente y servidor

---

## 🎯 Objetivo del MCP

- Estandarizar la integración de herramientas en LLMs
- Facilitar el acceso a datos externos
- Permitir arquitecturas modulares y escalables
- Mejorar la interoperabilidad entre sistemas de IA

---

## 🧠 Conceptos clave

- Model Context Protocol (MCP)
- Tool calling
- Arquitectura cliente-servidor
- Context injection
- Integración de herramientas en LLMs

---

## 📌 Requisitos

- Conocimientos básicos de:
  - APIs REST
  - JSON
  - Programación básica (Python o JavaScript recomendado)

---

## 📚 Recursos

- Curso oficial: https://anthropic.skilljar.com/introduction-to-model-context-protocol  
- Documentación MCP (Anthropic)

---

## ⚠️ Nota

Este repositorio es únicamente educativo y contiene un resumen personal del curso. No incluye material oficial de Anthropic.
