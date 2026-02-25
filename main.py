from datetime import date

# Get quarter dates
quarters_2025 = {
    "Q1": [date(2025, 9, 20), date(2025, 12, 12)],
    "Q2": [date(2026, 1, 4), date(2026, 3, 20)],
    "Q3": [date(2026, 3, 30), date(2026, 6, 11)],
}

# Get point values
plan_points = {
    "blue": 1359,
    "gold": 1905,
    "banana": 2592,
    "5": 75,
    "7": 75
}

# Get costs of meals
meal_costs = {
    "breakfast": 12.60, 
    "lunch": 13.65, 
    "dinner": 14.70, 
    "late night": 13.65
}

# Define not a number function
def not_number(string):
    try:
        float(string)
        return False
    except ValueError:
        return True

def get_current_quarter(today):
    for quarter_names in quarters_2025:
        current_quarter = quarter_names
        start_date = quarters_2025[quarter_names][0]
        end_date = quarters_2025[quarter_names][1]
        
        if start_date <= today <= end_date:
            return start_date, end_date

def get_user_points():
    user_points = input("How many slug points do you currently have? ")
    while not_number(user_points):
        user_points = input("Please enter a number: ")
    user_points = round(float(user_points), 2)
    
    return user_points

def get_plan():
    while True:
        plan = input("What slug points plan do you have? (blue, gold, banana, unlimited) ")
        if "blue" in plan.lower():
            return "blue"
        elif "gold" in plan.lower():
            return "gold"
        elif "banana" in plan.lower():
            return "banana"
        elif "unlimited" in plan.lower():
            unlimited = input("Do you have the 5-day or 7-day unlimited plan? (5,7) ")
            if "5" in unlimited.lower():
                return "5"
            elif "7" in unlimited.lower():
                return "7"
        else:
            continue

def get_mean_cost():
    mean_cost = (
        meal_costs["breakfast"] + meal_costs["lunch"] + meal_costs["dinner"] + meal_costs["late night"]
        ) / len(meal_costs)

    return mean_cost

def get_meal_want():
    meals_want = input("How many meals do you want to be able to eat a day? ")
    while not_number(meals_want):
        meals_want = input("Please enter a number: ")
    
    return meals_want

def calc_meal_stats(user_points, plan, start, end, today, mean_cost, meals_want, ):
    user_spent = float(plan_points[plan]) - float(user_points) # Points user has spent
    days_left = (end - today).days # Days left in quarter
    days_past = (today - start).days # Days since quarter started
    if days_left == 0:
        days_left = 1
    if days_past == 0:
        days_past = 1

    meals_left = user_points / mean_cost # Amount of meals user can buy
    meals_bought = user_spent / mean_cost # Amount of meals user has bought

    meals_per_day = meals_left / days_left # Amount of meals can eat per day
    points_per_day = meals_per_day * mean_cost
    meals_bought_per_day = meals_bought / days_past # Amount of meals eaten per day
    meals_will_get = meals_bought_per_day * days_left # Meals predicted will get

    points_leftover = user_points - (meals_will_get * mean_cost) # Points user will have leftover

    meals_want = float(meals_want) * days_left # meals you want to buy
    points_want = meals_want * mean_cost # meals you want to buy in points
    points_buy = points_want - user_points # points you need to buy to have that rate

    return {
        "meals_bought_per_day": meals_bought_per_day,
        "points_leftover": points_leftover,
        "meals_left": meals_left,
        "meals_will_get": meals_will_get,
        "meals_per_day": meals_per_day,
        "points_buy": points_buy,
        "points_per_day": points_per_day
    }

def print_results(results, meal_want):
    print("\n")
    print(f"You have been eating about {results['meals_bought_per_day']:.1f} meals per day.")
    if results["points_leftover"] > 0:
        print(
            f"You will have {results['points_leftover']:.2f} points ({(results['meals_left'] - results['meals_will_get']):.1f} meals) leftover if you don't start eating {results['meals_per_day']:.1f} meals ({results['points_per_day']:.2f} points) per day."
        )
    else:
        print(
            f"You can start eating {results['meals_per_day']:.1f} meals per day to perfectly have 0 slug points.\nYou can buy {abs(results['points_leftover']):.2f} points to continue eating as you have been ({results['meals_bought_per_day']:.1f} meals per day)."
        )
    if results["points_buy"] > 0:
        print(
            f"You can buy {results['points_buy']:.2f} points to eat {float(meal_want):.1f} meals per day."
        )
    else:
        print(
            f"You will have {abs(results['points_buy']):.2f} points leftover eating {float(meal_want):.1f} meals per day. Go get something from a cafe."
        )

def main():
    today = date.today()
    start, end = get_current_quarter(today)
    user_points = get_user_points()
    plan = get_plan()
    mean_cost = get_mean_cost()
    meal_want = get_meal_want()
    results = calc_meal_stats(user_points, plan, start, end, today, mean_cost, meal_want)
    print_results(results, meal_want)

main()