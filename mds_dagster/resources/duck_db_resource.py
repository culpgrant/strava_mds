"""
Dagster DuckDB Resource for interating with DuckDB
Creating to maintain the resource easier
"""

from typing import Dict, Optional

from dagster_duckdb import DuckDBResource

from core_library.utilities.custom_log import setup_console_logger

mds_logger = setup_console_logger()

# TODO: Make it so execute_query can take multiple queries
# TODO: Fix the type checks


class MDSDuckDBResource(DuckDBResource):
    """
    Customize Base DuckDB Dagster Resource
    """

    def execute_query(
        self,
        sql_query: str,
        write_disk_format: Optional[str] = None,
        write_disk_location: Optional[str] = None,
        fetch_format: Optional[str] = "python_object",
    ):
        """
        Execute and return a query

        :param sql_query: sql query to run
        :type sql_query: str
        :param write_disk_format: Write the data to disk, defaults to None
        :type write_disk_format: Optional[str], optional
        :param write_disk_location: file location, defaults to None
        :type write_disk_location: Optional[str], optional
        :param fetch_format: Format to return the result in, defaults to "python_object"
        :type fetch_format: Optional[str], optional
        :raises ValueError: Incorrect parameter values
        :raises ValueError: Incorrect parameter values
        :raises ValueError: Incorrect parameter values
        :return: Duckdb query result
        :rtype: _type_
        """
        valid_fetch_format = {"polars", "arrow", "python_object"}
        valid_write_disk_format = {"parquet", "csv"}

        # Validate the parameters
        if not fetch_format and not write_disk_format:
            raise ValueError("You must pass in a fetch_format or a write_disk_format")
        if fetch_format and fetch_format not in valid_fetch_format:
            raise ValueError(
                f"Invalid fetch_format of {fetch_format}. Expected to be in {valid_fetch_format}"
            )
        if write_disk_format and write_disk_format not in valid_write_disk_format:
            raise ValueError(
                f"Invalid write_disk_format of {write_disk_format}. Expected to be in {valid_write_disk_format}"
            )

        with DuckDBResource.get_connection(self) as conn:
            mds_logger.info(f"Running Query {sql_query}")

            if fetch_format == "polars":
                result = conn.execute(query=sql_query).pl()
                return result
            elif fetch_format == "python_object":
                result = conn.execute(query=sql_query).fetchall()
                return result
            elif fetch_format == "arrow":
                result = conn.execute(query=sql_query).arrow()
                return result

    def generate_dagster_metadata(self, table_name: str, *args, **kwargs) -> Dict:
        """
        Generates a dictionary of the metadata that we want to pass into Dagster

        :param table_name: table name to get metadata on
        :type table_name: str
        :return: helpful metadata
        :rtype: Dict
        """
        # TODO: implement a schema functionality to this
        mds_logger.info("Gathering Duck DB Table Metadata")
        columns_select = [
            "database_name",
            "schema_name",
            "table_name",
            "column_count",
            "estimated_size",
        ]
        query = f"SELECT {','.join(columns_select)} FROM duckdb_tables() WHERE TABLE_NAME = '{table_name}'"

        query_result = self.execute_query(query, fetch_format="polars", *args, **kwargs)

        metadata = {
            "table_name": query_result.select("table_name").item(),
            "datbase_name": query_result.select("database_name").item(),
            "schema_name": query_result.select("schema_name").item(),
            "column_count": query_result.select("column_count").item(),
            "estimated_num_rows": query_result.select("estimated_size").item(),
        }

        return metadata

    def check_schema_exists(self, schema_name: str) -> bool:
        """
        Function that tells you if a schema exists

        :param schema_name: schema to check
        :type schema_name: str
        :return: Tells you if it exists
        :rtype: bool
        """

        # Schemas are case insensative
        schema_name = schema_name.lower()
        mds_logger.info(f"Checking if {schema_name} exists")

        query = f"SELECT DISTINCT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}';"

        query_result = self.execute_query(query, fetch_format="python_object")
        if len(query_result) > 0:
            return True
        else:
            return False

    def create_schema(self, schema_name: str) -> bool:
        """
        Create a schema if it does not already exists

        :param schema_name: schema to create
        :type schema_name: str
        :return: True if executed
        :rtype: bool
        """

        # Schemas are case insensative
        schema_name = schema_name.lower()
        check_result = self.check_schema_exists(schema_name)
        if check_result:
            mds_logger.info(f"Schema {schema_name} already exists")
            return True
        else:
            mds_logger.info(f"Schema {schema_name} does not exist")
            query = f"CREATE SCHEMA IF NOT EXISTS {schema_name}"
            self.execute_query(query)
            return True
