import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ClinicFlow",
    page_icon="🏥",
    layout="wide"
)

# ---------------- STORAGE ----------------

if "patients" not in st.session_state:
    st.session_state.patients = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

# ---------------- SIDEBAR ----------------

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Patients", "Appointments"]
)

# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.title("🏥 ClinicFlow Dashboard")

    total_patients = len(st.session_state.patients)
    total_appointments = len(st.session_state.appointments)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Total Patients", total_patients)

    with col2:
        st.metric("📅 Appointments", total_appointments)

    with col3:
        st.metric("👨‍⚕️ Doctors", 1)

    st.divider()

    st.subheader("Recent Patients")

    if len(st.session_state.patients) > 0:
        st.dataframe(
            pd.DataFrame(st.session_state.patients),
            use_container_width=True
        )
    else:
        st.info("No patients available.")

# ---------------- PATIENTS ----------------

elif menu == "Patients":

    st.title("👨‍⚕️ Patient Management")

    name = st.text_input("Patient Name")
    age = st.number_input(
        "Patient Age",
        min_value=0,
        max_value=120
    )

    if st.button("Add Patient"):

        patient_id = len(st.session_state.patients) + 1

        st.session_state.patients.append({
            "ID": patient_id,
            "Name": name,
            "Age": age
        })

        st.success("Patient Added Successfully!")

    st.divider()

    st.subheader("Patient Records")

    if len(st.session_state.patients) > 0:

        df = pd.DataFrame(
            st.session_state.patients
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Delete Patient")

        patient_ids = [
            patient["ID"]
            for patient in st.session_state.patients
        ]

        delete_id = st.selectbox(
            "Select Patient ID",
            patient_ids
        )

        if st.button("Delete Patient"):

            st.session_state.patients = [
                patient
                for patient in st.session_state.patients
                if patient["ID"] != delete_id
            ]

            st.success("Patient Deleted!")

            st.rerun()

    else:
        st.info("No patients added yet.")

# ---------------- APPOINTMENTS ----------------

elif menu == "Appointments":

    st.title("📅 Appointment Booking")

    patient_name = st.text_input(
        "Patient Name"
    )

    appointment_date = st.date_input(
        "Appointment Date"
    )

    appointment_time = st.time_input(
        "Appointment Time"
    )

    if st.button("Book Appointment"):

        appointment_id = (
            len(st.session_state.appointments) + 1
        )

        st.session_state.appointments.append({
            "ID": appointment_id,
            "Patient": patient_name,
            "Date": appointment_date,
            "Time": appointment_time
        })

        st.success(
            f"Appointment booked for {patient_name}"
        )

    st.divider()

    st.subheader("Appointment Records")

    if len(st.session_state.appointments) > 0:

        st.dataframe(
            pd.DataFrame(
                st.session_state.appointments
            ),
            use_container_width=True
        )

    else:
        st.info("No appointments booked yet.")