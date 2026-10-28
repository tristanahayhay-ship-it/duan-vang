"""Documentation for the new project architecture."""

# Duan Vang Dashboard

This project has been reorganized into a cleaner multi-module Streamlit architecture.

## Structure

- `app/main.py`: application entry point
- `app/config.py`: configuration and defaults
- `app/data/`: raw data fetchers
- `app/services/`: business logic and orchestration
- `app/pages/`: page modules
- `app/components/`: reusable UI widgets

## Run locally

```bash
python -m streamlit run streamlit_app.py
```

## Next steps

1. Split the original large dashboard into dedicated pages.
2. Add macro, news, AI, and demo-trade modules.
3. Integrate database persistence and alerts.
4. Move all external API logic behind service/data layers.
