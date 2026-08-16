# Instacart + E-commerce Medallion ETL

Trabajo final — Ingeniería de Datos con Databricks.

ETL con arquitectura Medallion (Bronze → Silver → Golden) usando PySpark y Managed Identity, con despliegue CI/CD vía GitHub Actions hacia dos ambientes (desarrollo y producción) en Databricks Premium con Unity Catalog.

## Fuentes de datos (capa Raw)

1. **Instacart Market Basket** (`orders.csv`, `order_products__train.csv`, `products.csv`)
2. **E-commerce Sales Prediction** (`Ecommerce_Sales_Prediction_Dataset.csv`)

## Arquitectura

Ver `evidencias/arquitectura.png`.

Flujo: Fuentes → Azure Data Lake Storage Gen2 (raw, vía Managed Identity) → Databricks Unity Catalog (Bronze → Silver → Golden, PySpark, cluster `ClusterSD`) → Dashboard (Lakeview) / GitHub Actions (CI/CD dev → prod).

## Infraestructura

- Azure Data Lake Storage Gen2 con Hierarchical Namespace habilitado
- Access Connector for Azure Databricks (Managed Identity) con rol Storage Blob Data Contributor
- 4 External Locations (raw, bronze, silver, golden)
- Unity Catalog: catalog `instacart_ecommerce`, schemas `bronze`, `silver`, `golden`
- 2 Databricks Workspaces (Premium, Hybrid): desarrollo y producción, compartiendo el mismo metastore
- Cluster classic `ClusterSD` en cada workspace

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `datasets/` | Insumos del ETL (.csv) |
| `dashboard/` | Dashboard exportado (PDF) con KPIs y visualizaciones sobre la capa Golden |
| `reversion/` | Script DROP para eliminar catalog, schemas y tablas |
| `.github/workflows/` | Pipeline CI/CD: despliega notebooks y ejecuta el workflow en Databricks según la rama (dev/main) |
| `seguridad/` | GRANTS sobre catalog y schemas |
| `prepAmb/` | Script de preparación de ambiente (catalog + schemas) |
| `proceso/` | Notebooks del ETL en PySpark: `01_bronze_extract`, `02_silver_transform`, `03_golden_load` |
| `certificaciones/` | Certificaciones relacionadas al curso |
| `evidencias/` | Capturas de ejecución del workflow (GitHub Actions y Databricks), servicios aprovisionados en Azure, y diagrama de arquitectura |

## ETL — Medallion

1. **Bronze** (`01_bronze_extract.py`): ingesta cruda de los 4 CSVs desde `raw` hacia tablas Delta en el schema `bronze`, sin transformar.
2. **Silver** (`02_silver_transform.py`): limpieza de duplicados y nulos, cruce de `orders` + `order_products` + `products` en `order_detail`, limpieza de tipos en `ecommerce_sales`.
3. **Golden** (`03_golden_load.py`): modelo final para consumo — `sales_summary` (ventas por categoría y segmento) y `product_performance` (top productos por pedidos y tasa de recompra).

## CI/CD

El workflow (`.github/workflows/`) se dispara con cada push a las ramas `dev` o `main`:

- **Push a `dev`** → despliega los notebooks y ejecuta el workflow en el workspace de **desarrollo**
- **Push/merge a `main`** → despliega los notebooks y ejecuta el workflow en el workspace de **producción**

En ambos casos: crea (o reemplaza) el Job `WF_Instacart_Ecommerce_ETL`, usa el cluster classic existente `ClusterSD`, ejecuta las 3 tareas encadenadas (bronze → silver → golden) y monitorea hasta su finalización.

## Dashboard

Construido en Databricks Lakeview sobre las tablas Golden. Incluye KPIs de ingresos y unidades vendidas, ventas por categoría, distribución por segmento de cliente y el top 10 de productos más pedidos. Exportado como PDF en `dashboard/`.
