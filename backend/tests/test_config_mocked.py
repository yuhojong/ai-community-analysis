import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.llm_service import LLMService
import os

@pytest.mark.asyncio
async def test_llm_service_config_fallback_mocked():
    # Mock environment variable
    with patch.dict(os.environ, {"OPENAI_API_KEY": "env_key"}):
        service = LLMService(provider="openai")
        # Without DB, should fallback to env
        await service._ensure_client(db=None)
        assert service.api_key == "env_key"

@pytest.mark.asyncio
async def test_llm_service_config_db_mocked():
    from backend.models import SystemConfig

    # Mock DB session
    mock_db = AsyncMock()

    # Mock SystemConfig.get_value
    with patch("backend.models.SystemConfig.get_value", new_callable=AsyncMock) as mock_get_value:
        mock_get_value.return_value = "db_key"

        service = LLMService(provider="openai")
        await service._ensure_client(db=mock_db)

        assert service.api_key == "db_key"
        mock_get_value.assert_called_with(mock_db, "OPENAI_API_KEY")

@pytest.mark.asyncio
async def test_run_analysis_logic_mocked():
    from backend.scripts.run_analysis import run_daily_analysis
    from backend.models import Platform, SystemConfig

    mock_platforms = [
        MagicMock(spec=Platform, name="daum", id=1, is_active=True, config={"daum_id": "db_id", "daum_pw": "db_pw"})
    ]

    with patch("backend.scripts.run_analysis.AsyncSessionLocal") as mock_session_cls, \
         patch("backend.scripts.run_analysis.select") as mock_select, \
         patch("backend.scripts.run_analysis.DaumCafeScraper") as mock_scraper_cls, \
         patch("backend.scripts.run_analysis.LLMService") as mock_llm_cls, \
         patch("backend.scripts.run_analysis.ReportGenerator") as mock_report_gen, \
         patch("backend.models.SystemConfig.get_value", new_callable=AsyncMock) as mock_get_config:

        mock_db = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_db

        # Mocking db executions
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_platforms
        mock_db.execute.return_value = mock_result

        mock_get_config.side_effect = lambda db, key, default=None: {
            "LLM_PROVIDER": "openai",
            "SLACK_TOKEN": "slack_token",
            "SLACK_CHANNEL_ID": "chan_id"
        }.get(key, default)

        # We don't need to run the whole thing, just verifying the mocks are hit correctly if we were to run it.
        # But let's try to run it and expect it to fail later or finish if everything is mocked.

        # Mock scraper
        mock_scraper = AsyncMock()
        mock_scraper_cls.return_value = mock_scraper

        # Mock fetch_posts to return empty to finish quickly
        mock_scraper.fetch_posts.return_value = []

        # Mock targets
        mock_target_result = MagicMock()
        mock_target_result.scalars.return_value.all.return_value = [] # No targets to finish quickly
        mock_db.execute.side_effect = [mock_result, mock_target_result]

        await run_daily_analysis()

        # Verify if config was fetched from DB
        assert mock_get_config.called
