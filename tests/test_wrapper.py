from localbricks import dbutils, spark


def test_from_import():
    assert dbutils is not None, "dbutils should be initialized"
    assert spark is not None, "spark should be initialized"
    assert dbutils.widgets.get("pasta") == "rigatone", "config should be readable"
    assert (
        spark.table("system.compute.node_types").count() > 0
    ), "expected at least 1 row"
