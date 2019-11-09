import time
import pandas as pd
import numpy as np
#Make sure csv files are in same folder
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter a city where you want info from (Chicago, New York City, Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please try again.')
            continue

    # get user input for month (all, january, february, ... , june)
    month = input('Pick a specific month from January to June or pick all: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Pick a day or pick all: ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print('The most popular month is: {}'.format(most_common_month))

    # display the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print('Most popular day of the week: {}'.format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()
    print('Most popular hour: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print('Most popular start station is: {}'.format(most_start_station))


    # display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print('Most popular end station is: {}'.format(most_end_station))

    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station','End Station']].mode().iloc[0]
    print('Most popular beginning and end stations are:\nStart: {} End: {}'.format(start_end_station[0],start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total trip duration: {}'.format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Average trip duration: {}'.format(mean_time))

    #Longest trip duration with starting station
    max_trip_start = df.groupby('Start Station', as_index=False)['Trip Duration'].max().rename(columns={'Trip Duration': 'Longest Trip'}).loc[0]
    print('Station with longest trip:\n{}'.format(max_trip_start))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of users:\n{}'.format(user_types))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Gender count:\n{}'.format(is_gender(df)))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(is_birth(df))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def is_gender(df):
    gender_count = df['Gender'].value_counts()
    return gender_count

def is_birth(df):
    birth = df['Birth Year']
    return 'Earliest Birth: {}\nMost Recent: {}\nMost Common Year: {}'.format(birth.min(),birth.max(),birth.mode().iloc[0])


def raw_data(df):
    while True:
        n = input('Would you like to see raw data?(yes/no)')
        if n.lower() == 'yes':
            rows = int(input('How many rows?'))
            print(df.head(rows+1))
        elif n.lower() == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
