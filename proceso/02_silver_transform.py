# Databricks notebook source
# =========================================================
# proceso / 02_silver_transform.py
# Capa SILVER - Limpieza y transformación
# Proyecto: Instacart + E-commerce Medallion ETL
# =========================================================

from pyspark.sql.functions import col, trim, to_date, round as spark_round

# COMMAND ----------
CATALOG = "instacart_ecommerce"

spark.sql(f"USE CATALOG {CATALOG}")

# COMMAND ----------
# 1. Leer tablas Bronze
df_orders = spark.table(f"{CATALOG}.bronze.orders")
df_order_products = spark.table(f"{CATALOG}.bronze.order_products")
df_products = spark.table(f"{CATALOG}.bronze.products")
df_ecommerce = spark.table(f"{CATALOG}.bronze.ecommerce_sales")

# COMMAND ----------
# 2. Limpieza - Orders
df_orders_clean = (
    df_orders
    .dropDuplicates(["order_id"])
    .filter(col("order_id").isNotNull())
)

# COMMAND ----------
# 3. Limpieza - Order Products
df_order_products_clean = (
    df_order_products
    .dropDuplicates(["order_id", "product_id"])
    .filter(col("order_id").isNotNull() & col("product_id").isNotNull())
)

# COMMAND ----------
# 4. Limpieza - Products
df_products_clean = (
    df_products
    .dropDuplicates(["product_id"])
    .withColumn("product_name", trim(col("product_name")))
    .filter(col("product_id").isNotNull())
)

# COMMAND ----------
# 5. Detalle de pedidos: cruce Orders + Order Products + Products
df_order_detail = (
    df_order_products_clean
    .join(df_orders_clean, on="order_id", how="inner")
    .join(df_products_clean, on="product_id", how="inner")
    .select(
        "order_id",
        "product_id",
        "product_name",
        "user_id",
        "order_number",
        "order_dow",
        "order_hour_of_day",
        "add_to_cart_order",
        "reordered",
    )
)

df_order_detail.write.format("delta").mode("overwrite").option(
    "path", "abfss://silver@adlssmartdata1208.dfs.core.windows.net/order_detail"
).saveAsTable(f"{CATALOG}.silver.order_detail")

print(f"order_detail: {df_order_detail.count()} filas cargadas a Silver")

# COMMAND ----------
# 6. Limpieza - E-commerce Sales
df_ecommerce_clean = (
    df_ecommerce
    .dropDuplicates()
    .withColumn("Product_Category", trim(col("Product_Category")))
    .withColumn("Customer_Segment", trim(col("Customer_Segment")))
    .withColumn("Date", to_date(col("Date")))
    .withColumn("Price", spark_round(col("Price"), 2))
    .withColumn("Discount", spark_round(col("Discount"), 2))
    .withColumn("Marketing_Spend", spark_round(col("Marketing_Spend"), 2))
    .filter(col("Date").isNotNull())
)

df_ecommerce_clean.write.format("delta").mode("overwrite").option(
    "path", "abfss://silver@adlssmartdata1208.dfs.core.windows.net/ecommerce_sales"
).saveAsTable(f"{CATALOG}.silver.ecommerce_sales")

print(f"ecommerce_sales: {df_ecommerce_clean.count()} filas cargadas a Silver")

# COMMAND ----------
# 7. Verificación final
display(spark.sql(f"SHOW TABLES IN {CATALOG}.silver"))
