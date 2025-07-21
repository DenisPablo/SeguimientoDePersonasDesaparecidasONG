# 🧭 Sistema de Gestión de Casos de Personas Desaparecidas (Demo Portfolio)

Este proyecto es una aplicación web diseñada para ONGs que trabajan con casos de personas desaparecidas. Su objetivo es permitir el registro, seguimiento, y exportación de información relevante de forma organizada. El desarrollo tiene fines educativos y de portafolio personal.

---

## 🎯 Objetivos

### Objetivo General
Desarrollar un sistema local completo para la gestión de casos de personas desaparecidas, integrando funcionalidades avanzadas como mapeo geográfico, IA para envejecimiento facial y generación de reportes exportables.

### Objetivos Específicos
- Registrar personas desaparecidas y mantener una ficha actualizada.
- Permitir el seguimiento del caso a través de reportes y pistas.
- Localizar geográficamente avistamientos o pruebas.
- Generar imágenes estimadas con IA.
- Exportar los datos de forma organizada para su entrega a autoridades.

---

## 🧩 Funcionalidades Principales

### 👤 Gestión de Usuarios
- Registro e inicio de sesión de usuarios.
- Asociación de personas desaparecidas con usuarios.

### 🧍‍♂️ Gestión de Personas Desaparecidas
- Creación de ficha con foto original.
- Asociación de imagen estimada (envejecida) vía IA.
- Relación con múltiples reportes.

### 📑 Reportes
- Permite describir avances o novedades del caso.
- Vinculación a múltiples pistas o pruebas.

### 🧭 Pistas
- Detalles de cada pista (texto, ubicación, imágenes).
- Geolocalización mediante coordenadas.
- Múltiples imágenes por pista.

### 🗺️ Mapa Interactivo
- Visualización de ubicaciones relacionadas a las pistas.
- Utiliza Leaflet.js + OpenStreetMap.

### 🧠 Envejecimiento Facial por IA
- Generación de imagen estimada mediante API externa (DeepAI).
- Imagen almacenada en la base de datos como `foto_estimada`.

### 📤 Exportación de Casos
- Generación de PDF con:
  - Ficha de la persona.
  - Reportes y pistas asociadas.
  - Pistas con imágenes.
- Compresión automática en `.zip` para descarga.

---

## ⚙️ Tecnologías Utilizadas

| Componente              | Tecnología                             |
|------------------------|------------------------------------------|
| Backend                | Django (Python)                          |
| Base de Datos          | SQLite                                   |
| Frontend               | HTML + CSS /
