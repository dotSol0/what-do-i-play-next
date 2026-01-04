import pandas as pd
import numpy as np

def time_period_filter(time_period, df):
    if not time_period:
        return df.copy()
    df_filtered = df.copy()
    df_filtered = df_filtered[
        df_filtered["Piece Style"].astype(str).str.contains(time_period, case=False, na=False)
    ]
    return df_filtered

def instrumentation_query(instrument, df):
    # No instrument selected -> no filter
    if not instrument:
        return df.copy()

    # Normalize to list of instruments
    if isinstance(instrument, str):
        instruments = [instrument.strip().lower()]
    else:
        instruments = [str(i).strip().lower() for i in instrument]

    def match(instr_string):
        if not isinstance(instr_string, str):
            return False
        parts = [p.strip().lower() for p in instr_string.split(",")]
        for inst in instruments:
            if inst in parts:
                return True
        return False

    return df[df["Instrumentation"].apply(match)]



def key_query(key, df):
    # No key selected -> no filter
    if not key:
        return df.copy()

    # If list, combine masks
    if isinstance(key, list):
        if len(key) == 0:
            return df.copy()
        mask = pd.Series(False, index=df.index)
        for k in key:
            mask = mask | df["Key"].astype(str).str.contains(str(k), case=False, na=False)
        return df[mask]

    df_filtered = df.copy()
    df_filtered = df_filtered[
        df_filtered["Key"].astype(str).str.contains(str(key), case=False, na=False)
    ]
    return df_filtered

def mode_query(mode, df):
    # If user selected "All" or nothing, don't filter
    if not mode or mode == "All":
        return df.copy()

    # Accept list or single string
    if isinstance(mode, list):
        if len(mode) == 0:
            return df.copy()
        mask = pd.Series(False, index=df.index)
        for m in mode:
            mask = mask | df["Key"].astype(str).str.contains(str(m), case=False, na=False)
        return df[mask]

    df_filtered = df.copy()
    df_filtered = df_filtered[
        df_filtered["Key"].astype(str).str.contains(str(mode), case=False, na=False)
    ]
    return df_filtered

def year_query(start_year, end_year, df):
    df_filtered = df.copy()
    df_filtered = df_filtered[
        df_filtered["Year"].between(int(start_year), int(end_year))
    ]
    return df_filtered

def duration_range_query(start_duration, end_duration, df):
    if start_duration is not None and end_duration is not None:
        df_filtered = df.copy()
        df_filtered = df_filtered[
            df_filtered["Average Duration"].between(int(start_duration), int(end_duration))
        ]
        return df_filtered
    return df

def duration_query(start_duration, df):
    # Return rows roughly around the selected duration (±1)
    start = int(start_duration)
    low = max(0, start - 1)
    high = start + 1
    df_filtered = df.copy()
    if start_duration is not None:
        df_filtered = df_filtered[
            df_filtered["Average Duration"].between(low, high)
        ]
    return df_filtered


def baseline_query(query, df):
    # Ensure `df` is a pandas DataFrame (some callers may pass a list)
    if not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("Error with dataset: " \
            "`df` must be a pandas DataFrame or convertible to one")

    df_filtered = df.copy()
    # query layout: [time_period, instrument, key, mode, start_year, end_year, start_duration, end_duration]
    # Only apply filters when the query item is truthy (non-empty list/None)
    if query[1]:
        df_filtered = instrumentation_query(query[1], df_filtered)
    if query[6] is not None:
        if query[7] is not None:
            df_filtered = duration_range_query(query[6], query[7], df_filtered)
        else:
            df_filtered = duration_query(query[6], df_filtered)
    if query[2]:
        df_filtered = key_query(query[2], df_filtered)
    if query[3] and query[3] != "All":
        df_filtered = mode_query(query[3], df_filtered)
    if query[4] is not None:
        df_filtered = year_query(query[4], query[5], df_filtered)
    if query[0]:
        df_filtered = time_period_filter(query[0], df_filtered)
        
    
    
    sorted_df = df_filtered.sort_values(by='num_downloads', ascending = False)
    return sorted_df

