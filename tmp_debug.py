import pandas as pd
from ml.inference.predict_piece import predict_recommendations

def make_row(**kwargs):
    base = {
        'Title': 'foo',
        'Composer': 'Bar',
        'Key': 'C',
        'Piece Style': 'romantic',
        'Year': 1900,
        'Instrumentation': 'piano',
        'num_downloads': 10,
        'Permlink': 'p1',
    }
    base.update(kwargs)
    return pd.Series(base)

base = make_row(Instrumentation='piano')
df = pd.DataFrame([base, make_row(Title='low', num_downloads=1), make_row(Title='high', num_downloads=100)])

print('df:')
print(df)

recs = predict_recommendations(base, df)
print('recs length', len(recs))
print(recs[['Title','num_downloads']])
