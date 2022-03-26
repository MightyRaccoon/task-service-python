import logging
import os

from sqlalchemy import create_engine


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level='INFO'
)


def main():

    logger.info("Read SQL scripts")
    scripts = os.listdir("sql")

    logger.info("Connect to DB")
    psql_engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format(
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
            "172.19.0.2",
            5432,
            os.environ["POSTGRES_DB"]
        )
    )

    logger.info("Migrations Start")
    with psql_engine.connect() as db_connect:
        for script in scripts:
            logger.info("Migration %s started", script)
            full_script_part = "sql/" + script

            with open(full_script_part, "r") as file:
                query = file.read()

            db_connect.execute(query)

            logger.info("Migration %s done", script)

    logger.info("All migrations done!")


if __name__ == "__main__":
    main()
