import pytest

from zenserp.search import TBM, Device, SearchInput


class TestSearchInput:
    parameters = (
        (
            SearchInput(
                "Pied Piper",
                location="Tokyo,Japan",
                search_engine="google.co.jp",
                limit=5,
                offset=10,
                tbm=TBM.IMAGE_SEARCH,
                device=Device.DESKTOP,
                timeframe="w",
                gl="JP",
                lr="lang_en|lang_ja",
                hl="ja",
                latitude="35.652832",
                longitude="139.839478",
            ),
            {
                "q": "Pied Piper",
                "location": "Tokyo,Japan",
                "search_engine": "google.co.jp",
                "num": 5,
                "start": 10,
                "tbm": "isch",
                "device": "desktop",
                "timeframe": "w",
                "gl": "JP",
                "lr": "lang_en|lang_ja",
                "hl": "ja",
                "lat": "35.652832",
                "lng": "139.839478",
            },
        ),
        (
            SearchInput("Pied Piper"),
            {"q": "Pied Piper"},
        ),
    )

    @pytest.mark.parametrize("search_input, expect", parameters)
    def test_to_params(self, search_input, expect):
        params = search_input.to_params()
        assert params == expect
