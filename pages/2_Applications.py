import streamlit as st
import pandas as pd

from datetime import date

from database import get_db, init_db

from models import (
    Company,
    Application
)


st.set_page_config(
    page_title="Applications | JobTrack",
    page_icon="💼",
    layout="wide"
)

init_db()


st.title("💼 Applications")

st.caption(
    "Track all your job applications."
)


db = get_db()


# COMPANIES

companies = (
    db.query(Company)
    .order_by(Company.name)
    .all()
)


if not companies:

    st.warning(
        "Please add a company first."
    )

    if st.button("Go to Companies"):

        st.switch_page(
            "pages/1_Companies.py"
        )

    db.close()

    st.stop()


company_options = {
    company.name: company.id
    for company in companies
}



# ADD APPLICATION

st.subheader("➕ Add Application")


with st.form("application_form"):

    col1, col2 = st.columns(2)


    with col1:

        company_name = st.selectbox(
            "Company",
            list(company_options.keys())
        )

        job_title = st.text_input(
            "Job Title *"
        )

        job_type = st.selectbox(
            "Job Type",
            [
                "Full Time",
                "Part Time",
                "Internship",
                "Contract"
            ]
        )

        location = st.text_input(
            "Location"
        )


    with col2:

        application_date = st.date_input(
            "Application Date",
            value=date.today()
        )

        status = st.selectbox(
            "Status",
            [
                "Applied",
                "Screening",
                "Interview",
                "Offer",
                "Rejected",
                "Withdrawn"
            ]
        )

        salary = st.number_input(
            "Expected Salary",
            min_value=0.0,
            step=10000.0
        )

        job_url = st.text_input(
            "Job URL"
        )


    notes = st.text_area(
        "Notes"
    )


    submit = st.form_submit_button(
        "Save Application",
        use_container_width=True
    )


    if submit:

        if not job_title.strip():

            st.error(
                "Job title is required."
            )

        else:

            application = Application(

                company_id=
                    company_options[
                        company_name
                    ],

                job_title=
                    job_title.strip(),

                job_type=
                    job_type,

                location=
                    location.strip(),

                application_date=
                    application_date,

                status=
                    status,

                salary=
                    salary,

                job_url=
                    job_url.strip(),

                notes=
                    notes.strip()
            )


            db.add(application)

            db.commit()

            st.success(
                "Application saved successfully!"
            )

            st.rerun()


st.divider()

# SEARCH

st.subheader("🔎 Search")


search = st.text_input(
    "Search by company, role or location"
)


query = (
    db.query(
        Application,
        Company
    )
    .join(
        Company,
        Application.company_id ==
        Company.id
    )
)


if search:

    search_term = f"%{search}%"

    query = query.filter(

        (Company.name.ilike(search_term)) |

        (
            Application.job_title
            .ilike(search_term)
        ) |

        (
            Application.location
            .ilike(search_term)
        )
    )


results = (
    query
    .order_by(
        Application.application_date.desc()
    )
    .all()
)


# DISPLAY


st.subheader("📋 Applications")


if results:

    rows = []

    for application, company in results:

        rows.append({

            "ID":
                application.id,

            "Company":
                company.name,

            "Job Title":
                application.job_title,

            "Location":
                application.location or "-",

            "Date":
                application.application_date,

            "Status":
                application.status,

            "Salary":
                (
                    f"₹{application.salary:,.0f}"
                    if application.salary
                    else "-"
                )
        })


    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No applications found."
    )


# DELETE

all_applications = (
    db.query(Application)
    .order_by(Application.id)
    .all()
)


if all_applications:

    st.divider()

    st.subheader("🗑️ Delete Application")


    options = {}

    for application in all_applications:

        company = db.get(
            Company,
            application.company_id
        )

        label = (
            f"{company.name} - "
            f"{application.job_title} "
            f"(ID: {application.id})"
        )

        options[label] = application.id


    selected = st.selectbox(
        "Select application",
        list(options.keys())
    )


    if st.button(
        "Delete Application",
        type="secondary"
    ):

        application = db.get(
            Application,
            options[selected]
        )


        if application:

            db.delete(application)

            db.commit()

            st.success(
                "Application deleted."
            )

            st.rerun()


db.close()