import logging

from bs4 import BeautifulSoup

from apps.ntes.dto import RawCoachDTO
from apps.ntes.exceptions import NTESParsingError

logger = logging.getLogger(__name__)


class NTESHTMLParser:
    def parse(
        self,
        html: str,
    ) -> list[RawCoachDTO]:
        logger.info("Starting NTES coach composition parsing.")

        if not html.strip():
            logger.error("Empty HTML received for parsing.")
            raise NTESParsingError("Coach composition HTML is empty.")

        try:
            soup = BeautifulSoup(
                html,
                "html.parser",
            )

            table = soup.find("table")

            if table is None:
                raise NTESParsingError("Coach composition table not found.")

            tbody = table.find("tbody")

            if tbody is None:
                raise NTESParsingError("Coach composition table body not found.")

            row = tbody.find("tr")

            if row is None:
                raise NTESParsingError("Coach composition row not found.")

            container = row.find("td")

            if container is None:
                raise NTESParsingError("Coach container not found.")

            coach_blocks = container.find_all(
                "div",
                style=lambda value: (
                    value is not None and "display:inline-block" in value
                ),
                recursive=False,
            )

            if not coach_blocks:
                raise NTESParsingError("No coach blocks found.")

            logger.info(
                "Found %d coach blocks.",
                len(coach_blocks),
            )

            coaches: list[RawCoachDTO] = []

            for block in coach_blocks:
                children = block.find_all(
                    "div",
                    recursive=False,
                )

                if len(children) != 3:
                    logger.warning(
                        "Skipping malformed coach block with %d child divs.",
                        len(children),
                    )
                    continue

                coach_number_tag = children[1].find("b")

                if coach_number_tag is None:
                    logger.warning("Skipping coach block without coach number.")
                    continue

                coaches.append(
                    RawCoachDTO(
                        coach_sequence=children[2].get_text(),
                        coach_number=coach_number_tag.get_text(),
                        coach_type=children[0].get_text(),
                    )
                )

            logger.info(
                "Extracted %d RawCoachDTO objects.",
                len(coaches),
            )

            return coaches

        except NTESParsingError:
            logger.exception("NTES parsing failed.")
            raise

        except Exception as exc:
            logger.exception("Unexpected parsing failure.")
            raise NTESParsingError("Failed to parse coach composition.") from exc
