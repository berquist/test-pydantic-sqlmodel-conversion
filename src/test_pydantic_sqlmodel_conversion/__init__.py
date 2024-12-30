from datetime import date
from typing import Annotated, TypedDict

from pydantic import BaseModel, BeforeValidator
from sqlmodel import Field, SQLModel


class FuzzyTime(TypedDict):
    year: int | None
    month: int | None
    day: int | None


def date_from_fuzzytime_dict(ft: FuzzyTime) -> date | None:
    """Convert a FuzzyTime (FuzzyDate) dict to a datetime object.

    If all of the FuzzyTime fields are None, this usually means that it refers
    to something ongoing and None is returned.  If the year is known and any
    of the month or day are not, the date exists but is not fully known, and
    we currently assume that it is the first of the month and/or day.
    """
    year = ft["year"]
    month = ft["month"]
    day = ft["day"]
    if year is None:
        assert month is None
    if month is None:
        assert day is None
    if year is None:
        return None
    if month is None:
        month = 1
    if day is None:
        day = 1
    return date.fromisoformat(f"{year}-{month:02}-{day:02}")


class MyPydanticModel(BaseModel):
    id: int
    mydate: Annotated[date, BeforeValidator(date_from_fuzzytime_dict)]


class MySqlModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    mydate: Annotated[date, BeforeValidator(date_from_fuzzytime_dict)]


def main() -> None:
    mydate = {"year": 2024, "month": 7, "day": 4}
    model_pydantic = MyPydanticModel(id=0, mydate=mydate)
    print(model_pydantic)
    model_sqlmodel = MySqlModel(id=0, mydate=mydate)
    print(model_sqlmodel)
