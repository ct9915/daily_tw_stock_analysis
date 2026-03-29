# -*- coding: utf-8 -*-
"""Tests for Taiwan (TW) market support.

Covers:
- market_context: detect_market, get_market_role, get_market_guidelines
- data_provider.base: _is_tw_market, is_tw_stock_code, normalize_stock_code, _market_tag
- trading_calendar: MARKET_EXCHANGE, MARKET_TIMEZONE, get_market_for_stock
- market_strategy: TW_BLUEPRINT via get_market_strategy_blueprint
- market_profile: TW_PROFILE via get_profile
"""

import unittest

try:
    import data_provider  # noqa: F401
    _DATA_PROVIDER_AVAILABLE = True
except Exception:
    _DATA_PROVIDER_AVAILABLE = False


class TestDetectMarketTW(unittest.TestCase):
    """detect_market() correctly identifies Taiwan stocks."""

    def setUp(self):
        from src.market_context import detect_market
        self.detect = detect_market

    def test_tw_prefix_uppercase(self):
        self.assertEqual(self.detect("TW2330"), "tw")

    def test_tw_prefix_lowercase(self):
        self.assertEqual(self.detect("tw2330"), "tw")

    def test_tw_prefix_mixed_case(self):
        self.assertEqual(self.detect("Tw2330"), "tw")

    def test_tw_suffix_dot_tw(self):
        self.assertEqual(self.detect("2330.TW"), "tw")

    def test_tw_suffix_dot_two(self):
        self.assertEqual(self.detect("6770.TWO"), "tw")

    def test_tw_etf_code(self):
        self.assertEqual(self.detect("tw00050"), "tw")

    def test_no_collision_with_us(self):
        self.assertEqual(self.detect("AAPL"), "us")
        self.assertEqual(self.detect("TSLA"), "us")

    def test_cn_unaffected(self):
        self.assertEqual(self.detect("600519"), "cn")
        self.assertEqual(self.detect("000001"), "cn")

    def test_hk_unaffected(self):
        self.assertEqual(self.detect("HK00700"), "hk")
        self.assertEqual(self.detect("00700.HK"), "hk")


class TestMarketContextTW(unittest.TestCase):
    """get_market_role / get_market_guidelines return TW-specific content."""

    def test_role_zh(self):
        from src.market_context import get_market_role
        self.assertIn("台股", get_market_role("tw2330", lang="zh"))

    def test_role_en(self):
        from src.market_context import get_market_role
        self.assertIn("Taiwan", get_market_role("tw2330", lang="en"))

    def test_guidelines_zh_contains_limit_and_settlement(self):
        from src.market_context import get_market_guidelines
        g = get_market_guidelines("tw2330", lang="zh")
        self.assertIn("±10%", g)
        self.assertIn("T+2", g)

    def test_guidelines_en_contains_twse_and_twd(self):
        from src.market_context import get_market_guidelines
        g = get_market_guidelines("TW2330", lang="en")
        self.assertIn("TWSE", g)
        self.assertIn("TWD", g)


@unittest.skipUnless(_DATA_PROVIDER_AVAILABLE, "data_provider deps not installed")
class TestNormalizeStockCodeTW(unittest.TestCase):
    """normalize_stock_code handles TW prefix and .TW / .TWO suffix forms."""

    def setUp(self):
        from data_provider.base import normalize_stock_code
        self.normalize = normalize_stock_code

    def test_tw_prefix_lowercase(self):
        self.assertEqual(self.normalize("tw2330"), "TW2330")

    def test_tw_prefix_already_upper(self):
        self.assertEqual(self.normalize("TW2330"), "TW2330")

    def test_dot_tw_suffix(self):
        self.assertEqual(self.normalize("2330.TW"), "TW2330")

    def test_dot_two_suffix(self):
        self.assertEqual(self.normalize("6770.TWO"), "TW6770")

    def test_tw_etf(self):
        self.assertEqual(self.normalize("tw00050"), "TW00050")

    def test_cn_code_unchanged(self):
        self.assertEqual(self.normalize("600519"), "600519")

    def test_hk_code_unchanged(self):
        self.assertEqual(self.normalize("HK00700"), "HK00700")


@unittest.skipUnless(_DATA_PROVIDER_AVAILABLE, "data_provider deps not installed")
class TestMarketTagTW(unittest.TestCase):
    """_market_tag and is_tw_stock_code return correct values."""

    def test_market_tag_tw(self):
        from data_provider.base import _market_tag
        self.assertEqual(_market_tag("TW2330"), "tw")

    def test_market_tag_cn(self):
        from data_provider.base import _market_tag
        self.assertEqual(_market_tag("600519"), "cn")

    def test_market_tag_hk(self):
        from data_provider.base import _market_tag
        self.assertEqual(_market_tag("HK00700"), "hk")

    def test_market_tag_us(self):
        from data_provider.base import _market_tag
        self.assertEqual(_market_tag("AAPL"), "us")

    def test_is_tw_stock_code_true(self):
        from data_provider.base import is_tw_stock_code
        for code in ("TW2330", "tw2330", "2330.TW", "6770.TWO"):
            with self.subTest(code=code):
                self.assertTrue(is_tw_stock_code(code))

    def test_is_tw_stock_code_false(self):
        from data_provider.base import is_tw_stock_code
        for code in ("600519", "HK00700", "AAPL"):
            with self.subTest(code=code):
                self.assertFalse(is_tw_stock_code(code))


class TestTradingCalendarTW(unittest.TestCase):
    """TW exchange is registered and get_market_for_stock routes correctly."""

    def test_tw_exchange_registered(self):
        from src.core.trading_calendar import MARKET_EXCHANGE
        self.assertIn("tw", MARKET_EXCHANGE)
        self.assertEqual(MARKET_EXCHANGE["tw"], "XTAI")

    def test_tw_timezone_registered(self):
        from src.core.trading_calendar import MARKET_TIMEZONE
        self.assertIn("tw", MARKET_TIMEZONE)
        self.assertEqual(MARKET_TIMEZONE["tw"], "Asia/Taipei")

    @unittest.skipUnless(_DATA_PROVIDER_AVAILABLE, "data_provider deps not installed")
    def test_get_market_for_stock_tw(self):
        from src.core.trading_calendar import get_market_for_stock
        self.assertEqual(get_market_for_stock("TW2330"), "tw")
        self.assertEqual(get_market_for_stock("tw2330"), "tw")

    @unittest.skipUnless(_DATA_PROVIDER_AVAILABLE, "data_provider deps not installed")
    def test_get_market_for_stock_others_unaffected(self):
        from src.core.trading_calendar import get_market_for_stock
        self.assertEqual(get_market_for_stock("AAPL"), "us")
        self.assertEqual(get_market_for_stock("HK00700"), "hk")
        self.assertEqual(get_market_for_stock("600519"), "cn")


class TestTWStrategyBlueprint(unittest.TestCase):
    """TW strategy blueprint is returned and has expected content."""

    def test_tw_blueprint_returned(self):
        from src.core.market_strategy import get_market_strategy_blueprint
        bp = get_market_strategy_blueprint("tw")
        self.assertEqual(bp.region, "tw")

    def test_tw_blueprint_prompt_block(self):
        from src.core.market_strategy import get_market_strategy_blueprint
        block = get_market_strategy_blueprint("tw").to_prompt_block()
        self.assertIn("台股市場三維分析策略", block)
        self.assertIn("Action Framework", block)
        self.assertIn("進攻", block)
        self.assertIn("外資", block)

    def test_cn_blueprint_unaffected(self):
        from src.core.market_strategy import get_market_strategy_blueprint
        self.assertEqual(get_market_strategy_blueprint("cn").region, "cn")

    def test_us_blueprint_unaffected(self):
        from src.core.market_strategy import get_market_strategy_blueprint
        self.assertEqual(get_market_strategy_blueprint("us").region, "us")


class TestTWMarketProfile(unittest.TestCase):
    """TW market profile is returned and has expected content."""

    def test_tw_profile_returned(self):
        from src.core.market_profile import get_profile
        self.assertEqual(get_profile("tw").region, "tw")

    def test_tw_mood_index(self):
        from src.core.market_profile import get_profile
        self.assertEqual(get_profile("tw").mood_index_code, "^TWII")

    def test_tw_news_queries_non_empty_and_relevant(self):
        from src.core.market_profile import get_profile
        queries = get_profile("tw").news_queries
        self.assertGreater(len(queries), 0)
        self.assertTrue(any("台股" in q for q in queries))

    def test_cn_profile_unaffected(self):
        from src.core.market_profile import get_profile
        p = get_profile("cn")
        self.assertEqual(p.region, "cn")
        self.assertEqual(p.mood_index_code, "000001")


if __name__ == "__main__":
    unittest.main()
