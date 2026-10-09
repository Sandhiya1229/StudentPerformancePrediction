const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button = document.getElementById("predictButton");
    const error = document.getElementById("errorMessage");

    button.disabled = true;
    button.textContent = "Predicting...";
    error.textContent = "";

    const formData = new FormData(form);

    const data = {
        attendance: Number(formData.get("attendance")),
        previous_marks: Number(formData.get("previous_marks")),
        assignment_marks: Number(formData.get("assignment_marks")),
        study_hours: Number(formData.get("study_hours")),
        internal_marks: Number(formData.get("internal_marks"))
    };

    try {

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed.");
        }

        document.getElementById("result").hidden = false;

        document.getElementById("marks").textContent =
            result.predicted_marks;

        document.getElementById("category").textContent =
            result.category;

        const list = document.getElementById("suggestions");

        list.replaceChildren();

        result.suggestions.forEach(function (suggestion) {
            const item = document.createElement("li");
            item.textContent = suggestion;
            list.appendChild(item);
        });

        document.getElementById("result").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (err) {

        error.textContent = err.message;

    } finally {

        button.disabled = false;
        button.textContent = "Predict Performance";

    }

});