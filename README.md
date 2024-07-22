# local-bricks

Experimental tools with databricks serverless sessions for local development of code that should run on databricks.

## Local config

`./.databricks_local.yaml` is the default config file path and expects a `default` namespace. This can't be changed at the moment.

```yaml
default:
  pasta: rigatone
```

These key values will be injected in `dbutils.widgets` so you can test parameterized notebooks locally.

```py
initialize_spark_and_dbutils()
dbutils.widgets.get("pasta")

>>> 'rigatone'
```
