import streamlit as st
import pandas as pd

from datetime import date

from database import get_db, init_db

from models import (
    Application,
    Company,
    Interview
)


st.set_page_config(
    page_title="Interviews | JobTrack",
    page_icon="🎯",
    layout="wide"
)

init_db()


st.title("🎯 Interview Tracker")

st.caption(
    "Schedule and track interview rounds."
)


db = get_db()


# APPLICATIONS

applications = (
    db.query(
        Application,
        Company
    )
    .join(
        Company,
        Application.company_id ==
        Company.id
    )
    .order_by(
        Application.application_date.desc()
    )
    .all()
)


if not applications:

    st.warning(
        "Please create an application first."
    )

    if st.button(
        "Go to Applications"
    ):

        st.switch_page(
            "pages/2_Applications.py"
        )

    db.close()

    st.stop()


application_options = {}


for application, company in applications:

    label = (
        f"{company.name} - "
        f"{application.job_title} "
        f"(ID: {application.id})"
    )

    application_options[
        label
    ] = application.id


# ADD INTERVIEW

st.subheader("➕ Add Interview")


with st.form("interview_form"):

    selected_application = st.selectbox(
        "Application",
        list(application_options.keys())
    )


    col1, col2 = st.columns(2)


    with col1:

        round_number = st.number_input(
            "Round Number",
            min_value=1,
            value=1,
            step=1
        )

        interview_type = st.selectbox(
            "Interview Type",
            [
                "HR",
                "Technical",
                "Coding",
                "Managerial",
                "Behavioral",
                "System Design",
                "Other"
            ]
        )

        interviewer = st.text_input(
            "Interviewer"
        )


    with col2:

        interview_date = st.date_input(
            "Interview Date",
            value=date.today()
        )

        status = st.selectbox(
            "Status",
            [
                "Scheduled",
                "Completed",
                "Passed",
                "Failed",
                "Cancelled"
            ]
        )


    notes = st.text_area(
        "Notes"
    )


    submit = st.form_submit_button(
        "Save Interview",
        use_container_width=True
    )


    if submit:

        interview = Interview(

            application_id=
                application_options[
                    selected_application
                ],

            round_number=
                round_number,

            interview_type=
                interview_type,

            interview_date=
                interview_date,

            status=
                status,

            interviewer=
                interviewer.strip(),

            notes=
                notes.strip()
        )


        db.add(interview)

        db.commit()

        st.success(
            "Interview saved successfully!"
        )

        st.rerun()


st.divider()


# INTERVIEW LIST

st.subheader("📋 Interview Schedule")


interviews = (
    db.query(
        Interview,
        Application,
        Company
    )
    .join(
        Application,
        Interview.application_id ==
        Application.id
    )
    .join(
        Company,
        Application.company_id ==
        Company.id
    )
    .order_by(
        Interview.interview_date
    )
    .all()
)


if interviews:

    rows = []

    for interview, application, company in interviews:

        rows.append({

            "ID":
                interview.id,

            "Company":
                company.name,

            "Position":
                application.job_title,

            "Round":
                interview.round_number,

            "Type":
                interview.interview_type,

            "Date":
                interview.interview_date,

            "Status":
                interview.status,

            "Interviewer":
                interview.interviewer or "-"
        })


    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No interviews scheduled."
    )


# DELETE INTERVIEW

if interviews:

    st.divider()

    st.subheader("🗑️ Delete Interview")


    options = {}


    for interview, application, company in interviews:

        label = (
            f"{company.name} - "
            f"{application.job_title} - "
            f"Round {interview.round_number} "
            f"(ID: {interview.id})"
        )

        options[label] = interview.id


    selected = st.selectbox(
        "Select interview",
        list(options.keys())
    )


    if st.button(
        "Delete Interview",
        type="secondary"
    ):

        interview = db.get(
            Interview,
            options[selected]
        )


        if interview:

            db.delete(interview)

            db.commit()

            st.success(
                "Interview deleted."
            )

            st.rerun()


db.close()