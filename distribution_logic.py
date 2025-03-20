def calculate_seat_distribution(
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
    final_attendance,
):

    base_distributions = {
        "T20": {
            1: [37, 26, 23, 14],
            2: [40, 27, 20, 13],
            3: [44, 26, 18, 12],
            4: [46, 27, 15, 12],
            5: [48, 27, 14, 11],
        },
        "OD": {
            1: [41, 24, 19, 16],
            2: [43, 25, 17, 15],
            3: [45, 27, 15, 13],
            4: [47, 28, 14, 11],
            5: [49, 28, 13, 10],
        },
    }

    weather_effects = {
        "Sunny": {
            "T20": [1, 2, 2, 1],
            "OD": [2, 2, 1, 1],
        },
        "Overcast": {
            "T20": [-2, 3, 2, 1],
            "OD": [-3, 2, 1, 0],
        },
        "Hot": {
            "T20": [-4, 4, 3, -1],
            "OD": [-5, 5, 4, -2],
        },
    }

    base_dist = base_distributions[match_format][home_div]

    adjustments = weather_effects[weather][match_format]

    if fan_base_home > fan_base_away:
        adjustments[2] += 1
        adjustments[1] += 1
    else:
        adjustments[0] += 1

    if morale_home > 70:
        adjustments[2] += 1
        adjustments[3] += 1

    if rating_home > rating_away:
        adjustments[2] += 2

    adjusted_dist = [base_dist[i] + adjustments[i] for i in range(4)]

    total_percent = sum(adjusted_dist)
    normalized_dist = [p / total_percent for p in adjusted_dist]

    seat_counts = [round(normalized_dist[i] * final_attendance) for i in range(4)]

    total_seats = sum(seat_counts)
    difference = final_attendance - total_seats
    if difference != 0:
        seat_counts[0] += difference

    return seat_counts
    # return [
    #     seat_counts[0],
    #     seat_counts[1],
    #     seat_counts[2],
    #     seat_counts[3],
    # ]
