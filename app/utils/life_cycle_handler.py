from fastapi import FastAPI

from app.services.database_update_service import DatabaseUpdateService


def __on_app_started():
    DatabaseUpdateService.upgrade_public_schema()


def __on_app_finished():
    pass


def setup_event_handlers(app: FastAPI):
    app.add_event_handler("startup", __on_app_started)
    app.add_event_handler("shutdown", __on_app_finished)
