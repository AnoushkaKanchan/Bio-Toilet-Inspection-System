from apps.ai.contracts import (
    TANK_REQUIRED_FIELDS,
    TOP_LEVEL_REQUIRED_FIELDS,
    VALID_CAMERA_SIDES,
    VALID_MAINTENANCE_STATUS,
    VALID_PIPE_STATUS,
    VALID_PIPE_SUPPORT_STATUS,
    VALID_RUN_STATUS,
    VALID_SURFACE_STATUS,
)
from apps.ai.exceptions import AIContractError


class AIContractValidator:
    def validate(self, payload: dict) -> None:
        self._validate_payload(payload)
        self._validate_top_level_fields(payload)
        self._validate_status(payload)
        self._validate_tanks(payload)

    def _require_fields(
        self,
        data: dict,
        required_fields: tuple[str, ...],
    ) -> None:
        for field in required_fields:
            if field not in data:
                raise AIContractError(f"Missing required field: '{field}'.")

    def _validate_enum(
        self,
        value,
        valid_values,
        field_name: str,
    ) -> None:
        if value not in valid_values:
            raise AIContractError(f"Invalid {field_name}: {value}")

    def _validate_numeric(
        self,
        value,
        field_name: str,
    ) -> None:
        if not isinstance(value, (int, float)):
            raise AIContractError(f"'{field_name}' must be numeric.")

    def _validate_payload(self, payload: dict) -> None:
        if payload is None:
            raise AIContractError("Payload cannot be None.")

        if not isinstance(payload, dict):
            raise AIContractError("Payload must be a JSON object.")

    def _validate_top_level_fields(
        self,
        payload: dict,
    ) -> None:
        self._require_fields(
            payload,
            TOP_LEVEL_REQUIRED_FIELDS,
        )

    def _validate_status(
        self,
        payload: dict,
    ) -> None:
        self._validate_enum(
            payload["status"],
            VALID_RUN_STATUS,
            "status",
        )

    def _validate_tanks(
        self,
        payload: dict,
    ) -> None:
        tanks = payload["tanks"]

        if not isinstance(tanks, list):
            raise AIContractError("'tanks' must be a list.")

        if not tanks:
            raise AIContractError("'tanks' cannot be empty.")

        for tank in tanks:
            self._validate_tank(tank)

    def _validate_tank(
        self,
        tank: dict,
    ) -> None:
        if not isinstance(tank, dict):
            raise AIContractError("Each tank must be a JSON object.")

        self._require_fields(
            tank,
            TANK_REQUIRED_FIELDS,
        )

        if not isinstance(
            tank["coach_number"],
            int,
        ):
            raise AIContractError("'coach_number' must be an integer.")

        if not isinstance(
            tank["tank_id"],
            str,
        ):
            raise AIContractError("'tank_id' must be a string.")

        if not isinstance(
            tank["detection_image_path"],
            str,
        ):
            raise AIContractError("'detection_image_path' must be a string.")

        self._validate_enum(
            tank["camera_side"],
            VALID_CAMERA_SIDES,
            "camera_side",
        )

        self._validate_enum(
            tank["pipe_status"],
            VALID_PIPE_STATUS,
            "pipe_status",
        )

        if "pipe_support_status" in tank:
            self._validate_enum(
                tank["pipe_support_status"],
                VALID_PIPE_SUPPORT_STATUS,
                "pipe_support_status",
            )

        self._validate_enum(
            tank["surface_status"],
            VALID_SURFACE_STATUS,
            "surface_status",
        )

        self._validate_enum(
            tank["maintenance_status"],
            VALID_MAINTENANCE_STATUS,
            "maintenance_status",
        )

        self._validate_numeric(
            tank["timestamp_sec"],
            "timestamp_sec",
        )

        self._validate_numeric(
            tank["detection_confidence"],
            "detection_confidence",
        )

        if tank["timestamp_sec"] < 0:
            raise AIContractError("'timestamp_sec' cannot be negative.")

        if not (0 <= tank["detection_confidence"] <= 1):
            raise AIContractError("'detection_confidence' must be between 0 and 1.")
