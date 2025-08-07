import argparse
import traceback

from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy.orm import Session
from alembic import (
    command, 
    script
)
from alembic.config import Config
from alembic.migration import MigrationContext

from app.connectors.database_connector import (
    get_database, 
    get_db
)
from app.utils.constants import (
    DB_NOT_UPTODATE, 
    PUBLIC_SCHEMA
)
from app.utils.utils import get_project_root


@dataclass
class DatabaseUpdateService:
    db: Session = Depends(get_db)

    @staticmethod
    def __get_current_head(db: Session):
        connection = db.connection()
        context = MigrationContext.configure(connection)
        current_head = context.get_current_revision()
        if current_head == None:
            raise Exception(DB_NOT_UPTODATE)
        return current_head


    @staticmethod
    def __upgrade(schema: str, current_head: str):
        alembic_config = Config(get_project_root().joinpath("alembic.ini"))
        alembic_script = script.ScriptDirectory.from_config(alembic_config)
        config_head = alembic_script.get_current_head()

        if current_head != config_head:
            raise RuntimeError(
                "Database is not up-to-date. Execute migrations."
            )
        
        # If it is required to pass -x parameters to alembic
        x_arg = "".join(["tenant=", schema])  # "dry_run=" + "True"
        alembic_config.cmd_opts = argparse.Namespace()  # arguments stub

        if not hasattr(alembic_config.cmd_opts, "x"):
            if x_arg is not None:
                setattr(alembic_config.cmd_opts, "x", [x_arg])
            else:
                setattr(alembic_config.cmd_opts, "x", None)

        command.upgrade(alembic_config, "head")


    @staticmethod
    def upgrade_public_schema():
        db = get_database()
        try:
            current_head = DatabaseUpdateService.__get_current_head(db)
            DatabaseUpdateService.__upgrade(PUBLIC_SCHEMA, current_head)
            db.commit()
            db.flush()
        except:
            db.rollback()
            traceback.print_exc()
        finally:
            db.close()        

