#!/bin/bash

# Path to the database file
DB_FILE="/db/barbershop.db"

# Check if the database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "Error: $DB_FILE not found!"
    exit 1
fi

# Function to add a barber to the database
add_barber() {
    BARBER_NAME="$1"

    # Check if barber already exists
    BARBER_EXISTS=$(sqlite3 $DB_FILE "SELECT COUNT(*) FROM barbers WHERE name='$BARBER_NAME';")

    if [ "$BARBER_EXISTS" -gt 0 ]; then
        echo "Barber '$BARBER_NAME' already exists in the database."
    else
        # Add barber to the database
        sqlite3 $DB_FILE "INSERT INTO barbers (name) VALUES ('$BARBER_NAME');"
        echo "Barber '$BARBER_NAME' added successfully."
    fi

    # Get the barber's ID
    BARBER_ID=$(sqlite3 $DB_FILE "SELECT id FROM barbers WHERE name='$BARBER_NAME' LIMIT 1;")

    # Set available hours for the barber
    set_available_hours "$BARBER_ID"
}

# Function to set available hours for a barber
set_available_hours() {
    BARBER_ID="$1"

    while true; do
        read -p "Enter day of the week (e.g., Monday, Tuesday): " DAY_OF_WEEK
        read -p "Enter start time (HH:MM format, 24-hour): " START_TIME
        read -p "Enter end time (HH:MM format, 24-hour): " END_TIME

        # Validate input
        if [ -z "$DAY_OF_WEEK" ] || [ -z "$START_TIME" ] || [ -z "$END_TIME" ]; then
            echo "Error: All fields must be provided."
            continue
        fi

        # Insert into database
        sqlite3 $DB_FILE "INSERT INTO available_hours (barber_id, day_of_week, start_time, end_time) VALUES ($BARBER_ID, '$DAY_OF_WEEK', '$START_TIME', '$END_TIME');"
        echo "Available hours for $DAY_OF_WEEK ($START_TIME - $END_TIME) added successfully."

        # Ask if the user wants to add more available hours
        read -p "Do you want to add more available hours for this barber? (y/n): " more_hours
        if [[ "$more_hours" != [Yy]* ]]; then
            break
        fi
    done
}

# Loop to prompt the user for barber names
while true; do
    # Prompt user for barber name
    read -p "Enter the barber's name to add: " BARBER_NAME

    # Validate if input is empty
    if [ -z "$BARBER_NAME" ]; then
        echo "Error: Barber name cannot be empty."
        continue
    fi

    # Add barber and set available hours
    add_barber "$BARBER_NAME"

    # Ask if the user wants to add another barber
    read -p "Do you want to add another barber? (y/n): " choice
    if [[ "$choice" != [Yy]* ]]; then
        echo "Exiting... No more barbers will be added."
        break
    fi
done
