## Strava Modern Data Stack
This is a project used to analyse my strava data using the modern data stack

## Project Inspriation
Please check out the other amazing projects that inspired me and this project
- https://github.com/matsonj/nba-monte-carlo
- https://github.com/dagster-io/mdsfest-opensource-mds

# Run Locally
- Set `PYTHONPATH` environment variable


## TODO
- [ ] Need to build out the datalake with DuckDB to start with.
    - [ ] Going to need to research the Dagster Resource/IO Manager





- [ ] Add precommit hooks for "Your code has been rated at xxx/10"
- [x] Build out internal library
    - [x] Create the handler for strava
    - [ ] __init__.py add a check to make sure all functions are being imported - https://github.com/pola-rs/polars/blob/082dcc05ed4aec074c74a370628b28f423a9eb57/py-polars/polars/__init__.py#L4
- [x] Setup Github runners for CICD
- [ ] Start dbt project
    - [ ] Use precommit hooks (SQLfluff)
- [ ] Use Asset Checks in Dagster
- [ ] Use metadata in Dagster
- [ ] For dbt assets in Dagster just do sensors on the ingest jobs
- [ ] Use Great Expectations as well
- [ ] Decide between streamlit or evidence.dev
    - I want to use some maps
- [ ] Do a local only project with DuckDB
- [ ] Setup everything into a Docker container
- [ ] Do a cloud project with deploying
    - Dagster, DBT, Docker, Kubernetes, Terraform
- [ ] Maybe do an LLM over the dataset? idk
- Things to test for (can put these into a conventions folder/file):
    - [ ] Dagster Assets should be in a group

- [ ] Build Sphinx website - https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html
- [ ] Dagster setup slack integration for failure bot
    - Also do on success include helpful metadata (name, description, developer, trigger time)
- [ ] Add dataframe utils
- [ ] Build an internal Monitoring/Health check report
    - [ ] DBT % of models with documentation/tests/pk test
