from apps.inspection.models import Inspection
from apps.ntes.dto import NTESCoachDTO
from apps.ntes.models import NTESCoach


class NTESCoachRepository:
    def replace_composition(
        self,
        *,
        inspection: Inspection,
        coaches: list[NTESCoachDTO],
    ) -> list[NTESCoach]:
        NTESCoach.objects.filter(
            inspection=inspection,
        ).delete()

        coach_models = [
            NTESCoach(
                inspection=inspection,
                coach_sequence=coach.coach_sequence,
                coach_number=coach.coach_number,
                coach_type=coach.coach_type,
            )
            for coach in coaches
        ]

        created = NTESCoach.objects.bulk_create(
            coach_models,
        )

        return created

    def get_composition(
        self,
        *,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        return list(
            NTESCoach.objects.filter(
                inspection=inspection,
            ).order_by(
                "coach_sequence",
            )
        )
