# Databricks notebook source
# =========================================================
# proceso / 03_golden_load.py
# Capa GOLDEN - Modelo final para consumo (dashboards/BI)
# Proyecto: Instacart + E-commerce Medallion ETL
# =========================================================

from pyspark.sql.functions import sum as spark_sum, avg, count, round as spark_round

# COMMAND ----------
CATALOG = "instacart_ecommerce"

spark.sql(f"USE CATALOG {CATALOG}")

# COMMAND ----------
# 1. Leer tablas Silver
df_ecommerce = spark.table(f"{CATALOG}.silver.ecommerce_sales")
df_order_detail = spark.table(f"{CATALOG}.silver.order_detail")

# COMMAND ----------
# 2. Golden: sales_summary
# Resumen de ventas por categoría de producto y segmento de cliente
df_sales_summary = (
    df_ecommerce
    .groupBy("Product_Category", "Customer_Segment")
    .agg(
        spark_sum("Units_Sold").alias("total_units_sold"),
        spark_round(spark_sum((df_ecommerce.Price - df_ecommerce.Discount) * df_ecommerce.Units_Sold), 2).alias("total_revenue"),
        spark_round(avg("Price"), 2).alias("avg_price"),
        spark_round(spark_sum("Marketing_Spend"), 2).alias("total_marketing_spend"),
    )
    .orderBy(spark_sum("Units_Sold").desc())
)

df_sales_summary.write.format("delta").mode("overwrite").option(
    "path", "abfss://golden@adlssmartdata1208.dfs.core.windows.net/sales_summary"
).saveAsTable(f"{CATALOG}.golden.sales_summary")

print(f"sales_summary: {df_sales_summary.count()} filas cargadas a Golden")

# COMMAND ----------
# 3. Golden: product_performance
# Top productos por número de pedidos y tasa de recompra
df_product_performance = (
    df_order_detail
    .groupBy("product_id", "product_name")
    .agg(
        count("order_id").alias("total_orders"),
        spark_round(avg("reordered"), 2).alias("reorder_rate"),
    )
    .orderBy(count("order_id").desc())
)

df_product_performance.write.format("delta").mode("overwrite").option(
    "path", "abfss://golden@adlssmartdata1208.dfs.core.windows.net/product_performance"
).saveAsTable(f"{CATALOG}.golden.product_performance")

print(f"product_performance: {df_product_performance.count()} filas cargadas a Golden")

# COMMAND ----------
# 4. Verificación final
display(spark.sql(f"SHOW TABLES IN {CATALOG}.golden"))

# COMMAND ----------
# 5. Vista rápida de resultados
display(df_sales_summary.limit(10))

# COMMAND ----------
display(df_product_performance.limit(10))
