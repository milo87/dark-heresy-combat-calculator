from math import floor


class DegreesResult:
    def __init__(self, is_success: bool, degrees: int) -> None:
        self.is_success = is_success
        self.degrees = degrees

    def __str__(self) -> str:
        return f"{'Success' if self.is_success else 'Failure'} ({self.degrees} Do{'S' if self.is_success else 'F'})"


class Utils:
    @staticmethod
    def get_subsequent_hits(location: str, additional_hits: int) -> str:
        location_table = {
            "head": ["head", "arm", "body", "arm", "body"],
            "arm": ["arm", "body", "head", "body", "arm"],
            "body": ["body", "arm", "head", "arm", "body"],
            "leg": ["leg", "body", "arm", "head", "body"],
        }

        if additional_hits < 5:
            locations = location_table[location][:additional_hits]
        else:
            locations = location_table[location] + [location_table[location][-1]] * (
                additional_hits - 5
            )

        return ", ".join(locations)

    @staticmethod
    def get_degrees_of_failure_or_success(roll: int, target: int) -> DegreesResult:
        if roll <= target:
            degrees = target // 10 - roll // 10
            return DegreesResult(True, degrees + 1)
        else:
            degrees = abs((roll // 10 - target // 10))
            return DegreesResult(False, degrees + 1)

    @staticmethod
    def get_hit_location(roll: int) -> str:
        location_roll = int(f"{roll:02}"[::-1])

        if location_roll <= 10:
            location_string = "head"
        elif location_roll <= 20:
            location_string = "arm_right"
        elif location_roll <= 30:
            location_string = "arm_left"
        elif location_roll <= 70:
            location_string = "body"
        elif location_roll <= 85:
            location_string = "leg_right"
        else:
            location_string = "leg_left"

        return (location_string, f"{location_roll:02}")
