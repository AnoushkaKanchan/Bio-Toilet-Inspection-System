import logging
import time

from django.conf import settings
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
)
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import (
    sync_playwright,
)

from apps.ntes.exceptions import (
    CoachCompositionNotFoundError,
    NTESClientTimeoutError,
    NTESUnavailableError,
    TrainNotFoundError,
)

logger = logging.getLogger(__name__)


class PlaywrightNTESClient:

    def fetch(
        self,
        *,
        train_number: str,
    ) -> str:
        start = time.monotonic()

        playwright = None
        browser = None
        context = None
        page = None

        try:
            (
                playwright,
                browser,
                context,
                page,
            ) = self._launch_browser()

            logger.info(
                "Browser launched for train %s.",
                train_number,
            )

            self._open_ntes(
                page,
            )

            self._search_train(
                page,
                train_number,
            )

            self._check_invalid_train(
                page,
            )

            self._open_coach_position(
                page,
            )

            html = self._extract_modal_html(
                page,
            )

            logger.info(
                "Successfully retrieved coach composition for train %s.",
                train_number,
            )

            return html

        except PlaywrightTimeoutError as exc:
            logger.exception(
                "NTES timeout while processing train %s.",
                train_number,
            )
            raise NTESClientTimeoutError("NTES request timed out.") from exc

        except (
            NTESClientTimeoutError,
            TrainNotFoundError,
            CoachCompositionNotFoundError,
        ):
            raise

        except Exception as exc:
            logger.exception("NTES unavailable.")
            raise NTESUnavailableError("Unable to initialize NTES browser.") from exc

        finally:
            self._cleanup(
                playwright,
                browser,
                context,
                page,
            )

            logger.info(
                "Browser resources released in %.2f seconds.",
                time.monotonic() - start,
            )

    def _launch_browser(
        self,
    ) -> tuple[
        Playwright,
        Browser,
        BrowserContext,
        Page,
    ]:
        playwright = sync_playwright().start()

        browser_launcher = getattr(
            playwright,
            settings.NTES_BROWSER,
        )
        # temporary
        browser = browser_launcher.launch(
            headless=settings.NTES_HEADLESS,
        )

        context = browser.new_context(
            user_agent=settings.NTES_USER_AGENT,
        )

        page = context.new_page()

        page.set_default_timeout(
            settings.NTES_TIMEOUT_MS,
        )

        return (
            playwright,
            browser,
            context,
            page,
        )

    def _open_ntes(
        self,
        page: Page,
    ) -> None:
        logger.info("Opening NTES website.")

        try:
            page.goto(
                settings.NTES_BASE_URL,
                wait_until="domcontentloaded",
                timeout=settings.NTES_TIMEOUT_MS,
            )

            logger.info("NTES website loaded.")

        except PlaywrightTimeoutError as exc:
            raise NTESClientTimeoutError("Timed out while opening NTES.") from exc

    def _search_train(
        self,
        page: Page,
        train_number: str,
    ) -> None:
        logger.info(
            "Searching train %s.",
            train_number,
        )

        try:
            train_input = page.locator("#trainNo")

            train_input.fill(
                train_number,
            )

            search_button = page.locator(
                "span[onclick=\"onTrainInputFind('S');\"]",
            )

            search_button.click()

            coach_button = (
                page.locator(
                    "button[data-bs-toggle='modal']",
                )
                .filter(
                    has_text="Coach Position",
                )
                .first
            )

            page.locator(
                ".w3-panel.w3-red",
            ).or_(
                coach_button,
            ).wait_for(
                state="visible",
                timeout=settings.NTES_TIMEOUT_MS,
            )

            logger.info(
                "Train search completed.",
            )

        except PlaywrightTimeoutError as exc:
            raise NTESClientTimeoutError(
                "Timed out while searching train.",
            ) from exc

    def _check_invalid_train(
        self,
        page: Page,
    ) -> None:
        invalid_train = page.locator(".w3-panel.w3-red")

        if not invalid_train.is_visible():
            return

        message = invalid_train.inner_text().strip()

        if "Invalid Train No." in message:
            raise TrainNotFoundError(
                message,
            )

    def _open_coach_position(
        self,
        page: Page,
    ) -> None:
        logger.info(
            "Opening Coach Position modal.",
        )

        try:
            coach_button = (
                page.locator(
                    "button[data-bs-toggle='modal']",
                )
                .filter(
                    has_text="Coach Position",
                )
                .first
            )

            coach_button.wait_for(
                state="visible",
                timeout=settings.NTES_TIMEOUT_MS,
            )

            coach_button.scroll_into_view_if_needed()

            coach_button.click(
                force=True,
            )

            page.locator(
                ".modal.show",
            ).wait_for(
                state="visible",
                timeout=settings.NTES_TIMEOUT_MS,
            )

            logger.info(
                "Coach Position modal opened.",
            )

        except PlaywrightTimeoutError as exc:
            raise NTESClientTimeoutError(
                "Timed out while opening Coach Position.",
            ) from exc

        except Exception as exc:
            raise CoachCompositionNotFoundError(
                "Coach Position button not found.",
            ) from exc

    def _extract_modal_html(
        self,
        page: Page,
    ) -> str:
        logger.info(
            "Extracting Coach Position modal HTML.",
        )

        try:
            modal = page.locator(
                ".modal.show .modal-body",
            )

            modal.wait_for(
                state="visible",
                timeout=settings.NTES_TIMEOUT_MS,
            )

            html = modal.inner_html().strip()

            if not html:
                raise CoachCompositionNotFoundError(
                    "Coach Position modal is empty.",
                )

            return html

        except PlaywrightTimeoutError as exc:
            raise NTESClientTimeoutError(
                "Timed out while waiting for Coach Position modal.",
            ) from exc

    def _cleanup(
        self,
        playwright: Playwright | None,
        browser: Browser | None,
        context: BrowserContext | None,
        page: Page | None,
    ) -> None:
        for resource in (
            page,
            context,
            browser,
        ):
            if resource is None:
                continue

            try:
                resource.close()
            except Exception:
                logger.exception("Failed to close Playwright resource.")

        if playwright is not None:
            try:
                playwright.stop()
            except Exception:
                logger.exception("Failed to stop Playwright.")