import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ClinicFlow",
    page_icon="🏥",
    layout="wide"
)

if "patients" not in st.session_state:
    st.session_state.patients = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Patients", "Appointments"]
)

if menu == "Dashboard":
    st.title("🏥 ClinicFlow Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Total Patients", len(st.session_state.patients))

    with col2:
        st.metric("📅 Total Appointments", len(st.session_state.appointments))

    with col3:
        st.metric("👨‍⚕️ Doctors", 1)

    st.divider()
    st.subheader("Recent Patients")

    if st.session_state.patients:
        st.dataframe(pd.DataFrame(st.session_state.patients), use_container_width=True)
    else:
        st.info("No patients available yet.")

elif menu == "Patients":
    st.title("👨‍⚕️ Patient Management")

    with st.form("patient_form", clear_on_submit=True):
        name = st.text_input("Patient Name")
        age = st.number_input("Patient Age", min_value=0, max_value=120)
        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button("Add Patient")

        if submitted:
            if name.strip() == "" or phone.strip() == "":
                st.error("Please enter patient name and phone number.")
            else:
                patient_id = len(st.session_state.patients) + 1

                st.session_state.patients.append({
                    "ID": patient_id,
                    "Name": name,
                    "Age": age,
                    "Phone": phone
                })

                st.success("Patient Added Successfully!")

    st.divider()
    st.subheader("Patient Records")

    if st.session_state.patients:
        st.dataframe(pd.DataFrame(st.session_state.patients), use_container_width=True)

        patient_ids = [patient["ID"] for patient in st.session_state.patients]
        delete_id = st.selectbox("Select Patient ID to delete", patient_ids)

        if st.button("Delete Selected Patient"):
            st.session_state.patients = [
                patient for patient in st.session_state.patients
                if patient["ID"] != delete_id
            ]
            st.success("Patient Deleted!")
            st.rerun()
    else:
        st.info("No patients added yet.")

elif menu == "Appointments":
    st.title("📅 Appointment Booking")

    if not st.session_state.patients:
        st.warning("Add a patient first before booking an appointment.")
    else:
        patient_names = [patient["Name"] for patient in st.session_state.patients]

        with st.form("appointment_form", clear_on_submit=True):
            patient_name = st.selectbox("Select Patient", patient_names)
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")

            booked = st.form_submit_button("Book Appointment")

            if booked:
                appointment_id = len(st.session_state.appointments) + 1

                st.session_state.appointments.append({
                    "ID": appointment_id,
                    "Patient": patient_name,
                    "Date": str(appointment_date),
                    "Time": str(appointment_time)
                })

                st.success(f"Appointment booked for {patient_name}!")

    st.divider()
    st.subheader("Appointment Records")

    if st.session_state.appointments:
        st.dataframe(
            pd.DataFrame(st.session_state.appointments),
            use_container_width=True
        )
    else:
        st.info("No appointments booked yet.")