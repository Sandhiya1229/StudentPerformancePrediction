from flask import Blueprint, render_template, request, jsonify

from app.model import FEATURES, predict_performance

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "Student Performance API is running"
    })


@main.route("/api/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True) or {}

    try:
        values = []

        limits = {
            "attendance": (0, 100),
            "previous_marks": (0, 100),
            "assignment_marks": (0, 100),
            "study_hours": (0, 16),
            "internal_marks": (0, 100)
        }

        for feature in FEATURES:

            value = float(data[feature])
            minimum, maximum = limits[feature]

            if not minimum <= value <= maximum:
                return jsonify({
                    "error": f"Invalid value for {feature}"
                }), 400

            values.append(value)

        marks, category = predict_performance(values)

        suggestions = []

        if values[0] < 75:
            suggestions.append(
                "Improve attendance regularly."
            )

        if values[1] < 60:
            suggestions.append(
                "Practise previous exam questions."
            )

        if values[2] < 60:
            suggestions.append(
                "Complete assignments on time."
            )

        if values[3] < 2:
            suggestions.append(
                "Follow a regular daily study schedule."
            )

        if values[4] < 60:
            suggestions.append(
                "Focus on internal assessment preparation."
            )

        if not suggestions:
            suggestions.append(
                "Maintain your current learning habits."
            )

        return jsonify({
            "predicted_marks": marks,
            "category": category,
            "suggestions": suggestions
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please enter valid values in all fields."
        }), 400