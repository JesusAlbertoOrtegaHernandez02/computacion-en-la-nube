#  Arquitectura Acoplada – Sistema de Almacenamiento de la Empresa

Este proyecto implementa una **arquitectura acoplada en AWS** para un sistema de gestión de inventario empresarial.  
Está basada en una aplicación **Flask** contenedorizada y desplegada mediante **ECS Fargate**, **DynamoDB** y **API Gateway**,  
con soporte de **CORS** y balanceo de tráfico mediante **Network Load Balancer (NLB)**.

---

## 🧭 Tabla de Contenidos
- [ Descripción General](#-descripción-general)
- [ Estructura del Proyecto](#-estructura-del-proyecto)
- [ Flujo de Despliegue](#️-flujo-de-despliegue)
- [ Endpoints de la API](#-endpoints-de-la-api)
- [ Pruebas desde PowerShell](#-pruebas-desde-powershell)
- [ Frontend (Interfaz CRUD)](#️-frontend-interfaz-crud)
- [ Notas Técnicas Importantes](#-notas-técnicas-importantes)
- [ Tecnologías Empleadas](#-tecnologías-empleadas)
- [ Autor](#-autor)
- [ Versión en Inglés](#-versión-en-inglés)

---

##  Descripción General

La arquitectura acoplada está diseñada para ejecutar la aplicación **Flask** dentro de un contenedor Docker gestionado por **Amazon ECS Fargate**, con los siguientes componentes:

| Servicio AWS | Función principal |
|---------------|------------------|
| **ECS Fargate** | Ejecuta la aplicación Flask dentro de un contenedor. |
| **ECR** | Almacena la imagen Docker del servicio. |
| **API Gateway** | Expone los endpoints REST públicamente. |
| **Network Load Balancer (NLB)** | Redirige las peticiones hacia ECS. |
| **DynamoDB** | Base de datos NoSQL donde se almacenan los productos. |
| **CloudFormation** | Automatiza la creación de toda la infraestructura. |

---

##  Estructura del Proyecto

```bash
acoplada/
├── app/
│   ├── main.py              # Lógica principal de Flask (CRUD)
│   ├── db.py                # Clase para interacción con DynamoDB
│   └── requirements.txt     # Dependencias del backend
│
├── Dockerfile               # Imagen Docker del servicio Flask
├── frontend.html            # Interfaz web CRUD
│
├── db_dynamodb.yml          # Stack CloudFormation para DynamoDB
├── ecr.yml                  # Stack CloudFormation para ECR
├── main.yml                 # Stack principal (ECS + API Gateway + NLB + CORS)
│
└── README.md                # Documentación del proyecto
