import base64
import json
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeritageTech Lab | Ammonite 3D",
    page_icon="🏛️",
    layout="wide",
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "assets" / "model.glb"
RESULTS_PATH = BASE_DIR / "results.json"


# ============================================================
# TITLE
# ============================================================

st.title("🏛️ HeritageTech Lab #01")

st.subheader("From photographs to a 3D heritage object")

st.write(
    """
    This experiment demonstrates how a physical object can be
    reconstructed in 3D using only a collection of photographs.
    
    The object used in this experiment is an **ammonite fossil**.
    """
)


# ============================================================
# CHECK FILES
# ============================================================

st.write("### System check")

col1, col2 = st.columns(2)

with col1:
    if MODEL_PATH.exists():
        st.success(f"3D model found: {MODEL_PATH.name}")
        st.write(
            f"Model size: {MODEL_PATH.stat().st_size / 1024**2:.2f} MB"
        )
    else:
        st.error("model.glb not found in assets/")

with col2:
    if RESULTS_PATH.exists():
        st.success("results.json found")
    else:
        st.error("results.json not found")


# ============================================================
# LOAD RESULTS
# ============================================================

if RESULTS_PATH.exists():

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)

    st.write("### Reconstruction results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Images used",
        results.get("images_used", "—")
    )

    c2.metric(
        "Registered images",
        results.get("registered_images", "—")
    )

    coverage = results.get("registration_coverage")

    if coverage is not None:
        coverage = f"{coverage * 100:.1f}%"
    else:
        coverage = "—"

    c3.metric(
        "Coverage",
        coverage
    )

    c4.metric(
        "Sparse points",
        f"{results.get('sparse_points', 0):,}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Dense points",
        f"{results.get('dense_points', 0):,}"
    )

    c2.metric(
        "Mesh vertices",
        f"{results.get('mesh_vertices', 0):,}"
    )

    c3.metric(
        "Mesh faces",
        f"{results.get('mesh_faces', 0):,}"
    )


# ============================================================
# 3D MODEL
# ============================================================

st.divider()

st.write("## Interactive 3D reconstruction")

st.write(
    "Drag the model to rotate it and use the mouse wheel to zoom."
)


if MODEL_PATH.exists():

    model_bytes = MODEL_PATH.read_bytes()

    encoded_model = base64.b64encode(
        model_bytes
    ).decode("utf-8")

    model_uri = (
        "data:model/gltf-binary;base64,"
        + encoded_model
    )

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <script
            type="module"
            src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
        </script>

        <style>

            html,
            body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: #f3f3f3;
            }}

            model-viewer {{
                width: 100%;
                height: 650px;
                background: #f3f3f3;
            }}

        </style>

    </head>

    <body>

        <model-viewer

            src="{model_uri}"

            alt="3D reconstruction of an ammonite"

            camera-controls

            auto-rotate

            shadow-intensity="1"

            environment-image="neutral">

        </model-viewer>

    </body>

    </html>
    """

    st.iframe(
        html,
        width="stretch",
        height=680
    )

else:

    st.error(
        "The 3D model could not be loaded. "
        "Check that assets/model.glb exists."
    )


# ============================================================
# PIPELINE
# ============================================================

st.divider()

st.write("## Reconstruction pipeline")

st.markdown(
    """
    **1. Photographs**  
    Multiple overlapping photographs of the object.

    **2. Feature extraction**  
    Visual features detected with COLMAP / SIFT.

    **3. Feature matching**  
    Corresponding points identified between photographs.

    **4. Structure-from-Motion**  
    Camera positions and sparse 3D geometry reconstructed.

    **5. Multi-View Stereo**  
    Dense point cloud generated.

    **6. Surface reconstruction**  
    Dense cloud transformed into a polygonal mesh.
    """
)


# ============================================================
# CULTURAL HERITAGE
# ============================================================

st.divider()

st.write("## Why this matters for cultural heritage")

st.write(
    """
    Photogrammetry can support digital documentation,
    research, virtual exhibitions, education and
    remote access to cultural heritage objects.
    """
)


st.info(
    """
    Next step:
    transform this reconstructed object into an
    interactive web and AR museum experience.
    """
)


st.caption(
    "HeritageTech Lab · Experiment #01"
)
