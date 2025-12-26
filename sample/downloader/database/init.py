from tortoise import Tortoise
import logging


logger = logging.getLogger(__name__)


async def connect(db: str) -> None:
    await Tortoise.init(db_url=db, modules={"models": ["database.models"]})
    await Tortoise.generate_schemas()

    logger.info("connect to the database: %s", db)


async def disconnect():
    await Tortoise.close_connections()

    logger.info("disconnected the database")