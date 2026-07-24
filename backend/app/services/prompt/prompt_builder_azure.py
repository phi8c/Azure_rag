from typing import Any
import re


class PromptBuilderAzure:

    @staticmethod
    def build(
        system_prompt: str,
        variables: dict[str, Any],
    ) -> tuple[str, str]:

        system = system_prompt

        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            system = system.replace(
                placeholder,
                "" if value is None else str(value),
            )

        PromptBuilderAzure._validate(system)

        user = PromptBuilderAzure._build_user_prompt(
            variables,
        )

        return (
            system,
            user,
        )

    @staticmethod
    def _build_user_prompt(
        variables: dict[str, Any],
    ) -> str:

        return f"""
Job Description:

{variables.get("job_description", "")}

----------------------------------------

CV:

{variables.get("cv_text", "")}
""".strip()

    @staticmethod
    def _validate(
        prompt: str,
    ) -> None:

        placeholders = re.findall(
            r"\{\{(.*?)\}\}",
            prompt,
        )

        if placeholders:
            raise ValueError(
                "Missing prompt variables: "
                + ", ".join(placeholders)
            )