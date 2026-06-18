"""Local Streamlit demo for CogniPrint.

The demo computes profiles in the browser session only. It does not persist
input text, send it to model APIs, or make external network calls.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cogniprint.fingerprint import FEATURE_SPECS, CognitiveFingerprint  # noqa: E402


SAMPLE_CORPUS_DIR = ROOT / "datasets" / "public-benchmark-v1.1" / "raw"
FEATURE_LABELS = {
    "mean_word_length": "Mean word length",
    "type_token_ratio": "Type-token ratio",
    "char_entropy": "Character entropy",
    "word_entropy": "Word entropy",
    "punctuation_ratio": "Punctuation ratio",
    "uppercase_ratio": "Uppercase ratio",
    "mean_syllables_per_word": "Syllables per word",
    "char_bigram_uniqueness": "Char bigram uniqueness",
    "simpson_diversity": "Simpson diversity",
    "digit_token_ratio": "Digit token ratio",
    "mean_sentence_length_words": "Sentence length",
    "flesch_reading_ease": "Flesch reading ease",
}


def main() -> None:
    st.set_page_config(page_title="CogniPrint Demo", layout="wide")
    inject_styles()

    st.title("CogniPrint local demo")
    st.caption(
        "Compact statistical text profiles. Descriptive research interface; "
        "not a source, identity, AI-origin, legal, or forensic decision tool."
    )

    mode = st.radio("Mode", ["Single text", "Compare two texts"], horizontal=True)
    mean_vector = load_sample_corpus_mean()

    if mode == "Single text":
        render_single_text(mean_vector)
    else:
        render_comparison(mean_vector)

    st.divider()
    st.caption("Privacy: inputs are processed in this local Streamlit session and are not stored by this app.")


def render_single_text(mean_vector: np.ndarray | None) -> None:
    text = st.text_area(
        "Text sample",
        height=260,
        placeholder="Paste text here to compute a 12-coordinate cognitive fingerprint...",
    )
    if not st.button("Compute fingerprint", type="primary"):
        return
    if not text.strip():
        st.warning("Enter a text sample first.")
        return

    profile = build_profile(text)
    render_profile("Profile phi(T)", profile)
    render_summary_metrics(profile, mean_vector)


def render_comparison(mean_vector: np.ndarray | None) -> None:
    left, right = st.columns(2)
    with left:
        text_a = st.text_area("Text A", height=240, placeholder="First text sample...")
    with right:
        text_b = st.text_area("Text B", height=240, placeholder="Second text sample...")

    if not st.button("Compare profiles", type="primary"):
        return
    if not text_a.strip() or not text_b.strip():
        st.warning("Enter both text samples before comparing.")
        return

    profile_a = build_profile(text_a)
    profile_b = build_profile(text_b)
    distance = float(np.linalg.norm(profile_a["vector"] - profile_b["vector"]))
    cosine_similarity = 1.0 - CognitiveFingerprint.distance(
        profile_a["vector"].tolist(),
        profile_b["vector"].tolist(),
        metric="cosine",
    )

    metric_cols = st.columns(3)
    metric_cols[0].metric("Euclidean distance D2", f"{distance:.4f}")
    metric_cols[1].metric("Cosine similarity", f"{cosine_similarity:.4f}")
    if mean_vector is not None:
        centroid_delta = abs(
            float(np.linalg.norm(profile_a["vector"] - mean_vector))
            - float(np.linalg.norm(profile_b["vector"] - mean_vector))
        )
        metric_cols[2].metric("Corpus-mean distance delta", f"{centroid_delta:.4f}")
    else:
        metric_cols[2].metric("Corpus mean", "not available")

    col_a, col_b = st.columns(2)
    with col_a:
        render_profile("Text A profile", profile_a)
    with col_b:
        render_profile("Text B profile", profile_b)


def build_profile(text: str) -> dict[str, object]:
    fingerprint = CognitiveFingerprint(text)
    raw = fingerprint.feature_dict()
    normalized = fingerprint.normalized_feature_dict()
    vector = np.array(fingerprint.vector(normalized=True), dtype=float)
    return {
        "fingerprint": fingerprint,
        "raw": raw,
        "normalized": normalized,
        "vector": vector,
    }


def render_profile(title: str, profile: dict[str, object]) -> None:
    st.subheader(title)
    raw: dict[str, float] = profile["raw"]  # type: ignore[assignment]
    normalized: dict[str, float] = profile["normalized"]  # type: ignore[assignment]

    for spec in FEATURE_SPECS:
        value = float(normalized[spec.name])
        clamped = min(1.0, max(0.0, value))
        label = FEATURE_LABELS.get(spec.name, spec.name)
        st.markdown(
            f"""
            <div class="feature-row">
              <div class="feature-label">
                <span>{label}</span>
                <small>raw {raw[spec.name]:.4f} | norm {value:.4f}</small>
              </div>
              <div class="feature-track"><div class="feature-fill" style="width:{clamped * 100:.2f}%"></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_summary_metrics(profile: dict[str, object], mean_vector: np.ndarray | None) -> None:
    fingerprint: CognitiveFingerprint = profile["fingerprint"]  # type: ignore[assignment]
    vector: np.ndarray = profile["vector"]  # type: ignore[assignment]
    cols = st.columns(4)
    cols[0].metric("Tokens", len(fingerprint.words))
    cols[1].metric("Sentences", len(fingerprint.sentences))
    cols[2].metric("Unique words", len(set(fingerprint.words)))
    cols[3].metric("Vector norm", f"{float(np.linalg.norm(vector)):.4f}")

    if mean_vector is not None:
        st.metric("Distance from bundled sample-corpus mean", f"{float(np.linalg.norm(vector - mean_vector)):.4f}")
    else:
        st.info("Bundled sample-corpus mean is not available in this checkout.")


@st.cache_data(show_spinner=False)
def load_sample_corpus_mean() -> np.ndarray | None:
    if not SAMPLE_CORPUS_DIR.exists():
        return None
    vectors = []
    for path in sorted(SAMPLE_CORPUS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            vectors.append(CognitiveFingerprint(text).vector(normalized=True))
    if not vectors:
        return None
    return np.array(vectors, dtype=float).mean(axis=0)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
          .feature-row { margin: 0 0 0.72rem; }
          .feature-label {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            font-size: 0.88rem;
            margin-bottom: 0.18rem;
          }
          .feature-label small { color: rgba(49, 51, 63, 0.58); font-variant-numeric: tabular-nums; }
          .feature-track { height: 6px; background: rgba(49, 51, 63, 0.10); border-radius: 0; }
          .feature-fill { height: 6px; background: #111; border-radius: 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
