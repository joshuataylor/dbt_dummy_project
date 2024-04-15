# dbt dummyproject

Dummy project for working with dbt, for use with the dbt-helpers plugin.

Steps:

1. Install Postgres, create a dummy database with the data from [postgres_data.sql](postgres_data.sql)
2. Edit `~/.config/dbt/profiles.yml`:

```yaml
config:
  send_anonymous_usage_stats: false
  use_experimental_parser: true
  partial_parse: true
  printer_width: 100
  static_parser: true
  # debug: true
  # fail_fast: true

dummy_project:
  target: 'full'
  outputs:
    full:
      type: postgres
      type: postgres
      host: 127.0.0.1
      user: postgres
      password: cheese123
      port: 5432
      dbname: dummyprojectlarge
      schema: public
      threads: 16
```

3. Install dbt:
3a. Use `mise`, then `poetry install`, there is a [pyproject.toml](pyproject.toml)
3b. Or setup a virtualenv with dbt `1.7.x`+

4. `dbt run`