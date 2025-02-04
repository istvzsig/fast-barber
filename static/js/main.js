// static/script.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("booking-form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent page reload

        const username = document.getElementById("username").value;
        const barberId = document.getElementById("barber").value;
        const appointmentTime = document.getElementById("appointment-time").value;

        if (!username || !barberId || !appointmentTime) {
            alert("Please fill in all fields.");
            return;
        }

        const response = await fetch("/bookings/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                barber_id: parseInt(barberId),
                appointment_time: appointmentTime
            })
        });

        if (response.ok) {
            alert("Booking successful!");
            location.reload(); // Reload the page to show updated bookings
        } else {
            alert("Error booking appointment.");
        }
    });
});
