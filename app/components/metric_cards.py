"""Reusable metric cards for dashboard sections."""
from __future__ import annotations

from typing import Any

import streamlit as st


def render_metric_cards(metrics: list[dict[str, Any]]) -> None:
    """Render a row of metric cards.

    Each metric dict should contain: label, value, delta, help, positive.
    """
    cols = st.columns(len(metrics))
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            st.metric(
                label=metric.get("label", "Metric"),
                value=metric.get("value", "--"),
                delta=metric.get("delta", None),
                help=metric.get("help", None),
            )
