import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_db, init_db

from models import (
    Company,
    Application,
    Interview
)


st.set_page_config(
    page_title="Analytics | JobTrack",
    page_icon="📊",
    layout="wide"
)

init_db()


st.title("📊 Career Analytics")

st.caption(
    "Analyze your job search performance."
)


db = get_db()


# APPLICATION DATA

results = (
    db.query(
        Application,
        Company
    )
    .join(
        Company,
        Application.company_id ==
        Company.id
    )
    .all()
)


if not results:

    st.info(
        "Add applications to see analytics."
    )

    db.close()

    st.stop()


rows = []


for application, company in results:

    rows.append({

        "Company":
            company.name,

        "Job Title":
            application.job_title,

        "Status":
            application.status,

        "Date":
            application.application_date,

        "Location":
            application.location or "Unknown",

        "Job Type":
            application.job_type
    })


df = pd.DataFrame(rows)


# KPI
total = len(df)

interviews = len(
    df[
        df["Status"] == "Interview"
    ]
)

offers = len(
    df[
        df["Status"] == "Offer"
    ]
)

rejected = len(
    df[
        df["Status"] == "Rejected"
    ]
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Applications",
    total
)

col2.metric(
    "Interviews",
    interviews
)

col3.metric(
    "Offers",
    offers
)

col4.metric(
    "Rejected",
    rejected
)


st.divider()


# STATUS

col1, col2 = st.columns(2)


with col1:

    status_counts = (
        df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Applications"
    ]


    fig = px.pie(
        status_counts,
        names="Status",
        values="Applications",
        title="Application Status"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# JOB TYPE

with col2:

    job_counts = (
        df["Job Type"]
        .value_counts()
        .reset_index()
    )

    job_counts.columns = [
        "Job Type",
        "Applications"
    ]


    fig = px.bar(
        job_counts,
        x="Job Type",
        y="Applications",
        text="Applications",
        title="Applications by Job Type"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# LOCATION

st.subheader("📍 Applications by Location")


location_counts = (
    df["Location"]
    .value_counts()
    .reset_index()
)

location_counts.columns = [
    "Location",
    "Applications"
]


fig = px.bar(
    location_counts,
    x="Location",
    y="Applications",
    text="Applications",
    title="Applications by Location"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# APPLICATION TIMELINE

st.subheader("📅 Application Timeline")


timeline = (
    df.groupby("Date")
    .size()
    .reset_index(
        name="Applications"
    )
)


fig = px.line(
    timeline,
    x="Date",
    y="Applications",
    markers=True,
    title="Applications Over Time"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# COMPANY ANALYSIS

st.subheader("🏢 Applications by Company")


company_counts = (
    df["Company"]
    .value_counts()
    .reset_index()
)

company_counts.columns = [
    "Company",
    "Applications"
]


st.dataframe(
    company_counts,
    use_container_width=True,
    hide_index=True
)


db.close()