from flask_wtf import Form
from wtforms.fields import IntegerField, RadioField, BooleanField, SelectField
from wtforms import widgets
from wtforms import validators


class CombatForm(Form):
    roll = IntegerField(
        "Roll",
        validators=[
            validators.input_required(),
            validators.number_range(min=1, max=100),
        ],
    )

    target = IntegerField(
        "Attribute (WS/BS)",
        validators=[
            validators.input_required(),
            validators.number_range(min=1, max=200),
        ],
    )

    misc = IntegerField(
        "Misc Modifier",
        validators=[
            validators.number_range(min=-100, max=100),
        ],
        default=0,
    )

    attack_type = RadioField(
        "Attack Type",
        choices=[
            ("standard", "Standard (+10)"),
            ("swift_semi", "Swift/Semi-Auto"),
            ("lighting_full", "Lightning/Full Auto (-10)"),
            ("supressing", "Suppressing Fire (-20)"),
            ("called", "Called Shot (-20)"),
        ],
        default="standard",
    )

    modifiers = RadioField(
        "Modifiers",
        choices=[
            ("none", "None"),
            ("guarded", "Guarded Action (-10)"),
            ("aim_half", "Aim, Half (+10)"),
            ("aim_full", "Aim, Full (+20)"),
        ],
        default="none",
    )

    # other conditional effects
    pinned = BooleanField("Pinned")
    target_stunned = BooleanField("Target Stunned")
    untrained = BooleanField("Untrained With Weapon")
    set_range = SelectField(
        "Range",
        choices=[
            ("normal", "Normal"),
            ("point_blank", "Point Blank (+30)"),
            ("short", "Short (+10)"),
            ("long", "Long (-10)"),
            ("extreme", "Extreme (-30)"),
        ],
    )
