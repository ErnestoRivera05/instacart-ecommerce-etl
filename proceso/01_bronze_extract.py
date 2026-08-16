# Databricks notebook source
# =========================================================
# proceso / 01_bronze_extract.py
# Capa BRONZE - Extracción cruda desde Raw (Managed Identity)
# Proyecto: Instacart + E-commerce Medallion ETL
# =========================================================

# COMMAND ----------

# Parámetros generales
CATALOG = "instacart_ecommerce"
SCHEMA_BRONZE = "bronze"
RAW_PATH = "abfss://raw@adlssmartdata1208.dfs.core.windows.net/"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA_BRONZE}")

# COMMAND ----------

# 1. Ingesta: orders.csv (separador ; )
df_orders = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ";")
    .load(RAW_PATH + "orders.csv")
)

df_orders.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{SCHEMA_BRONZE}.orders"
)

print(f"orders: {df_orders.count()} filas cargadas a Bronze")

# COMMAND ----------

df_orders.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/orders"
).saveAsTable(f"{CATALOG}.{SCHEMA_BRONZE}.orders")

# COMMAND ----------

# DBTITLE 1,Cell 5
# 2. Ingesta: order_products__train.csv (separador ; )
df_order_products = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ";")
    .load(RAW_PATH + "order_products__train.csv")
)

df_order_products.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/order_products"
).saveAsTable(
    f"{CATALOG}.{SCHEMA_BRONZE}.order_products"
)

print(f"order_products: {df_order_products.count()} filas cargadas a Bronze")

# COMMAND ----------

df_order_products.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/order_products"
).saveAsTable(f"{CATALOG}.{SCHEMA_BRONZE}.order_products")

# COMMAND ----------

# DBTITLE 1,Cell 7
# 3. Ingesta: products.csv (separador ; )
df_products = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ";")
    .load(RAW_PATH + "products.csv")
)

df_products.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/products"
).saveAsTable(
    f"{CATALOG}.{SCHEMA_BRONZE}.products"
)

print(f"products: {df_products.count()} filas cargadas a Bronze")

# COMMAND ----------

df_products.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/products"
).saveAsTable(f"{CATALOG}.{SCHEMA_BRONZE}.products")

# COMMAND ----------

# DBTITLE 1,Cell 9
# 4. Ingesta: Ecommerce_Sales_Prediction_Dataset.csv
df_ecommerce = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(RAW_PATH + "Ecommerce_Sales_Prediction_Dataset.csv")
)

df_ecommerce.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/ecommerce_sales"
).saveAsTable(
    f"{CATALOG}.{SCHEMA_BRONZE}.ecommerce_sales"
)

print(f"ecommerce_sales: {df_ecommerce.count()} filas cargadas a Bronze")

# COMMAND ----------

df_ecommerce.write.format("delta").mode("overwrite").option(
    "path", "abfss://bronze@adlssmartdata1208.dfs.core.windows.net/ecommerce_sales"
).saveAsTable(f"{CATALOG}.{SCHEMA_BRONZE}.ecommerce_sales")

# COMMAND ----------

# 5. Verificación final
display(spark.sql(f"SHOW TABLES IN {CATALOG}.{SCHEMA_BRONZE}"))
