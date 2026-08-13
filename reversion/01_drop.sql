-- =========================================================
-- reversion / 01_drop.sql
-- Reversión: eliminar tablas y schemas del proyecto
-- Proyecto: Instacart + E-commerce Medallion ETL
-- =========================================================

USE CATALOG instacart_ecommerce;

-- 1. Eliminar tablas Bronze
DROP TABLE IF EXISTS bronze.orders;
DROP TABLE IF EXISTS bronze.order_products;
DROP TABLE IF EXISTS bronze.products;
DROP TABLE IF EXISTS bronze.ecommerce_sales;

-- 2. Eliminar tablas Silver
DROP TABLE IF EXISTS silver.order_detail;
DROP TABLE IF EXISTS silver.ecommerce_sales;

-- 3. Eliminar tablas Golden
DROP TABLE IF EXISTS golden.sales_summary;
DROP TABLE IF EXISTS golden.product_performance;

-- 4. Eliminar schemas (una vez vacíos)
DROP SCHEMA IF EXISTS bronze;
DROP SCHEMA IF EXISTS silver;
DROP SCHEMA IF EXISTS golden;

-- 5. Eliminar el catalog (una vez vacío)
DROP CATALOG IF EXISTS instacart_ecommerce;

-- =========================================================
-- Nota: las rutas físicas en el Data Lake (raw/bronze/silver/golden)
-- NO se eliminan con este script porque son externas (External Location).
-- Si se requiere borrar los archivos físicos, debe hacerse manualmente
-- desde el portal de Azure (Storage Account > Containers).
-- =========================================================
