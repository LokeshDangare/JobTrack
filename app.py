import streamlit as st
import pandas as pd
import plotly.express as px

from database import init_db, get_db

from utils.queries import (
    get_dashboard_statistics,
    get_status_counts
)


# PAGE CONFIG

st.set_page_config(
    page_title="JobTrack",
    page_icon="💼",
    layout="wide"
)


# INITIALIZE DATABASE

init_db()


# CUSTOM CSS
st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# SIDEBAR
with st.sidebar:

    st.title("💼 JobTrack")

    st.write(
        "Your Job Application Command Center"
    )

    st.divider()

    st.info(
        """
        Track companies,
        applications and
        interview rounds
        in one place.
        """
    )

    st.divider()

    st.caption(
        "Streamlit + MySQL + SQLAlchemy"
    )


# HEADER

st.markdown(
    '<div class="main-title">💼 JobTrack</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal job application command center'
    '</div>',
    unsafe_allow_html=True
)

# DATABASE

db = get_db()

stats = get_dashboard_statistics(db)

# KPI CARDS

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Applications",
    stats["applications"]
)

col2.metric(
    "Companies",
    stats["companies"]
)

col3.metric(
    "Interviews",
    stats["interviews"]
)

col4.metric(
    "Offers",
    stats["offers"]
)

col5.metric(
    "Rejected",
    stats["rejected"]
)


st.divider()


# APPLICATION PIPELINE

st.subheader("📌 Application Pipeline")

status_data = get_status_counts(db)


if status_data:

    df = pd.DataFrame(
        status_data,
        columns=[
            "Status",
            "Applications"
        ]
    )

    fig = px.bar(
        df,
        x="Status",
        y="Applications",
        text="Applications",
        title="Applications by Status"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No applications available. "
        "Add your first application."
    )


st.divider()


# QUICK ACTIONS

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)


with col1:

    st.write("### 🏢")

    st.write(
        "Add a company"
    )

    if st.button(
        "Companies",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Companies.py"
        )


with col2:

    st.write("### 💼")

    st.write(
        "Track an application"
    )

    if st.button(
        "Applications",
        use_container_width=True
    ):

        st.switch_page(
            "pages/2_Applications.py"
        )


with col3:

    st.write("### 🎯")

    st.write(
        "Manage interviews"
    )

    if st.button(
        "Interviews",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Interviews.py"
        )


db.close()