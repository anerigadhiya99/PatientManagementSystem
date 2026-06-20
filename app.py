import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, time

st.set_page_config(
    page_title="ClinicFlow",
    page_icon="🏥",
    layout="wide"
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("clinicflow.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def get_patients():
    return pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )


def get_appointments():
    return pd.read_sql_query(
        "SELECT * FROM appointments",
        conn
    )


# ---------------- SIDEBAR ----------------

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Patients", "Appointments"]
)


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.title("🏥 ClinicFlow Dashboard")

    patients_df = get_patients()
    appointments_df = get_appointments()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Total Patients", len(patients_df))

    with col2:
        st.metric("📅 Total Appointments", len(appointments_df))

    with col3:
        st.metric("👨‍⚕️ Doctors", 1)

    st.divider()

    st.subheader("Recent Patients")

    if len(patients_df) > 0:
        st.dataframe(
            patients_df,
            use_container_width=True
        )
    else:
        st.info("No patients available yet.")


# ---------------- PATIENTS ----------------

elif menu == "Patients":

    st.title("👨‍⚕️ Patient Management")

    with st.form("patient_form", clear_on_submit=True):
        name = st.text_input("Patient Name")
        age = st.number_input(
            "Patient Age",
            min_value=0,
            max_value=120
        )
        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button("Add Patient")

        if submitted:
            if name.strip() == "" or phone.strip() == "":
                st.error("Please enter patient name and phone number.")
            else:
                cursor.execute(
                    """
                    INSERT INTO patients (name, age, phone)
                    VALUES (?, ?, ?)
                    """,
                    (name, age, phone)
                )

                conn.commit()

                st.success("Patient Added Successfully!")
                st.rerun()

    st.divider()

    st.subheader("Patient Records")

    patients_df = get_patients()

    if len(patients_df) > 0:
        st.dataframe(
            patients_df,
            use_container_width=True
        )

        patient_ids = patients_df["id"].tolist()

        delete_id = st.selectbox(
            "Select Patient ID to delete",
            patient_ids
        )

        if st.button("Delete Selected Patient"):
            cursor.execute(
                "DELETE FROM patients WHERE id = ?",
                (delete_id,)
            )

            conn.commit()

            st.success("Patient Deleted!")
            st.rerun()

    else:
        st.info("No patients added yet.")


# ---------------- APPOINTMENTS ----------------

elif menu == "Appointments":

    st.title("📅 Appointment Booking")

    patients_df = get_patients()

    if len(patients_df) == 0:
        st.warning("Add a patient first before booking an appointment.")

    else:
        patient_names = patients_df["name"].tolist()

        with st.form("appointment_form", clear_on_submit=True):
            patient_name = st.selectbox(
                "Select Patient",
                patient_names
            )

            appointment_date = st.date_input(
                "Appointment Date",
                value=date.today()
            )

            appointment_time = st.time_input(
                "Appointment Time",
                value=time(10, 0)
            )

            booked = st.form_submit_button("Book Appointment")

            if booked:
                cursor.execute(
                    """
                    INSERT INTO appointments
                    (patient_name, appointment_date, appointment_time)
                    VALUES (?, ?, ?)
                    """,
                    (
                        patient_name,
                        str(appointment_date),
                        str(appointment_time)
                    )
                )

                conn.commit()

                st.success(
                    f"Appointment booked for {patient_name}!"
                )

                st.rerun()

    st.divider()

    st.subheader("Appointment Records")

    appointments_df = get_appointments()

    if len(appointments_df) > 0:
        st.dataframe(
            appointments_df,
            use_container_width=True
        )
    else:
        st.info("No appointments booked yet.")