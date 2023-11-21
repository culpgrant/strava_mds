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
- [ ] Add precommit hooks for "Your code has been rated at xxx/10"
- [x] Fix the isort so we can have the proper ordering of the packages(native, 3rdparty, my package)
- [x] Setup logging
- [x] Build out internal library
    - [x] Create the handler for strava
- [x] Setup Github runners for CICD
- [x] Build out dagster ingest
- [ ] Start dbt project
    - [ ] Use precommit hooks (SQLfluff)
- [ ] Use Asset Checks in Dagster
- [ ] Use metadata in Dagster
- [ ] Use Great Expectations as well
- [ ] Decide between streamlit or evidence.dev
    - I want to use some maps
- [ ] Do a local only project with DuckDB
- [ ] Setup everything into a Docker container
- [ ] Do a cloud project with deploying
    - Dagster, DBT, Docker, Kubernetes, Terraform
- [ ] Maybe do an LLM over the dataset? idk
- Things to test for:
    - [ ] Dagster Assets should be in a group
- [ ] Build Sphinx website - https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html
- [x] Github pr template
- [ ] Dagster setup slack integration for failure bot
