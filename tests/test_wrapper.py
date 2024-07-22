from serverless.src.main import initialize_spark_and_dbutils


def test_initialize_spark_and_dbutils():
    initialize_spark_and_dbutils()
    assert dbutils is not None, "dbutils should be initialized"
    assert spark is not None, "spark should be initialized"
    print(dbutils.widgets)
    print(spark.table("system.workflow.jobs").count())


initialize_spark_and_dbutils()
print(dbutils.widgets)
