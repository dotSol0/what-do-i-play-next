Built an end-to-end music recommendation system using IMSLP metadata, featuring content-based similarity search and LLM-assisted musical descriptions.

# What Do I Play Next?

A classical music recommender that suggests repertoire based on
instrumentation, era, key, and popularity. 

### Features (v0)
- Streamlit frontend
- Baseline filtering recommender
- dataset (currently contains 700 largely unknown pieces, will be expanded to include a sizable chunk of the IMSLP database)

### Coming Soon...
- A solo tag that will give you all pieces in the base that has that instrument + piano accompaniment
- A backfilled recommender: Type in the last piece you've played, and you will be given pieces similar to it! Plus, you'll be given pieces more difficult than it
- A user rating system: Rate the quality of the musical selections! Would you recommend it to other musicians?
- Light/dark mode

### Run locally
```bash
pip install -r requirements.txt
streamlit run frontend/app/streamlit.py
