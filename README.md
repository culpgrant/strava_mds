## Strava Modern Data Stack
This is a project used to analyse my strava data using the modern data stack

## Project Inspriation
Please check out the other amazing projects that inspired me and this project
- https://github.com/matsonj/nba-monte-carlo
- https://github.com/dagster-io/mdsfest-opensource-mds

# Run Locally
- Set `PYTHONPATH` environment variable


## TODO
- [x] Setup pytest
- [x] Move intterogate arguments to .toml file
- [ ] Create a script for starting dagster locally
- [ ] Build out internal library
    - [ ] Create the handler for strava
- [ ] Setup Github runners for CICD
- [ ] Build out dagster ingest
- [ ] Start dbt project
    - [ ] Use precommit hooks (SQLfluff)
- [ ] Use Asset Checks in Dagster
- [ ] Use Great Expectations as well
- [ ] Decide between streamlit or evidence.dev
    - I want to use some maps
- [ ] Do a local only project with DuckDB
- [ ] Do a cloud project with deploying
    - Dagster, DBT, Docker, Kubernetes, Terraform
- [ ] Maybe do an LLM over the dataset? idk
