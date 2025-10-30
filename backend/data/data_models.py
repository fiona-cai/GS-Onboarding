# Data models used in the onboarding
# NOTE: This file should not be modified
from datetime import datetime
from pydantic import model_validator
from sqlmodel import Field

from backend.data.base_model import BaseSQLModel
from backend.data.enums import CommandStatus


class MainCommand(BaseSQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.

    List of commands: https://docs.google.com/spreadsheets/d/1XWXgp3--NHZ4XlxOyBYPS-M_LOU_ai-I6TcvotKhR1s/edit?gid=564815068#gid=564815068
    """

    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    name: str
    params: str | None = None
    format: str | None = None
    data_size: int
    total_size: int

    @model_validator(mode="after")
    def validate_params_format(self):
        """
        Check that params and format are both None or that the params and format have the same number of comma seperated values.
        In either of these cases return self. Otherwise raise a ValueError.
        The format of the comma seperated values is "data1,data2" so no spaces between data and the commas.
        """
        # If both are None, it's valid
        if self.params is None and self.format is None:
            return self

        # If only one is provided, it's invalid
        if (self.params is None) != (self.format is None):
            raise ValueError("Both params and format must be provided together or both be None")

        assert self.params is not None and self.format is not None

        # Split on commas and trim whitespace for comparison purposes
        params_list = [p.strip() for p in self.params.split(",")] if self.params != "" else []
        format_list = [f.strip() for f in self.format.split(",")] if self.format != "" else []

        if len(params_list) != len(format_list):
            raise ValueError("Params and format must have the same number of values")

        return self


class Command(BaseSQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """

    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    command_type: int = Field(
        foreign_key="maincommand.id"
    )  # Forign key must be a string
    status: CommandStatus = CommandStatus.PENDING
    params: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
