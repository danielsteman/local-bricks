import yaml
import os


spark = None
dbutils = None


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

    running_in_databricks = bool(os.getenv("DATABRICKS_RUNTIME_VERSION"))
    if running_in_databricks:
        return

    try:
        from databricks.connect import DatabricksSession

        spark = DatabricksSession.builder.serverless().getOrCreate()
    except ImportError:
        print("DatabricksSession is not available. Initializing local Spark.")
        from pyspark.sql import SparkSession

        spark = (
            SparkSession.builder.master("local[*]").appName("LocalSpark").getOrCreate()
        )

    try:
        from databricks.sdk import WorkspaceClient

        w = WorkspaceClient()
        dbutils = w.dbutils
        set_widget_values(dbutils)
    except ImportError:
        print("WorkspaceClient is not available. Install `databricks-sdk`.")


if not bool(os.getenv("DATABRICKS_RUNTIME_VERSION")):
    initialize_spark_and_dbutils()
