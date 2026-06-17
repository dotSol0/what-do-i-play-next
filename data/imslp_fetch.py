import time
from imslp.interfaces import internal


def fetch_works(start: int = 0, count: int | None = None, batch: int = 5000, cache: bool = True):
    """Fetch works from IMSLP in safe chunks.

    - start: offset to begin fetching
    - count: total number of works to return (None => fetch until exhaustion)
    - batch: number of works to request per internal.list_works call
    - cache: pass cache=True to internal.list_works if desired

    Returns a list of work dicts.
    """
    works = []
    fetched = 0
    cur = start

    while True:
        to_get = batch if count is None else min(batch, count - fetched)
        if to_get <= 0:
            break

        chunk = internal.list_works(start=cur, count=to_get, cache=cache)
        print(f"start={cur} count={to_get} returned {len(list(chunk))} results")

        # Ensure we have a concrete list
        try:
            length = len(chunk)
        except TypeError:
            chunk = list(chunk)
            length = len(chunk)

        if not chunk:
            break

        works.extend(chunk)
        fetched += length
        cur += length

        if count is not None and fetched >= count:
            break

        # small pause between large list requests
        time.sleep(0.1)

    return works
