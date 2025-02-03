#!/bin/bash

# Path to the database file
DB_FILE="barbershop.db"

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

    # Add barber to the database
    add_barber "$BARBER_NAME"

    # Ask if the user wants to add another barber
    read -p "Do you want to add another barber? (y/n): " choice
    if [[ "$choice" != [Yy]* ]]; then
        echo "Exiting... No more barbers will be added."
        break
    fi
done

