from sqlalchemy import *

from sqlalchemy.orm import *

from app.core.database import Base


class DepartmentSensitivityPermission(

    Base

):


    __tablename__ = (

        "department_sensitivity_permissions"

    )


    id:Mapped[int] = (

        mapped_column(

            primary_key=True
        )

    )


    owner_department_id:Mapped[int | None] = (

        mapped_column(

            nullable=True
        )

    )


    viewer_department_id:Mapped[int | None] = (

        mapped_column(

            nullable=True
        )

    )


    sensitivity_id: Mapped[int | None] = (

        mapped_column(

            nullable=True
        )

    )


    position_level_id:Mapped[int | None] = (

        mapped_column(

            nullable=True
        )

    )


    allow:Mapped[bool | None] = (

        mapped_column(

            default=False,

            nullable=True
        )

    )