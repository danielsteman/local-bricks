from localbricks.main import initialize_spark_and_dbutils


def test_initialize_spark_and_dbutils():
    initialize_spark_and_dbutils()
    assert dbutils is not None, "dbutils should be initialized"
    assert spark is not None, "spark should be initialized"
    assert dbutils.widgets.get("pasta") == "rigatone"
    assert spark.table("system.compute.node_types").count() > 0
