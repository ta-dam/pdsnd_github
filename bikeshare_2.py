import time
import pandas as pd
import numpy as np

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

    city = input('What city do you want to explore—Chicago, New York City or Washington? Enter your chosen city:').lower()

    while city != ('chicago' or 'new york city' or 'washington'):
        try:
            load_data(city)
        except:
            print('No data available for the city you entered.')
            city = input('Enter Chicago, New York City or Washington:').lower()
            break



    # get user input for month (all, january, february, ... , june)

    month = input('Do you want to filter by a specific month? Enter January - June. If you don\'t want to filter by month enter \'all\': ').lower()

    while month != ('january' or 'february' or 'march' or 'april' or 'may' or 'june' or 'all'):
        try:
            load_data(month)
        except:
            print('You\'ve entered an invalid month.')
            month = input('Enter a month from January-June or\'all\': ').lower()
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Do you want to filter by day of the week? Enter a day of the week. If you don\'t want to filter by day enter \'all\': ').lower()

    while day != ('monday' or 'tuesday' or 'wednesday' or 'thursday' or 'friday' or 'saturday' or 'sunday' or 'all'):
        try:
            load_data(day)
        except:
            print('You\'ve entered an invalid day.')
            day = input('Enter a day of the week or \'all\': ').lower()
            break


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.Series(df['Start Time']).dt.month
    df['day_of_week'] = pd.Series(df['Start Time']).dt.weekday_name

    #extract hour from Start Time to create new columns
    df['hour'] = pd.Series(df['Start Time']).dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # concat 'Start Station' column with 'End Station' column
    df['trip'] = pd.Series(df['Start Station']).str.cat([pd.Series(df['End Station'])], sep=' to ')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week:', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    print('Most Frequent Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total Travel Time:', round(total, 2))
    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('Mean Travel Time:', round(mean, 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Amount according to user types:\n', user_types)

    # Display counts of gender
    if city == 'washington':
        print('No data on gender available for the selected city.')
    else:
        gender = df['Gender'].value_counts()
        print('Amount according to gender:\n', gender)


    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('No data on the year of birth available for the selected city.')
    else:
        common_birth_year = df['Birth Year'].mode()[0]
        most_recent = df['Birth Year'].max()
        earliest = df['Birth Year'].min()
        print('Earliest year of birth: {}\nMost recent year of birth: {}\nMost common year of birth: {}'.format(int(earliest), int(most_recent), int(common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_input (df):
    pd.options.display.max_columns = None
    display = input('Would you like to display the csv input? Enter \'yes\' or \'no\':\n').lower()
    i = 0
    y = 5
    while display != 'no':
        print(df.iloc[x:y, :8])
        display = input('Do you want see the next 5 lines? Enter \'yes\' or \'no\':\n'.lower())
        x += 5
        y += 5
        if display != 'yes':
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_input(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
