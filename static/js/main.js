// static/script.js

const DUMMY_BARBER_IMG_URLS = [
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.eMjfMxVlYuzAcXkq7VoPcQAAAA%26pid%3DApi&f=1&ipt=b39635a9b774b53452266eef7c644b34f5e58f2aece28f1b6816f44f33fa961a&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.5xurOceVymIXcglDe5ZUvAAAAA%26pid%3DApi&f=1&ipt=3a161bab345bacaf3f5e4ce0f4503fd47d11a0ef8514e5ee1fd95c9da785ed42&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.7ZOVa68CWitlK-8RwCfd-wAAAA%26pid%3DApi&f=1&ipt=51e683838e8db57896289258e8f1e0157bc63a8f457b60f6d2cf6193e95818a7&ipo=images",
]

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("booking-form");
    let barberId = null;

    const barberOptions = document.querySelectorAll(".barber-option");
    barberOptions.forEach((option, i) => {
        option.style.backgroundImage = `url('${DUMMY_BARBER_IMG_URLS[i]}')`;
        option.addEventListener("click", function () {
            barberOptions.forEach(opt => {
                opt.classList.remove("selected");
                opt.classList.add("not-selected")
            });
            option.classList.add("selected");
            barberId = this.dataset.barberId;
        });
    });

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
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
            location.reload();
        } else {
            alert("Error booking appointment.");
        }

        document.querySelectorAll(".barber-option")
            .forEach(opt => opt.classList.remove("selected"));
    });
});
