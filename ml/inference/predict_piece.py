import pandas as pd
from typing import Optional

from ml.inference.recommend import instrumentation_query


# constants for bias weights
_COMPOSER_BIAS = 3
_KEY_BIAS = 4
_STYLE_BIAS = 3
_YEAR_BIAS = 2
_YEAR_WINDOW = 100  # years either side


def _compute_score(row: pd.Series, target: pd.Series) -> int:
    """Return an integer score representing similarity between *row* and *target*.

    The score is the sum of the additive biases described in the project
    requirements:

    * +3 if ``Composer`` is equal
    * +4 if ``Key`` is equal
    * +3 if ``Piece Style`` is equal
    * +2 if ``Year`` is within \u00b1100 years of the target's year

    Any missing fields are treated as ``False`` (no bias added).
    """
    score = 0

    if pd.notna(row.get("Composer")) and pd.notna(target.get("Composer")):
        if str(row["Composer"]).strip().lower() == str(target["Composer"]).strip().lower():
            score += _COMPOSER_BIAS

    if pd.notna(row.get("Key")) and pd.notna(target.get("Key")):
        if str(row["Key"]).strip().lower() == str(target["Key"]).strip().lower():
            score += _KEY_BIAS

    if pd.notna(row.get("Piece Style")) and pd.notna(target.get("Piece Style")):
        if str(row["Piece Style"]).strip().lower() == str(target["Piece Style"]).strip().lower():
            score += _STYLE_BIAS

    # year comparison: we expect normalized integer year in the "Year" column
    try:
        y_target = int(target.get("Year"))
        y_row = int(row.get("Year"))
    except Exception:
        y_target = None
        y_row = None

    if y_target is not None and y_row is not None:
        if abs(y_target - y_row) <= _YEAR_WINDOW:
            score += _YEAR_BIAS

    return score


def predict_recommendations(target: pd.Series,
                            df: pd.DataFrame,
                            top_n: Optional[int] = None) -> pd.DataFrame:
    """Return a ranked set of pieces similar to ``target``.

    The algorithm follows these steps:

    1. make a copy of ``df`` to avoid mutating the caller's data.
    2. if ``target`` has a non-empty instrumentation value, filter the
       copy to rows that share at least one instrument using the helper
       from :mod:`ml.inference.recommend`.  If the filtered frame is empty,
       fall back to the unfiltered copy.
    3. compute a bias score for every candidate row relative to ``target``
       using :func:`_compute_score`.
    4. sort by the score (descending) and then by ``num_downloads``
       (descending) to break ties.
    5. optionally return only the first ``top_n`` rows; if ``top_n`` is
       ``None`` the entire scored frame is returned.

    The returned dataframe contains the original columns plus an appended
    ``similarity_score`` column.
    """
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    # step 1
    candidates = df.copy()

    # step 2: attempt instrumentation-based narrowing
    instr = target.get("Instrumentation")
    if instr:
        filtered = instrumentation_query(instr, candidates)
        if not filtered.empty:
            candidates = filtered
    # if nothing remained (empty frame) we keep original candidates

    # drop the target itself if it appears in the frame (by permalink or Title)
    if "Permlink" in target and "Permlink" in candidates:
        candidates = candidates[candidates["Permlink"] != target["Permlink"]]

    # If filtering + removal resulted in zero candidates, revert to the
    # full dataset (minus the target).  This handles situations where the
    # instrumentation query only matched the target row itself.
    if candidates.empty:
        candidates = df.copy()
        if "Permlink" in target and "Permlink" in candidates:
            candidates = candidates[candidates["Permlink"] != target["Permlink"]]

    # step 3: compute score
    candidates = candidates.copy()
    candidates["similarity_score"] = candidates.apply(
        lambda r: _compute_score(r, target), axis=1
    )

    # step 4: sort
    candidates = candidates.sort_values(
        by=["similarity_score", "num_downloads"],
        ascending=[False, False],
        na_position="last",
    )

    # step 5: limit
    if top_n is not None:
        candidates = candidates.head(top_n)

    return candidates
