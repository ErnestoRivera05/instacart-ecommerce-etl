-- =========================================================
-- seguridad / 01_grants.sql
-- Seguridad: permisos sobre catalog, schemas y tablas
-- Proyecto: Instacart + E-commerce Medallion ETL
-- =========================================================

USE CATALOG instacart_ecommerce;

-- 1. Permisos a nivel de Catalog
-- Reemplazar 'cristiansana1@outlook.com' por el usuario/grupo real que necesite acceso
GRANT USE CATALOG ON CATALOG instacart_ecommerce TO `cristiansana1@outlook.com`;

-- 2. Permisos a nivel de Schema
GRANT USE SCHEMA ON SCHEMA bronze TO `cristiansana1@outlook.com`;
GRANT USE SCHEMA ON SCHEMA silver TO `cristiansana1@outlook.com`;
GRANT USE SCHEMA ON SCHEMA golden TO `cristiansana1@outlook.com`;

-- 3. Permisos de lectura sobre la capa Golden (consumo de dashboards/BI)
GRANT SELECT ON SCHEMA golden TO `cristiansana1@outlook.com`;

-- 4. Permisos de lectura/escritura sobre Bronze y Silver (procesos ETL)
GRANT SELECT, MODIFY ON SCHEMA bronze TO `cristiansana1@outlook.com`;
GRANT SELECT, MODIFY ON SCHEMA silver TO `cristiansana1@outlook.com`;

-- =========================================================
-- Nota: en un entorno real se recomienda crear un grupo
-- (ej. "data_engineers") en Microsoft Entra ID y asignar
-- los GRANTS al grupo en lugar de a usuarios individuales.
-- =========================================================
