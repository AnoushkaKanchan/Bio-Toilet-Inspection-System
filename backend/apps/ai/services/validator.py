from apps.ai.contracts import (
    ALLOWED_TANK_FIELDS,
    ALLOWED_TOP_LEVEL_FIELDS,
    TANK_ID_PATTERN,
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
        self._validate_top_level_types(payload)
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
            raise AIContractError(
                f"Invalid {field_name}: {value!r}. "
                f"Expected one of: {sorted(valid_values)}."
            )
        
    def _validate_numeric(
        self,
        value,
        field_name: str,
        minimum: float | int | None = None,
        maximum: float | int | None = None,
    ) -> None:
        # Python evaluates isinstance(True, int) as True, so we must explicitly exclude bool
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise AIContractError(f"'{field_name}' must be numeric.")
        
        if minimum is not None and value < minimum:
            raise AIContractError(f"'{field_name}' cannot be less than {minimum}.")
            
        if maximum is not None and value > maximum:
            raise AIContractError(f"'{field_name}' cannot be greater than {maximum}.")

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

        # Reject unknown top-level fields using pre-computed set
        unknown_fields = set(payload) - ALLOWED_TOP_LEVEL_FIELDS
        if unknown_fields:
            raise AIContractError(
                f"Unknown top-level field(s): {sorted(unknown_fields)}"
            )

    def _validate_top_level_types(self, payload: dict) -> None:
        if not isinstance(payload["inspection_run_id"], str) or not payload["inspection_run_id"].strip():
            raise AIContractError("'inspection_run_id' must be a non-empty string.")

        video_source = payload["video_source"]
        if not isinstance(video_source, dict):
            raise AIContractError("'video_source' must be an object.")

        for field in ("left_camera", "right_camera"):
            if (
                field not in video_source
                or not isinstance(video_source[field], str)
                or not video_source[field].strip()
            ):
                raise AIContractError(
                    f"'video_source.{field}' must be a non-empty string."
                )

        if not isinstance(payload["train_inspection_timestamp"], str) or not payload["train_inspection_timestamp"].strip():
            raise AIContractError("'train_inspection_timestamp' must be a non-empty string.")

        if not isinstance(payload["summary"], dict):
            raise AIContractError("'summary' must be a JSON object.")

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

        seen_tanks = set()

        for tank in tanks:
            self._validate_tank(tank)
            
            tank_key = (tank["coach_number"], tank["tank_id"])
            if tank_key in seen_tanks:
                raise AIContractError(
                    f"Duplicate tank record found for coach {tank['coach_number']}, tank ID '{tank['tank_id']}'."
                )
            seen_tanks.add(tank_key)

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

        # Reject unknown tank fields using pre-computed set
        unknown_fields = set(tank) - ALLOWED_TANK_FIELDS
        if unknown_fields:
            raise AIContractError(
                f"Unknown tank field(s): {sorted(unknown_fields)}"
            )

        # Enforce exact type check for integer before checking bounds
        if isinstance(tank["coach_number"], bool) or not isinstance(tank["coach_number"], int):
            raise AIContractError("'coach_number' must be an integer.")
            
        self._validate_numeric(
            tank["coach_number"],
            "coach_number",
            minimum=0,
        )

        if not isinstance(tank["tank_id"], str):
            raise AIContractError("'tank_id' must be a string.")
            
        if not TANK_ID_PATTERN.match(tank["tank_id"]):
            raise AIContractError(f"'tank_id' '{tank['tank_id']}' does not match the required pattern (e.g., L1, R2).")

        if not isinstance(tank["detection_image_path"], str) or not tank["detection_image_path"].strip():
            raise AIContractError("'detection_image_path' must be a non-empty string.")

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
            minimum=0,
        )

        self._validate_numeric(
            tank["detection_confidence"],
            "detection_confidence",
            minimum=0,
            maximum=1,
        )