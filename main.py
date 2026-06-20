patients = []

while True:
    print("\n===== Patient Management System =====")
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patient")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter patient name: ")
        age = input("Enter patient age: ")
        phone = input("Enter patient phone number: ")

        patient = {
            "name": name,
            "age": age,
            "phone": phone
        }

        patients.append(patient)

        print("Patient Registered Successfully!")

    elif choice == "2":
        print("\nPatient List:")

        for patient in patients:
            print(patient)

    elif choice == "3":
        search_name = input("Enter patient name to search: ")

        found = False

        for patient in patients:
            if patient["name"].lower() == search_name.lower():
                print("\nPatient Found!")
                print(patient)
                found = True

        if not found:
            print("Patient not found.")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")