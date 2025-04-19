from datetime import timedelta

# Function to calculate total time required to watch all episodes
def calculate_watch_time(total_episodes, episode_length_minutes=20):
    total_time_minutes = total_episodes * episode_length_minutes
    return total_time_minutes

# Function to convert time from minutes to days, months, and years
def convert_time(minutes):
    days = minutes // (24 * 60)
    remaining_minutes = minutes % (24 * 60)
    hours = remaining_minutes // 60
    minutes_left = remaining_minutes % 60
    
    # For simplicity, assume 30 days per month and 365 days per year
    months = days // 30
    years = days // 365
    days_left = days % 30
    
    return years, months, days_left, hours, minutes_left

# Function to calculate how many episodes to watch per day
def episodes_per_day(total_episodes, daily_watch_hours, episode_length_minutes=20):
    daily_watch_minutes = daily_watch_hours * 60
    episodes_per_day = daily_watch_minutes // episode_length_minutes
    return episodes_per_day

# Main function to get user inputs and display results
def main():
    # Get input from the user
    total_episodes = int(input("Enter the total number of episodes: "))
    daily_watch_hours = float(input("Enter how many hours you can watch per day: "))
    
    # Calculate total watch time
    total_minutes = calculate_watch_time(total_episodes)
    
    # Convert total watch time to days, months, and years
    years, months, days, hours, minutes = convert_time(total_minutes)
    
    # Calculate episodes per day based on daily available watch hours
    episodes_per_day_value = episodes_per_day(total_episodes, daily_watch_hours)
    
    # Display the results
    print(f"\nTotal watch time: {total_minutes} minutes")
    print(f"Equivalent to: {years} years, {months} months, {days} days, {hours} hours, and {minutes} minutes")
    
    print(f"To finish the series, you should watch approximately {episodes_per_day_value:.2f} episodes per day.")
    
# Run the program
if __name__ == "__main__":
    main()
