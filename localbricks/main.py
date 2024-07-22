import yaml
import builtins


def set_widget_values(
    dbutils, config_path: str = ".databricks.local", namespace: str = "default"
) -> None:
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)

    scoped_data = data.get(namespace, {})

    for key, value in scoped_data.items():
        dbutils.widgets.text(key, value)


def initialize_spark_and_dbutils():
    global spark
    global dbutils

    if "spark" not in locals() and "spark" not in globals():
        try:
            from databricks.connect import DatabricksSession

            spark = DatabricksSession.builder.serverless().getOrCreate()
        except ImportError:
            print("DatabricksSession is not available. Initializing local Spark.")
            from pyspark.sql import SparkSession

            spark = (
                SparkSession.builder.master("local[*]")
                .appName("LocalSpark")
                .getOrCreate()
            )

    if "dbutils" not in locals() and "dbutils" not in globals():
        try:
            from databricks.sdk import WorkspaceClient

            w = WorkspaceClient()
            dbutils = w.dbutils
            set_widget_values(dbutils)
        except ImportError:
            print("WorkspaceClient is not available. Install `databricks-sdk`.")

    builtins.spark = spark
    builtins.dbutils = dbutils
