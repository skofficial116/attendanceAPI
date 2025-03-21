import math
from distribution_logic import calculate_seat_distribution
from typing import List, Dict


def calculate_home_participation(home_division, away_division, weather, match_format):

    base_home_participation = 0.50

    division_factor = (6 - home_division) * 0.04
    away_division_factor = (6 - away_division) * -0.03

    if home_division == 1 and away_division == 5:
        return round(0.83, 2)

    weather_factors = {
        "Sunny": 0.05,
        "Overcast": +0.09,
        "Hot": +0.08,
    }
    weather_factor = weather_factors.get(weather, 0)

    format_factors = {
        "OD": 0.02,
        "T20": 0.04,
    }
    format_factor = format_factors.get(match_format, 0)

    home_participation = (
        base_home_participation
        + division_factor
        + away_division_factor
        + weather_factor
        + format_factor
    )

    if home_division == away_division:
        home_participation = max(0.58, min(0.66, home_participation))
    else:
        home_participation = max(0.45, min(0.70, home_participation))

    return round(home_participation, 2), round(1 - home_participation, 2)


BASE_DIV_ATTENDANCE_RANGE = {
    5: (800, 1200),
    4: (3000, 4000),
    3: (5000, 7000),
    2: (8500, 10500),
    1: (15000, 18000),
}

weather_effects = {
    "Sunny": {
        1: (1.2, 1.3),
        2: (1.15, 1.2),
        3: (1.1, 1.15),
        4: (1.02, 1.08),
        5: (0.95, 1.02),
    },
    "Overcast": {
        1: (1.0, 1.1),
        2: (0.95, 1.05),
        3: (0.85, 0.95),
        4: (0.8, 0.88),
        5: (0.7, 0.78),
    },
    "Hot": {
        1: (1.1, 1.2),
        2: (1.05, 1.1),
        3: (0.95, 1.05),
        4: (0.9, 0.96),
        5: (0.8, 0.88),
    },
}


format_effects = {
    "OD": {
        1: (1.15, 1.2),
        2: (1.1, 1.15),
        3: (1.05, 1.1),
        4: (0.92, 1.0),
        5: (1.02, 1.08),
    },
    "T20": {
        1: (1.2, 1.25),
        2: (1.1, 1.15),
        3: (1.05, 1.1),
        4: (1.02, 1.08),
        5: (1.08, 1.12),
    },
}

RATING_MIN = 800
RATING_MAX = 2400


def exponential_rating_impact(rating, scale_factor=0.05):
    """Exponential function to calculate rating impact on attendance."""
    normalized_rating = (rating - RATING_MIN) / (RATING_MAX - RATING_MIN)
    return math.exp(scale_factor * normalized_rating) - 1


def logistic_function(x, midpoint, steepness, max_value):
    """Logistic function to model morale impact on attendance."""
    return max_value / (1 + math.exp(-steepness * (x - midpoint)))


def calculate_base_attendance(div, rating):
    base_lower, base_upper = BASE_DIV_ATTENDANCE_RANGE[div]
    return base_lower + ((rating - RATING_MIN) / (RATING_MAX - RATING_MIN)) * (
        base_upper - base_lower
    )


def calculate_attendance(
    home_div: int,
    away_div: int,
    fan_base_home: int,
    fan_base_away: int,
    morale_home: int,
    morale_away: int,
    rating_home: int,
    rating_away: int,
    weather: str,
    match_format: str,
) -> List[Dict[str, int]]:
    base_home = calculate_base_attendance(home_div, rating_home)
    base_away = calculate_base_attendance(away_div, rating_away)

    weather_factor_home = sum(weather_effects[weather][home_div]) / 2
    weather_factor_away = sum(weather_effects[weather][away_div]) / 2
    casual_home = int(base_home * weather_factor_home)
    casual_away = int((base_away * weather_factor_away) * 0.6)

    rating_impact_home = exponential_rating_impact(rating_home)
    rating_impact_away = exponential_rating_impact(rating_away)

    morale_impact_home = logistic_function(morale_home, 50, 0.15, 0.1)
    morale_impact_away = logistic_function(morale_away, 50, 0.15, 0.1)

    loyal_home = int(fan_base_home * (1 + morale_impact_home + rating_impact_home))
    loyal_away = int(fan_base_away * (1 + morale_impact_away + rating_impact_away))

    format_factor_home = sum(format_effects[match_format][home_div]) / 2
    format_factor_away = sum(format_effects[match_format][away_div]) / 2
    adjusted_home = int((casual_home + loyal_home) * format_factor_home)
    adjusted_away = int((casual_away + loyal_away) * format_factor_away)
    home_part, away_part = calculate_home_participation(
        home_div, away_div, weather, match_format
    )

    total_attendance = int(adjusted_home * home_part) + int(adjusted_away * away_part)

    distribution = calculate_seat_distribution(
        home_div,
        away_div,
        fan_base_home,
        fan_base_away,
        morale_home,
        morale_away,
        rating_home,
        rating_away,
        weather,
        match_format,
        total_attendance,
    )

    return [
        {"category": "Total", "attendance": total_attendance},
        {"category": "Standard", "attendance": distribution[0]},
        {"category": "Deluxe", "attendance": distribution[1]},
        {"category": "Premium", "attendance": distribution[2]},
        {"category": "Members", "attendance": distribution[3]},
    ]
