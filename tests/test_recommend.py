import pandas as pd
from ml.inference.recommend import instrumentation_query


def test_instrumentation_exact_match():
    df = pd.DataFrame({
        
