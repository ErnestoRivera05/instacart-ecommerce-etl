-- =========================================================
-- prepAmb / 01_ambiente.sql
-- Preparación de ambiente: Catalog + Schemas (Medallion)
-- Proyecto: Instacart + E-commerce Medallion ETL
-- =========================================================

-- 1. Crear el Catalog principal del proyecto
CREATE CATALOG IF NOT EXISTS instacart_ecommerce
COMMENT 'Catalog del proyecto final - ETL Medallion (Instacart + E-commerce)';

-- 2. Crear los Schemas de cada capa Medallion
CREATE SCHEMA IF NOT EXISTS instacart_ecommerce.bronze
COMMENT 'Capa Bronze - datos crudos extraídos de la raw sin transformar';

CREATE SCHEMA IF NOT EXISTS instacart_ecommerce.silver
COMMENT 'Capa Silver - datos limpios y transformados';

CREATE SCHEMA IF NOT EXISTS instacart_ecommerce.golden
COMMENT 'Capa Golden - modelo final listo para consumo (dashboards/BI)';

-- 3. Verificación rápida
SHOW SCHEMAS IN instacart_ecommerce;
