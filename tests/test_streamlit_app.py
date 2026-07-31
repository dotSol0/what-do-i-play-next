from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parents[1] / "frontend" / "app" / "streamlit.py")

# AppTest (streamlit==1.52.2) can't serialize widget state for a rerun when a
# single-selection st.segmented_control is on the page: ButtonGroup.value
# (streamlit/testing/v1/element_tree.py) is typed/implemented as a list, but
# selection_mode="single" stores a scalar in session_state, so `for v in
# self.value` iterates the string's characters instead of treating it as one
# selection. This app uses two such widgets (`mode`, `duration_selection`),
# so any click-triggered rerun hits it regardless of what's clicked.
_SEGMENTED_CONTROL_RERUN_BUG = "streamlit AppTest can't rerun past a single-mode segmented_control widget (see comment above)"


def test_app_loads_without_error():
    at = AppTest.from_file(APP_PATH)
    at.run()
    assert not at.exception


@pytest.mark.skip(reason=_SEGMENTED_CONTROL_RERUN_BUG)
def test_submit_returns_results():
    at = AppTest.from_file(APP_PATH)
    at.run()

    at.button[1].click().run()  # "Click to Submit"

    assert not at.exception
    assert "results" in at.session_state
    assert len(at.session_state["results"]) > 0
