import pandas as pd
import pytest

from ml.inference.predict_piece import predict_recommendations, _compute_score


def make_row(**kwargs):
    """Helper to construct a 1-row DataFrame/Series with default fields."""
    base = {
        "Title": "foo",
        "Composer": "Bar",
        "Key": "C",
        "Piece Style": "romantic",
        "Year": 1900,
        "Instrumentation": "piano",
        "num_downloads": 10,
        "Permlink": "p1",
    }
    base.update(kwargs)
    return pd.Series(base)


def test_compute_score_matching_fields():
    target = make_row()
    # same values should yield the sum of all biases
    assert _compute_score(target, target) == (
        3 + 4 + 3 + 2
    )

    # mismatch composer only
    alt = target.copy()
    alt["Composer"] = "Different"
    assert _compute_score(alt, target) == (4 + 3 + 2)

    # year outside window
    alt = target.copy()
    alt["Year"] = 2005
    assert _compute_score(alt, target) == (3 + 4 + 3)


def test_predict_with_instrumentation_fallback():
    df = pd.DataFrame([
        make_row(Title="a", Instrumentation="violin", Permlink="p1"),
        make_row(Title="b", Instrumentation="piano", Permlink="p2"),
        make_row(Title="c", Instrumentation="flute", Permlink="p3"),
    ])
    # choose a target that isn't actually in df by giving a new permlink
    target = make_row(Instrumentation="harpsichord", Permlink="pX")

    # none share "harpsichord" -> fallback should return full set
    result = predict_recommendations(target, df)
    assert set(result["Title"]) == {"a", "b", "c"}

    # if we ask for piano target, we should only see "b"
    target2 = make_row(Instrumentation="piano")
    result2 = predict_recommendations(target2, df)
    assert list(result2["Title"]) == ["b"]


def test_tiebreaker_by_downloads():
    base = make_row(Instrumentation="piano", Permlink="p0")
    df = pd.DataFrame([
        base,
        make_row(Title="low", num_downloads=1, Permlink="p1"),
        make_row(Title="high", num_downloads=100, Permlink="p2"),
    ])
    # all share same composer/key/style/year so score equal; order by downloads
    recs = predict_recommendations(base, df)
    titles = list(recs["Title"])
    # expect 'high' then either 'foo' or 'low' depending on how duplicates handled
    assert titles[0] == "high"
    assert len(titles) == 2 or len(titles) == 3


def test_limits_top_n():
    df = pd.DataFrame([make_row(Title=str(i), Permlink=f"p{i}") for i in range(5)])
    target = make_row(Instrumentation="piano")
    small = predict_recommendations(target, df, top_n=2)
    assert len(small) == 2


def test_filter_only_target_fallback():
    # when the instrumentation query selects only the target row, we should
    # fallback to the full dataset (minus the target) rather than returning
    # an empty frame.
    df = pd.DataFrame([
        make_row(Title="x", Instrumentation="piano", Permlink="p0"),
        make_row(Title="y", Instrumentation="violin", Permlink="p1"),
    ])
    target = make_row(Instrumentation="piano", Permlink="p0")
    recs = predict_recommendations(target, df)
    # should see the other row "y" despite the initial filter only matching
    # the target itself
    assert list(recs["Title"]) == ["y"]
