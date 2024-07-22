import yaml
from abc import ABC, abstractmethod
from typing import Any, Optional
import os


class WidgetHandler(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass


class EnvVarWidgetHandler(WidgetHandler):
    def get(self, key) -> Optional[str]:
        return os.environ.get(key)


class DBUtilsHandler:
    def __init__(self, widget_handler: WidgetHandler):
        self.widgets = widget_handler()


def set_widget_values(config_path: str = ".databricks.local"):
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the YAML file
    yaml_path = os.path.join(project_root, config_path)

    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)


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
        except ImportError:
            print("WorkspaceClient is not available. Install `databricks-sdk`.")


initialize_spark_and_dbutils()

dbutils.widgets.text("HOI", "HAI")
print(dbutils.widgets.get("HOI"))

print(spark.table("system.access.audit").count())
