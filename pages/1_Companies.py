import streamlit as st
import pandas as pd

from database import get_db, init_db
from models import Company


st.set_page_config(
    page_title="Companies | JobTrack",
    page_icon="🏢",
    layout="wide"
)

init_db()


st.title("🏢 Companies")

st.caption(
    "Manage companies you are applying to."
)


db = get_db()


# ADD COMPANY

st.subheader("➕ Add Company")


with st.form("company_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Company Name *"
        )

        industry = st.text_input(
            "Industry"
        )

    with col2:

        location = st.text_input(
            "Location"
        )

        website = st.text_input(
            "Website"
        )

    submit = st.form_submit_button(
        "Add Company",
        use_container_width=True
    )


    if submit:

        if not name.strip():

            st.error(
                "Company name is required."
            )

        else:

            existing = (
                db.query(Company)
                .filter(
                    Company.name == name.strip()
                )
                .first()
            )

            if existing:

                st.warning(
                    "This company already exists."
                )

            else:

                company = Company(
                    name=name.strip(),
                    industry=industry.strip(),
                    location=location.strip(),
                    website=website.strip()
                )

                db.add(company)

                db.commit()

                st.success(
                    "Company added successfully!"
                )

                st.rerun()


st.divider()


# COMPANY LIST


st.subheader("📋 Companies")


companies = (
    db.query(Company)
    .order_by(Company.name)
    .all()
)


if companies:

    rows = []

    for company in companies:

        rows.append({

            "ID": company.id,

            "Company": company.name,

            "Industry":
                company.industry or "-",

            "Location":
                company.location or "-",

            "Website":
                company.website or "-"
        })


    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No companies found."
    )


# DELETE

if companies:

    st.divider()

    st.subheader("🗑️ Delete Company")

    options = {
        f"{c.name} (ID: {c.id})":
        c.id
        for c in companies
    }

    selected = st.selectbox(
        "Select company",
        list(options.keys())
    )


    if st.button(
        "Delete Company",
        type="secondary"
    ):

        company = db.get(
            Company,
            options[selected]
        )

        if company:

            db.delete(company)

            db.commit()

            st.success(
                "Company deleted."
            )

            st.rerun()


db.close()