from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.role import (
    Role
)

from app.models.department import (
    Department
)

from app.models.position_level import (
    PositionLevel
)

from app.models.sensitivity_level import (
    SensitivityLevel
)

from app.models.department_sensitivity_permission import (
    DepartmentSensitivityPermission
)


class PermissionRepository:


    @staticmethod
    async def get_role_access(

        db:
        AsyncSession,   

        role_name:
        str

    ):


        role_query = await db.execute(

            select(
                Role
            )

            .where(

                Role.name
                == role_name

            )

        )


        role = (

            role_query
            .scalar_one_or_none()

        )


        if not role:

            return []


        result = await db.execute(

            select(

                Department.name,

                SensitivityLevel.priority,

                SensitivityLevel.code

            )

            .join(

                DepartmentSensitivityPermission,

                Department.id

                ==

                DepartmentSensitivityPermission
                .owner_department_id

            )

            .join(

                SensitivityLevel,

                SensitivityLevel.id

                ==

                DepartmentSensitivityPermission
                .sensitivity_id

            )

            .where(

                DepartmentSensitivityPermission
                .viewer_department_id

                ==

                role.department_id,


                DepartmentSensitivityPermission
                .position_level_id

                ==

                role.position_level_id,


                DepartmentSensitivityPermission
                .allow

                ==

                True

            )

        )


        permissions = result.all()
        
        print(" in ra permission trong hàm", permissions)


        return [

            {

                "department":

                row[0],


                "max_sensitivity":

                row[1],


                "sensitivity_code":

                row[2]

            }

            for row in permissions

        ]