# Instacart + E-commerce Medallion ETL

Trabajo final — Ingeniería de Datos con Databricks.

ETL con arquitectura Medallion (Bronze → Silver → Golden) usando PySpark y Managed Identity, con despliegue CI/CD vía GitHub Actions.

## Fuentes de datos (capa Raw)

1. **Instacart Market Basket** (`orders.csv`, `order_products__train.csv`, `products.csv`)
2. **E-commerce Sales Prediction** (`Ecommerce_Sales_Prediction_Dataset.csv`)

## Arquitectura

_Pendiente: agregar diagrama de arquitectura (Raw → Bronze → Silver → Golden → PowerBI/Lakeview)._

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `datasets/` | Insumos del ETL (.csv) |
| `dashboard/` | Gráficos finales (.json, .png, .pbix) |
| `reversion/` | Scripts DROP para eliminar tablas y rutas |
| `.github/workflows/` | Pipeline CI/CD (dev → prod) |
| `seguridad/` | GRANTS, usuarios y grupos |
| `prepAmb/` | Preparación de ambiente (catalog, schemas, external location) |
| `proceso/` | Notebooks de ETL (PySpark) — se ejecutan en producción |
| `certificaciones/` | Certificaciones relacionadas |
| `evidencias/` | Capturas de ejecución correcta |

## Ejecución

_Pendiente: instrucciones de ejecución del workflow._
