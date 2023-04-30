from flask import Flask, request, render_template
from flask_wtf import CSRFProtect
from form import CombatForm
from utils import Utils

csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = "fortheemperor"
csrf.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    form = CombatForm(request.form)
    if request.method == "POST" and form.validate():
        roll = int(request.form["roll"])
        target = int(request.form["target"])

        attack_type = request.form["attack_type"]
        modifiers = request.form["modifiers"]
        extra_hits_divisor = 0

        if attack_type == "lighting_full":
            extra_hits_divisor = 2
        elif attack_type == "swift_semi":
            extra_hits_divisor = 1
            target -= 10
        elif attack_type == "suppressing" or attack_type == "called":
            target -= 20
        # Standard
        else:
            target += 10

        if modifiers == "aim_half":
            target += 10
        elif modifiers == "aim_full":
            target += 20

        results["Roll"] = roll
        results["Target"] = target

        degrees = Utils.get_degrees_of_failure_or_success(roll, target)
        results["Result"] = str(degrees)

        if degrees.is_success:
            hit_location, hit_location_number = Utils.get_hit_location(roll)
            results[
                "Hit Location"
            ] = f"{', '.join(hit_location.split('_'))} ({hit_location_number})"

            if extra_hits_divisor > 0:
                extra_hits = degrees.degrees // extra_hits_divisor
                results["Extra Hits"] = Utils.get_subsequent_hits(
                    hit_location.split("_")[0], extra_hits
                )

    return render_template("form.html", form=form, results=results)


if __name__ == "__main__":
    app.run(debug=True)
