from connection import create_connection
from datetime import datetime


# =========================================================
# MAIN MENU
# =========================================================

while True:

    print("\n========================================")
    print("       VEHICLE RENTAL MANAGEMENT")
    print("==========================================")

    print("1. Customer Management")
    print("2. Vehicle Management")
    print("3. Rent a Vehicle")
    print("4. Return Vehicle")
    print("5. Payment Management")
    print("6. Maintenance Management")
    print("7. Search")
    print("8. Reports & Analytics")
    print("9. Exit")

    choice = input("\nEnter your choice: ")


    # =====================================================
    # 1. CUSTOMER MANAGEMENT
    # =====================================================

    if choice == "1":

        print("\n========== CUSTOMER MANAGEMENT ==========")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Rental History")

        customer_choice = input("\nEnter your choice: ")


        # -------------------------------------------------
        # ADD CUSTOMER
        # -------------------------------------------------

        if customer_choice == "1":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                full_name = input("Enter customer name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email: ")
                address = input("Enter address: ")
                license_number = input("Enter license number: ")

                query = """
                INSERT INTO customers
                (full_name, phone, email, address, license_number)
                VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    full_name,
                    phone,
                    email,
                    address,
                    license_number
                )

                cursor.execute(query, values)
                connection.commit()

                print("\nCustomer added successfully!")
                print("Customer ID:", cursor.lastrowid)

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # VIEW CUSTOMERS
        # -------------------------------------------------

        elif customer_choice == "2":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute("SELECT * FROM customers")

                customers = cursor.fetchall()

                print("\n========== ALL CUSTOMERS ==========")

                if not customers:

                    print("No customers found.")

                else:

                    for customer in customers:

                        print("----------------------------------------")
                        print("Customer ID   :", customer[0])
                        print("Name          :", customer[1])
                        print("Phone         :", customer[2])
                        print("Email         :", customer[3])
                        print("Address       :", customer[4])
                        print("License No.   :", customer[5])
                        print("Created At    :", customer[6])

                print("========================================")

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # SEARCH CUSTOMER
        # -------------------------------------------------

        elif customer_choice == "3":

            search = input(
                "\nEnter customer ID, name, phone or license number: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT *
                FROM customers
                WHERE CAST(customer_id AS CHAR) = %s
                   OR full_name LIKE %s
                   OR phone LIKE %s
                   OR license_number LIKE %s
                """

                value = "%" + search + "%"

                cursor.execute(
                    query,
                    (search, value, value, value)
                )

                customers = cursor.fetchall()

                if not customers:

                    print("\nCustomer not found.")

                else:

                    print("\n========== CUSTOMER DETAILS ==========")

                    for customer in customers:

                        print("----------------------------------------")
                        print("Customer ID :", customer[0])
                        print("Name        :", customer[1])
                        print("Phone       :", customer[2])
                        print("Email       :", customer[3])
                        print("Address     :", customer[4])
                        print("License No. :", customer[5])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # UPDATE CUSTOMER
        # -------------------------------------------------

        elif customer_choice == "4":

            customer_id = input("Enter customer ID to update: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM customers WHERE customer_id = %s",
                    (customer_id,)
                )

                customer = cursor.fetchone()

                if not customer:

                    print("\nCustomer not found.")

                else:

                    print("\nEnter new details:")

                    full_name = input("Enter new name: ")
                    phone = input("Enter new phone: ")
                    email = input("Enter new email: ")
                    address = input("Enter new address: ")
                    license_number = input(
                        "Enter new license number: "
                    )

                    query = """
                    UPDATE customers
                    SET full_name = %s,
                        phone = %s,
                        email = %s,
                        address = %s,
                        license_number = %s
                    WHERE customer_id = %s
                    """

                    values = (
                        full_name,
                        phone,
                        email,
                        address,
                        license_number,
                        customer_id
                    )

                    cursor.execute(query, values)
                    connection.commit()

                    print("\nCustomer updated successfully!")

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # DELETE CUSTOMER
        # -------------------------------------------------

        elif customer_choice == "5":

            customer_id = input("Enter customer ID to delete: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM customers WHERE customer_id = %s",
                    (customer_id,)
                )

                customer = cursor.fetchone()

                if not customer:

                    print("\nCustomer not found.")

                else:

                    confirm = input(
                        "Are you sure you want to delete this customer? (yes/no): "
                    )

                    if confirm.lower() == "yes":

                        cursor.execute(
                            "DELETE FROM customers WHERE customer_id = %s",
                            (customer_id,)
                        )

                        connection.commit()

                        print("\nCustomer deleted successfully!")

                    else:

                        print("\nDelete cancelled.")

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # RENTAL HISTORY
        # -------------------------------------------------

        elif customer_choice == "6":

            customer_id = input("Enter customer ID: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT
                    r.rental_id,
                    c.full_name,
                    v.vehicle_number,
                    v.brand,
                    v.model,
                    r.pickup_date,
                    r.return_date,
                    r.actual_return_date,
                    r.total_days,
                    r.total_amount,
                    r.rental_status
                FROM rentals r
                JOIN customers c
                    ON r.customer_id = c.customer_id
                JOIN vehicles v
                    ON r.vehicle_id = v.vehicle_id
                WHERE r.customer_id = %s
                ORDER BY r.rental_id DESC
                """

                cursor.execute(query, (customer_id,))

                rentals = cursor.fetchall()

                if not rentals:

                    print("\nNo rental history found.")

                else:

                    print("\n========== RENTAL HISTORY ==========")

                    for rental in rentals:

                        print("----------------------------------------")
                        print("Rental ID        :", rental[0])
                        print("Customer         :", rental[1])
                        print("Vehicle Number   :", rental[2])
                        print("Vehicle          :", rental[3], rental[4])
                        print("Pickup Date      :", rental[5])
                        print("Return Date      :", rental[6])
                        print("Actual Return    :", rental[7])
                        print("Total Days       :", rental[8])
                        print("Total Amount     :", rental[9])
                        print("Rental Status    :", rental[10])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        else:

            print("\nInvalid choice!")


    # =====================================================
    # 2. VEHICLE MANAGEMENT
    # =====================================================

    elif choice == "2":

        print("\n========== VEHICLE MANAGEMENT ==========")
        print("1. Add Vehicle")
        print("2. View All Vehicles")
        print("3. Available Vehicles")
        print("4. Search Vehicle")
        print("5. Update Vehicle")
        print("6. Delete Vehicle")
        print("7. Maintenance History")

        vehicle_choice = input("\nEnter your choice: ")


        # -------------------------------------------------
        # ADD VEHICLE
        # -------------------------------------------------

        if vehicle_choice == "1":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                vehicle_number = input("Enter vehicle number: ")
                vehicle_type = input("Enter vehicle type: ")
                brand = input("Enter brand: ")
                model = input("Enter model: ")
                year = int(input("Enter year: "))
                rent_per_day = float(
                    input("Enter rent per day: ")
                )

                query = """
                INSERT INTO vehicles
                (vehicle_number, vehicle_type, brand, model,
                 year, rent_per_day, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Available')
                """

                values = (
                    vehicle_number,
                    vehicle_type,
                    brand,
                    model,
                    year,
                    rent_per_day
                )

                cursor.execute(query, values)
                connection.commit()

                print("\nVehicle added successfully!")
                print("Vehicle ID:", cursor.lastrowid)

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # VIEW ALL VEHICLES
        # -------------------------------------------------

        elif vehicle_choice == "2":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute("SELECT * FROM vehicles")

                vehicles = cursor.fetchall()

                print("\n========== ALL VEHICLES ==========")

                if not vehicles:

                    print("No vehicles found.")

                else:

                    for vehicle in vehicles:

                        print("----------------------------------------")
                        print("Vehicle ID     :", vehicle[0])
                        print("Vehicle Number :", vehicle[1])
                        print("Type           :", vehicle[2])
                        print("Brand          :", vehicle[3])
                        print("Model          :", vehicle[4])
                        print("Year           :", vehicle[5])
                        print("Rent Per Day   :", vehicle[6])
                        print("Status         :", vehicle[7])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # AVAILABLE VEHICLES
        # -------------------------------------------------

        elif vehicle_choice == "3":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT *
                FROM vehicles
                WHERE status = 'Available'
                """

                cursor.execute(query)

                vehicles = cursor.fetchall()

                print("\n========== AVAILABLE VEHICLES ==========")

                if not vehicles:

                    print("No available vehicles.")

                else:

                    for vehicle in vehicles:

                        print("----------------------------------------")
                        print("Vehicle ID     :", vehicle[0])
                        print("Vehicle Number :", vehicle[1])
                        print("Type           :", vehicle[2])
                        print("Brand          :", vehicle[3])
                        print("Model          :", vehicle[4])
                        print("Year           :", vehicle[5])
                        print("Rent Per Day   :", vehicle[6])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # SEARCH VEHICLE
        # -------------------------------------------------

        elif vehicle_choice == "4":

            search = input(
                "\nEnter vehicle number, brand, model or type: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                value = "%" + search + "%"

                query = """
                SELECT *
                FROM vehicles
                WHERE vehicle_number LIKE %s
                   OR vehicle_type LIKE %s
                   OR brand LIKE %s
                   OR model LIKE %s
                """

                cursor.execute(
                    query,
                    (value, value, value, value)
                )

                vehicles = cursor.fetchall()

                if not vehicles:

                    print("\nVehicle not found.")

                else:

                    print("\n========== VEHICLE DETAILS ==========")

                    for vehicle in vehicles:

                        print("----------------------------------------")
                        print("Vehicle ID     :", vehicle[0])
                        print("Vehicle Number :", vehicle[1])
                        print("Type           :", vehicle[2])
                        print("Brand          :", vehicle[3])
                        print("Model          :", vehicle[4])
                        print("Year           :", vehicle[5])
                        print("Rent Per Day   :", vehicle[6])
                        print("Status         :", vehicle[7])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # UPDATE VEHICLE
        # -------------------------------------------------

        elif vehicle_choice == "5":

            vehicle_id = input("Enter vehicle ID to update: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM vehicles WHERE vehicle_id = %s",
                    (vehicle_id,)
                )

                vehicle = cursor.fetchone()

                if not vehicle:

                    print("\nVehicle not found.")

                else:

                    vehicle_number = input(
                        "Enter new vehicle number: "
                    )

                    vehicle_type = input(
                        "Enter new vehicle type: "
                    )

                    brand = input("Enter new brand: ")
                    model = input("Enter new model: ")
                    year = int(input("Enter new year: "))

                    rent_per_day = float(
                        input("Enter new rent per day: ")
                    )

                    status = input(
                        "Enter status (Available/Rented/Maintenance): "
                    )

                    query = """
                    UPDATE vehicles
                    SET vehicle_number = %s,
                        vehicle_type = %s,
                        brand = %s,
                        model = %s,
                        year = %s,
                        rent_per_day = %s,
                        status = %s
                    WHERE vehicle_id = %s
                    """

                    values = (
                        vehicle_number,
                        vehicle_type,
                        brand,
                        model,
                        year,
                        rent_per_day,
                        status,
                        vehicle_id
                    )

                    cursor.execute(query, values)
                    connection.commit()

                    print("\nVehicle updated successfully!")

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # DELETE VEHICLE
        # -------------------------------------------------

        elif vehicle_choice == "6":

            vehicle_id = input("Enter vehicle ID to delete: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM vehicles WHERE vehicle_id = %s",
                    (vehicle_id,)
                )

                vehicle = cursor.fetchone()

                if not vehicle:

                    print("\nVehicle not found.")

                else:

                    if vehicle[7] == "Rented":

                        print(
                            "\nCannot delete a rented vehicle."
                        )

                    else:

                        confirm = input(
                            "Are you sure you want to delete this vehicle? (yes/no): "
                        )

                        if confirm.lower() == "yes":

                            cursor.execute(
                                "DELETE FROM vehicles WHERE vehicle_id = %s",
                                (vehicle_id,)
                            )

                            connection.commit()

                            print(
                                "\nVehicle deleted successfully!"
                            )

                        else:

                            print("\nDelete cancelled.")

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # MAINTENANCE HISTORY
        # -------------------------------------------------

        elif vehicle_choice == "7":

            vehicle_id = input("Enter vehicle ID: ")

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT
                    maintenance_id,
                    service_date,
                    description,
                    cost,
                    status
                FROM maintenance
                WHERE vehicle_id = %s
                ORDER BY service_date DESC
                """

                cursor.execute(query, (vehicle_id,))

                records = cursor.fetchall()

                if not records:

                    print("\nNo maintenance history found.")

                else:

                    print("\n========== MAINTENANCE HISTORY ==========")

                    for record in records:

                        print("----------------------------------------")
                        print("Maintenance ID :", record[0])
                        print("Service Date    :", record[1])
                        print("Description     :", record[2])
                        print("Cost            :", record[3])
                        print("Status          :", record[4])

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        else:

            print("\nInvalid choice!")


    # =====================================================
    # 3. RENT A VEHICLE
    # =====================================================

    elif choice == "3":

        connection = create_connection()
        cursor = connection.cursor()

        try:

            customer_id = input("Enter customer ID: ")
            vehicle_id = input("Enter vehicle ID: ")

            pickup_date = input(
                "Enter pickup date (YYYY-MM-DD): "
            )

            return_date = input(
                "Enter return date (YYYY-MM-DD): "
            )

            pickup = datetime.strptime(
                pickup_date,
                "%Y-%m-%d"
            )

            return_date_obj = datetime.strptime(
                return_date,
                "%Y-%m-%d"
            )

            total_days = (
                return_date_obj - pickup
            ).days

            if total_days <= 0:

                print(
                    "\nReturn date must be after pickup date."
                )

            else:

                # Check customer
                cursor.execute(
                    """
                    SELECT customer_id
                    FROM customers
                    WHERE customer_id = %s
                    """,
                    (customer_id,)
                )

                customer = cursor.fetchone()

                if not customer:

                    print("\nCustomer not found.")

                else:

                    # Get vehicle details
                    cursor.execute(
                        """
                        SELECT vehicle_number,
                               brand,
                               model,
                               rent_per_day,
                               status
                        FROM vehicles
                        WHERE vehicle_id = %s
                        """,
                        (vehicle_id,)
                    )

                    vehicle = cursor.fetchone()

                    if not vehicle:

                        print("\nVehicle not found.")

                    elif vehicle[4] != "Available":

                        print(
                            "\nVehicle is not available."
                        )
                        print(
                            "Current Status:",
                            vehicle[4]
                        )

                    else:

                        rent_per_day = float(vehicle[3])

                        rent_amount = (
                            total_days * rent_per_day
                        )

                        late_fee = 0

                        total_amount = (
                            rent_amount + late_fee
                        )

                        # Insert rental
                        query = """
                        INSERT INTO rentals
                        (
                            customer_id,
                            vehicle_id,
                            booking_date,
                            pickup_date,
                            return_date,
                            total_days,
                            rent_amount,
                            late_fee,
                            total_amount,
                            rental_status
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            CURDATE(),
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            'Active'
                        )
                        """

                        values = (
                            customer_id,
                            vehicle_id,
                            pickup_date,
                            return_date,
                            total_days,
                            rent_amount,
                            late_fee,
                            total_amount
                        )

                        cursor.execute(query, values)

                        rental_id = cursor.lastrowid

                        # Update vehicle status
                        cursor.execute(
                            """
                            UPDATE vehicles
                            SET status = 'Rented'
                            WHERE vehicle_id = %s
                            """,
                            (vehicle_id,)
                        )

                        connection.commit()

                        print(
                            "\n========== RENTAL DETAILS =========="
                        )

                        print("Rental ID      :", rental_id)
                        print("Customer ID    :", customer_id)
                        print("Vehicle        :", vehicle[0])
                        print(
                            "Vehicle        :",
                            vehicle[1],
                            vehicle[2]
                        )
                        print("Pickup Date    :", pickup_date)
                        print("Return Date    :", return_date)
                        print("Total Days     :", total_days)
                        print(
                            "Rent Per Day   :",
                            rent_per_day
                        )
                        print(
                            "Rent Amount    :",
                            rent_amount
                        )
                        print("Late Fee       :", late_fee)
                        print(
                            "Total Amount   :",
                            total_amount
                        )

                        print(
                            "Vehicle Status : Rented"
                        )

                        print(
                            "===================================="
                        )

        except Exception as e:

            connection.rollback()
            print("\nError:", e)

        finally:

            cursor.close()
            connection.close()


    # =====================================================
    # 4. RETURN VEHICLE
    # =====================================================

    elif choice == "4":

        connection = create_connection()
        cursor = connection.cursor()

        try:

            rental_id = input("Enter rental ID: ")

            actual_return_date = input(
                "Enter actual return date (YYYY-MM-DD): "
            )

            actual_date = datetime.strptime(
                actual_return_date,
                "%Y-%m-%d"
            )

            # Get rental details
            query = """
            SELECT
                rental_id,
                vehicle_id,
                return_date,
                rent_amount,
                late_fee,
                total_amount,
                rental_status
            FROM rentals
            WHERE rental_id = %s
            """

            cursor.execute(query, (rental_id,))

            rental = cursor.fetchone()

            if not rental:

                print("\nRental not found.")

            elif rental[6] == "Completed":

                print("\nThis rental is already completed.")

            else:

                vehicle_id = rental[1]
                original_return_date = rental[2]

                if isinstance(
                    original_return_date,
                    datetime
                ):

                    original_date = original_return_date

                else:

                    original_date = datetime.combine(
                        original_return_date,
                        datetime.min.time()
                    )

                late_days = (
                    actual_date - original_date
                ).days

                if late_days < 0:

                    late_days = 0

                # Get vehicle rent per day
                cursor.execute(
                    """
                    SELECT rent_per_day
                    FROM vehicles
                    WHERE vehicle_id = %s
                    """,
                    (vehicle_id,)
                )

                vehicle = cursor.fetchone()

                if vehicle:

                    rent_per_day = float(vehicle[0])

                else:

                    rent_per_day = 0

                # Late fee = 20% of rent per day
                late_fee_per_day = (
                    rent_per_day * 0.20
                )

                late_fee = (
                    late_days * late_fee_per_day
                )

                total_amount = (
                    float(rental[3]) + late_fee
                )

                # Update rental
                update_query = """
                UPDATE rentals
                SET actual_return_date = %s,
                    late_fee = %s,
                    total_amount = %s,
                    rental_status = 'Completed'
                WHERE rental_id = %s
                """

                cursor.execute(
                    update_query,
                    (
                        actual_return_date,
                        late_fee,
                        total_amount,
                        rental_id
                    )
                )

                # Make vehicle available
                cursor.execute(
                    """
                    UPDATE vehicles
                    SET status = 'Available'
                    WHERE vehicle_id = %s
                    """,
                    (vehicle_id,)
                )

                connection.commit()

                print(
                    "\n========== RETURN DETAILS =========="
                )

                print("Rental ID        :", rental_id)
                print(
                    "Original Return  :",
                    original_return_date
                )
                print(
                    "Actual Return    :",
                    actual_return_date
                )
                print("Late Days        :", late_days)
                print("Late Fee         :", late_fee)
                print(
                    "Updated Total    :",
                    total_amount
                )
                print(
                    "Vehicle Status   : Available"
                )

                print(
                    "===================================="
                )

        except Exception as e:

            connection.rollback()
            print("\nError:", e)

        finally:

            cursor.close()
            connection.close()


    # =====================================================
    # 5. PAYMENT MANAGEMENT
    # =====================================================

    elif choice == "5":

        connection = create_connection()
        cursor = connection.cursor()

        try:

            rental_id = input("Enter rental ID: ")

            # Get rental total
            cursor.execute(
                """
                SELECT total_amount
                FROM rentals
                WHERE rental_id = %s
                """,
                (rental_id,)
            )

            rental = cursor.fetchone()

            if not rental:

                print("\nRental not found.")

            else:

                total_amount = float(rental[0])

                # Get previous payments
                cursor.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0)
                    FROM payments
                    WHERE rental_id = %s
                    AND payment_status != 'Cancelled'
                    """,
                    (rental_id,)
                )

                previous_payment = float(
                    cursor.fetchone()[0]
                )

                print(
                    "\nTotal Rental Amount:",
                    total_amount
                )

                print(
                    "Already Paid:",
                    previous_payment
                )

                remaining_amount = (
                    total_amount - previous_payment
                )

                print(
                    "Remaining Amount:",
                    remaining_amount
                )

                if remaining_amount <= 0:

                    print("\nPayment is already completed.")

                else:

                    paid_amount = float(
                        input("Enter payment amount: ")
                    )

                    if paid_amount <= 0:

                        print(
                            "\nPayment amount must be greater than 0."
                        )

                    elif paid_amount > remaining_amount:

                        print(
                            "\nPayment cannot be greater than remaining amount."
                        )

                    else:

                        payment_method = input(
                            "Enter payment method (Cash/UPI/Card): "
                        )

                        new_total_paid = (
                            previous_payment +
                            paid_amount
                        )

                        if new_total_paid >= total_amount:

                            payment_status = "Paid"

                        else:

                            payment_status = "Partial"

                        query = """
                        INSERT INTO payments
                        (
                            rental_id,
                            payment_date,
                            amount,
                            payment_method,
                            payment_status
                        )
                        VALUES
                        (
                            %s,
                            CURDATE(),
                            %s,
                            %s,
                            %s
                        )
                        """

                        values = (
                            rental_id,
                            paid_amount,
                            payment_method,
                            payment_status
                        )

                        cursor.execute(query, values)

                        connection.commit()

                        print(
                            "\n========== PAYMENT DETAILS =========="
                        )

                        print(
                            "Rental ID       :",
                            rental_id
                        )

                        print(
                            "Rental Amount   :",
                            total_amount
                        )

                        print(
                            "Previous Paid   :",
                            previous_payment
                        )

                        print(
                            "Current Payment :",
                            paid_amount
                        )

                        print(
                            "Total Paid      :",
                            new_total_paid
                        )

                        print(
                            "Remaining       :",
                            total_amount - new_total_paid
                        )

                        print(
                            "Payment Method  :",
                            payment_method
                        )

                        print(
                            "Payment Status  :",
                            payment_status
                        )

                        print(
                            "===================================="
                        )

        except Exception as e:

            connection.rollback()
            print("\nError:", e)

        finally:

            cursor.close()
            connection.close()


    # =====================================================
    # 6. MAINTENANCE MANAGEMENT
    # =====================================================

    elif choice == "6":

        print("\n========== MAINTENANCE MANAGEMENT ==========")
        print("1. Add Maintenance")
        print("2. View Maintenance")
        print("3. Complete Maintenance")

        maintenance_choice = input(
            "\nEnter your choice: "
        )


        # -------------------------------------------------
        # ADD MAINTENANCE
        # -------------------------------------------------

        if maintenance_choice == "1":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                vehicle_id = input(
                    "Enter vehicle ID: "
                )

                service_date = input(
                    "Enter service date (YYYY-MM-DD): "
                )

                description = input(
                    "Enter maintenance description: "
                )

                cost = float(
                    input("Enter maintenance cost: ")
                )

                query = """
                INSERT INTO maintenance
                (
                    vehicle_id,
                    service_date,
                    description,
                    cost,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    'Pending'
                )
                """

                values = (
                    vehicle_id,
                    service_date,
                    description,
                    cost
                )

                cursor.execute(query, values)

                # Vehicle goes into maintenance
                cursor.execute(
                    """
                    UPDATE vehicles
                    SET status = 'Maintenance'
                    WHERE vehicle_id = %s
                    """,
                    (vehicle_id,)
                )

                connection.commit()

                print(
                    "\nMaintenance record added successfully!"
                )

                print(
                    "Vehicle Status: Maintenance"
                )

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # VIEW MAINTENANCE
        # -------------------------------------------------

        elif maintenance_choice == "2":

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT
                    m.maintenance_id,
                    v.vehicle_number,
                    v.brand,
                    v.model,
                    m.service_date,
                    m.description,
                    m.cost,
                    m.status
                FROM maintenance m
                JOIN vehicles v
                    ON m.vehicle_id = v.vehicle_id
                ORDER BY m.service_date DESC
                """

                cursor.execute(query)

                records = cursor.fetchall()

                print(
                    "\n========== MAINTENANCE RECORDS =========="
                )

                if not records:

                    print("No maintenance records found.")

                else:

                    for record in records:

                        print("----------------------------------------")
                        print(
                            "Maintenance ID :",
                            record[0]
                        )
                        print(
                            "Vehicle        :",
                            record[1]
                        )
                        print(
                            "Brand/Model    :",
                            record[2],
                            record[3]
                        )
                        print(
                            "Service Date   :",
                            record[4]
                        )
                        print(
                            "Description    :",
                            record[5]
                        )
                        print(
                            "Cost           :",
                            record[6]
                        )
                        print(
                            "Status         :",
                            record[7]
                        )

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # COMPLETE MAINTENANCE
        # -------------------------------------------------

        elif maintenance_choice == "3":

            maintenance_id = input(
                "Enter maintenance ID: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                cursor.execute(
                    """
                    SELECT vehicle_id
                    FROM maintenance
                    WHERE maintenance_id = %s
                    """,
                    (maintenance_id,)
                )

                maintenance = cursor.fetchone()

                if not maintenance:

                    print(
                        "\nMaintenance record not found."
                    )

                else:

                    vehicle_id = maintenance[0]

                    cursor.execute(
                        """
                        UPDATE maintenance
                        SET status = 'Completed'
                        WHERE maintenance_id = %s
                        """,
                        (maintenance_id,)
                    )

                    cursor.execute(
                        """
                        UPDATE vehicles
                        SET status = 'Available'
                        WHERE vehicle_id = %s
                        """,
                        (vehicle_id,)
                    )

                    connection.commit()

                    print(
                        "\nMaintenance completed successfully!"
                    )

                    print(
                        "Vehicle Status: Available"
                    )

            except Exception as e:

                connection.rollback()
                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        else:

            print("\nInvalid choice!")


    # =====================================================
    # 7. SEARCH
    # =====================================================

    elif choice == "7":

        print("\n========== SEARCH ==========")
        print("1. Search Customer")
        print("2. Search Vehicle")
        print("3. Search Rental")

        search_choice = input(
            "\nEnter your choice: "
        )


        # -------------------------------------------------
        # SEARCH CUSTOMER
        # -------------------------------------------------

        if search_choice == "1":

            search = input(
                "Enter customer name, phone or license: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                value = "%" + search + "%"

                query = """
                SELECT *
                FROM customers
                WHERE full_name LIKE %s
                   OR phone LIKE %s
                   OR license_number LIKE %s
                """

                cursor.execute(
                    query,
                    (value, value, value)
                )

                customers = cursor.fetchall()

                if not customers:

                    print("\nCustomer not found.")

                else:

                    for customer in customers:

                        print("----------------------------------------")
                        print(
                            "Customer ID :",
                            customer[0]
                        )
                        print(
                            "Name        :",
                            customer[1]
                        )
                        print(
                            "Phone       :",
                            customer[2]
                        )
                        print(
                            "Email       :",
                            customer[3]
                        )
                        print(
                            "Address     :",
                            customer[4]
                        )
                        print(
                            "License No. :",
                            customer[5]
                        )

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # SEARCH VEHICLE
        # -------------------------------------------------

        elif search_choice == "2":

            search = input(
                "Enter vehicle number, brand or model: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                value = "%" + search + "%"

                query = """
                SELECT *
                FROM vehicles
                WHERE vehicle_number LIKE %s
                   OR brand LIKE %s
                   OR model LIKE %s
                   OR vehicle_type LIKE %s
                """

                cursor.execute(
                    query,
                    (value, value, value, value)
                )

                vehicles = cursor.fetchall()

                if not vehicles:

                    print("\nVehicle not found.")

                else:

                    for vehicle in vehicles:

                        print("----------------------------------------")
                        print(
                            "Vehicle ID     :",
                            vehicle[0]
                        )
                        print(
                            "Vehicle Number :",
                            vehicle[1]
                        )
                        print(
                            "Type           :",
                            vehicle[2]
                        )
                        print(
                            "Brand          :",
                            vehicle[3]
                        )
                        print(
                            "Model          :",
                            vehicle[4]
                        )
                        print(
                            "Year           :",
                            vehicle[5]
                        )
                        print(
                            "Rent Per Day   :",
                            vehicle[6]
                        )
                        print(
                            "Status         :",
                            vehicle[7]
                        )

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        # -------------------------------------------------
        # SEARCH RENTAL
        # -------------------------------------------------

        elif search_choice == "3":

            rental_id = input(
                "Enter rental ID: "
            )

            connection = create_connection()
            cursor = connection.cursor()

            try:

                query = """
                SELECT
                    r.rental_id,
                    c.full_name,
                    v.vehicle_number,
                    v.brand,
                    v.model,
                    r.pickup_date,
                    r.return_date,
                    r.actual_return_date,
                    r.total_days,
                    r.rent_amount,
                    r.late_fee,
                    r.total_amount,
                    r.rental_status
                FROM rentals r
                JOIN customers c
                    ON r.customer_id = c.customer_id
                JOIN vehicles v
                    ON r.vehicle_id = v.vehicle_id
                WHERE r.rental_id = %s
                """

                cursor.execute(
                    query,
                    (rental_id,)
                )

                rental = cursor.fetchone()

                if not rental:

                    print("\nRental not found.")

                else:

                    print(
                        "\n========== RENTAL DETAILS =========="
                    )

                    print(
                        "Rental ID       :",
                        rental[0]
                    )
                    print(
                        "Customer        :",
                        rental[1]
                    )
                    print(
                        "Vehicle         :",
                        rental[2]
                    )
                    print(
                        "Brand/Model     :",
                        rental[3],
                        rental[4]
                    )
                    print(
                        "Pickup Date     :",
                        rental[5]
                    )
                    print(
                        "Return Date     :",
                        rental[6]
                    )
                    print(
                        "Actual Return   :",
                        rental[7]
                    )
                    print(
                        "Total Days      :",
                        rental[8]
                    )
                    print(
                        "Rent Amount     :",
                        rental[9]
                    )
                    print(
                        "Late Fee        :",
                        rental[10]
                    )
                    print(
                        "Total Amount    :",
                        rental[11]
                    )
                    print(
                        "Rental Status   :",
                        rental[12]
                    )

            except Exception as e:

                print("\nError:", e)

            finally:

                cursor.close()
                connection.close()


        else:

            print("\nInvalid choice!")


    # =====================================================
    # 8. REPORTS & ANALYTICS
    # =====================================================

    elif choice == "8":

        print("\n========== REPORTS & ANALYTICS ==========")
        print("1. Total Revenue")
        print("2. Most Rented Vehicles")
        print("3. Top Customers")
        print("4. Available Vehicles")
        print("5. Rental History")
        print("6. Maintenance Cost")
        print("7. Monthly Revenue")

        report_choice = input(
            "\nEnter your choice: "
        )

        connection = create_connection()
        cursor = connection.cursor()


        try:

            # -------------------------------------------------
            # TOTAL REVENUE
            # -------------------------------------------------

            if report_choice == "1":

                query = """
                SELECT COALESCE(SUM(total_amount), 0)
                FROM rentals
                WHERE rental_status = 'Completed'
                """

                cursor.execute(query)

                revenue = cursor.fetchone()[0]

                print(
                    "\n========== TOTAL REVENUE =========="
                )

                print(
                    "Total Revenue:",
                    revenue
                )


            # -------------------------------------------------
            # MOST RENTED VEHICLES
            # -------------------------------------------------

            elif report_choice == "2":

                query = """
                SELECT
                    v.vehicle_number,
                    v.brand,
                    v.model,
                    COUNT(r.rental_id) AS total_rentals
                FROM rentals r
                JOIN vehicles v
                    ON r.vehicle_id = v.vehicle_id
                GROUP BY
                    v.vehicle_id,
                    v.vehicle_number,
                    v.brand,
                    v.model
                ORDER BY total_rentals DESC
                """

                cursor.execute(query)

                records = cursor.fetchall()

                print(
                    "\n========== MOST RENTED VEHICLES =========="
                )

                if not records:

                    print("No rental data available.")

                else:

                    for record in records:

                        print("----------------------------------------")
                        print(
                            "Vehicle:",
                            record[0]
                        )
                        print(
                            "Brand/Model:",
                            record[1],
                            record[2]
                        )
                        print(
                            "Total Rentals:",
                            record[3]
                        )


            # -------------------------------------------------
            # TOP CUSTOMERS
            # -------------------------------------------------

            elif report_choice == "3":

                query = """
                SELECT
                    c.customer_id,
                    c.full_name,
                    COUNT(r.rental_id) AS total_rentals
                FROM customers c
                JOIN rentals r
                    ON c.customer_id = r.customer_id
                GROUP BY
                    c.customer_id,
                    c.full_name
                ORDER BY total_rentals DESC
                """

                cursor.execute(query)

                records = cursor.fetchall()

                print(
                    "\n========== TOP CUSTOMERS =========="
                )

                if not records:

                    print("No rental data available.")

                else:

                    for record in records:

                        print("----------------------------------------")
                        print(
                            "Customer ID:",
                            record[0]
                        )
                        print(
                            "Customer:",
                            record[1]
                        )
                        print(
                            "Total Rentals:",
                            record[2]
                        )


            # -------------------------------------------------
            # AVAILABLE VEHICLES
            # -------------------------------------------------

            elif report_choice == "4":

                query = """
                SELECT
                    vehicle_number,
                    vehicle_type,
                    brand,
                    model,
                    rent_per_day
                FROM vehicles
                WHERE status = 'Available'
                """

                cursor.execute(query)

                vehicles = cursor.fetchall()

                print(
                    "\n========== AVAILABLE VEHICLES =========="
                )

                if not vehicles:

                    print("No available vehicles.")

                else:

                    for vehicle in vehicles:

                        print("----------------------------------------")
                        print(
                            "Vehicle Number:",
                            vehicle[0]
                        )
                        print(
                            "Type:",
                            vehicle[1]
                        )
                        print(
                            "Brand/Model:",
                            vehicle[2],
                            vehicle[3]
                        )
                        print(
                            "Rent Per Day:",
                            vehicle[4]
                        )


            # -------------------------------------------------
            # RENTAL HISTORY
            # -------------------------------------------------

            elif report_choice == "5":

                query = """
                SELECT
                    r.rental_id,
                    c.full_name,
                    v.vehicle_number,
                    r.pickup_date,
                    r.return_date,
                    r.total_amount,
                    r.rental_status
                FROM rentals r
                JOIN customers c
                    ON r.customer_id = c.customer_id
                JOIN vehicles v
                    ON r.vehicle_id = v.vehicle_id
                ORDER BY r.rental_id DESC
                """

                cursor.execute(query)

                records = cursor.fetchall()

                print(
                    "\n========== COMPLETE RENTAL HISTORY =========="
                )

                if not records:

                    print("No rental history found.")

                else:

                    for record in records:

                        print("----------------------------------------")
                        print(
                            "Rental ID:",
                            record[0]
                        )
                        print(
                            "Customer:",
                            record[1]
                        )
                        print(
                            "Vehicle:",
                            record[2]
                        )
                        print(
                            "Pickup:",
                            record[3]
                        )
                        print(
                            "Return:",
                            record[4]
                        )
                        print(
                            "Amount:",
                            record[5]
                        )
                        print(
                            "Status:",
                            record[6]
                        )


            # -------------------------------------------------
            # MAINTENANCE COST
            # -------------------------------------------------

            elif report_choice == "6":

                query = """
                SELECT
                    COALESCE(SUM(cost), 0)
                FROM maintenance
                """

                cursor.execute(query)

                total_cost = cursor.fetchone()[0]

                print(
                    "\n========== MAINTENANCE COST =========="
                )

                print(
                    "Total Maintenance Cost:",
                    total_cost
                )


            # -------------------------------------------------
            # MONTHLY REVENUE
            # -------------------------------------------------

            elif report_choice == "7":

                query = """
                SELECT
                    DATE_FORMAT(booking_date, '%Y-%m')
                    AS month,
                    SUM(total_amount) AS revenue
                FROM rentals
                GROUP BY
                    DATE_FORMAT(booking_date, '%Y-%m')
                ORDER BY month
                """

                cursor.execute(query)

                records = cursor.fetchall()

                print(
                    "\n========== MONTHLY REVENUE =========="
                )

                if not records:

                    print("No revenue data available.")

                else:

                    for record in records:

                        print("----------------------------------------")
                        print(
                            "Month:",
                            record[0]
                        )
                        print(
                            "Revenue:",
                            record[1]
                        )


            else:

                print("\nInvalid choice!")


        except Exception as e:

            print("\nError:", e)

        finally:

            cursor.close()
            connection.close()


    # =====================================================
    # 9. EXIT
    # =====================================================

    elif choice == "9":

        print(
            "\nThank you for using "
            "Vehicle Rental Management System!"
        )

        print("Goodbye!\n")

        break


    # =====================================================
    # INVALID MAIN MENU CHOICE
    # =====================================================

    else:

        print(
            "\nInvalid choice! Please try again.\n"
        )
