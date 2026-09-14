## **_Analisis de Incidencias Operativas en Turismo_**
#### **Tipo de Proyecto: Tecnológico con enfoque en Análisis de Datos**

## **Abstract**
El presente proyecto, “Reporte de Incidencias Operativas en una agencia de turismo receptiva”, tiene como objetivo analizar registros historicos de incidencias ocurridas durante la gestión y coordinacion de servicios turísticos. La motivación principal surge de la necesidad de transformar los registros operativos en información util que permita identificar situaciones recurrentes, detectar posibles puntos críticos, y contribuir a una gestión más eficiente de las operaciones.

Para ello, se trabajará con un dataset que contiene registros de una bitácora de incidencias operativas: incluyendo información relacionada con agencias, proveedores, servicios, referencias de *TourPlan* (sistema de software especializado para empresas turísticas), estados, tipos de incidencia e impacto operativo.

Los resultados estarán dirigidos principalmente a equipos de ***Operaciones y Reservas*** de agencias de turismo receptivas, y buscan aportar información que facilite la *identificación de problemas recurrentes* y la toma de decisiones basada en datos reales.

## ***CRISP-DM — Comprensión del negocio***

## **Contexto comercial y analitico: Fundamentación**

El proyecto se desarrolla en una agencia de turismo receptiva de la Patagonia, donde la coordinación de servicios, proveedores, agencias y pasajeros puede generar diversas situaciones operativas.

El análisis que proponemos busca identificar patrones, problemas recurrentes y puntos críticos a partir de una *bitácora historica* de incidencias, elaborada por el equipo Operativo durante la temporada 2025/26.

El enfoque será *inicialmente* descriptivo & exploratorio, analizando variables como *tipo de incidencia, servicio, proveedor, agencia, fecha e impacto*.        

Los resultados buscan aportar información para orientar esfuerzos operativos y revisar protocolos frente a situaciones recurrentes, especialmente aquellas relacionadas con cambios, cancelaciones y otros eventos que afectan directamente al volumen de trabajo del equipo.

## **Fuente de datos**
El dataset utilizado surge de un conjunto inicial de registros operativos, cuyo uso fue autorizado por la empresa para fines académicos. Sobre este archivo CSV inicial se realizó un proceso de transformación & anonimización, preservando su estructura y lógica, resguardando la informacion sensible.

## **Preguntas / Hipótesis a Resolver mediante el Análisis de Datos [Problemática / Necesidades]**

Entre las principales preguntas se plantean:

- ¿Qué tipos de incidencias son más frecuentes?
- ¿Qué servicios o proveedores concentran mayor cantidad de incidencias?
- ¿En qué períodos se registran más incidencias?
- ¿Qué impacto tienen estas situaciones?
- ¿Existen patrones recurrentes?

Hipótesis de trabajo:
*“Las incidencias operativas presentan patrones asociados a determinados servicios, proveedores y períodos de operación.”*

## **Objetivos generales y especificos**
Objetivo general

*Analizar los registros operativos de la temporada 2025/26 para identificar patrones y problemas recurrentes que permitan comprender el comportamiento del sector operativo de la empresa.*

Objetivos específicos

- Explorar y comprender la estructura del dataset.
- Detectar valores nulos, duplicados e inconsistencias.
- Analizar la distribución de las principales variables.
- Generar insights que contribuyan a la comprensión de las operaciones y sirvan como base para futuras mejoras en la gestión operativa.

## **Importación de datos**

|                           | Nuestro dataset                           |
| ------------------------- | ----------------------------------------- |
| **Origen**                | Bitácora de registros operativos          |
| **Período**               | Temporada 2025/26                         |
| **Formato**               | CSV                                       |
| **Fuente**                | Repositorio de GitHub                     |
| **Método de importación** | Pandas → `read_csv()`                     |
| **Tratamiento previo**    | Transformación y anonimización            |

