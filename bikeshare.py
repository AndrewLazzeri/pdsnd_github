import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'phoenix: phoenix.csv',
              'houston : houston.csv'}

MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all months': 7}

DAYOFWEEK_DATA = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7, 'all': 8}

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

    cityentry = input("Plese provide your desired city.  We have data for Washington, Chicago and New York City: ")
    while cityentry.lower() not in CITY_DATA:
        cityentry = input(cityentry + " doesn't have data. Please provide either Chicago, Washington or New York City:  ")
    print("Great, "+cityentry + " has tons of data.  Let me ask you a few more questions to target your inquiry. ")
    global cityentry1
    cityentry1 = cityentry

    # get user input for month (all, january, february, ... , june)
    monthentry = input("Specifically, please provide your month of interest.  Currently we have data for January to June inclusive or if you want all months, input all months:  ")
    while monthentry.lower() not in MONTH_DATA:
        monthentry = input(monthentry + " doesn't have data. Please provide a month between January and June inclusive or all months:  ")
    print(monthentry + " has lots of data.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    dayentry = input("Finally, the last question.  Please provide the day of the week you have interest in.  This should take the form of Monday, Tuesday, etc. or all for all days: ")
    while dayentry.lower() not in DAYOFWEEK_DATA:
        dayentry = input(dayentry + " doesn't have data. Please provide valid day of the week or all for     all days:  ")
    print("Great.  You selected "+dayentry +". Let me perform some calculations involving the city of "+cityentry +" isolating " + monthentry +" and "+dayentry)

    print('-'*40)
    return cityentry, monthentry, dayentry


def load_data(cityentry, monthentry, dayentry):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        This code will help filter the underlying data by city, month and day
    """
    CSVREF = {'washington':'washington.csv', 'chicago':'chicago.csv', 'new york city':'new_york_city.csv'}
    for city, csv in CSVREF.items():
        if city == cityentry.lower():
            df = pd.read_csv(str(csv))
            df['Start Time Mod'] = pd.to_datetime(df['Start Time'])
            df['Hour'] = df['Start Time Mod'].dt.hour
            df['Month'] = df['Start Time Mod'].dt.month
            df['Day'] = df['Start Time Mod'].dt.day
            df['Day_of_Week'] = df['Start Time Mod'].dt.dayofweek


            if monthentry.lower() != 'all months':
                for month, num in MONTH_DATA.items():
                    if month == monthentry.lower():
                        df = df[df['Month'] == num]
            elif monthentry.lower() == 'all months':
                df = df

            if dayentry.lower() != 'all':
                for day, num in DAYOFWEEK_DATA.items():
                    if day == dayentry.lower():
                        df = df[df['Day_of_Week'] == num]
            elif dayentry.lower() == 'all':
                df = df

    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    MONTHREF ={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    most_common_month = df['Month'].mode()[0]
    for num, month in MONTHREF.items():
        if num == most_common_month:
            print(month +" is the most common month for rides")

    # display the most common day of week
    DAYREF ={1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
    most_common_day = df['Day_of_Week'].mode()[0]
    for num, day in DAYREF.items():
        if num == most_common_month:
            print(day +" is the most common day for rides based on your filters")


    # display the most common start hour
    most_common_hour = df['Hour'].mode()[0]
    hour_convert = most_common_hour - 12
    if most_common_hour > 12:
        print(str(hour_convert) + " PM is the most common time for rides to start")
    elif most_common_hour <= 12:
        print(str(most_common_hour) + " AM is the most common time for rides to start")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    print("The most common start station based on your filters is "+mode_start_station)

    # display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    print("The most common end station based on your filters is "+mode_end_station)

    # display most frequent combination of start station and end station trip
    df['StartStop'] = df['Start Station'] + "." + df['End Station']
    mode_connected_trip = df['StartStop'].mode()[0]
    reformat_mode_connect = str(mode_connected_trip).split(".")
    print("The most common trip is from "+reformat_mode_connect[0]+" to "+reformat_mode_connect[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total amount of time travelled was "+str(df['Trip Duration'].sum()))


    # display mean travel time
    print("The average amount of time travelled was "+str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,cityentry1):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("There were a total of "+str(np.sum(df['User Type']=='Customer'))+" customers and "+str(np.sum(df['User Type']=='Subscriber'))+" subscribers during the filtered period")

    # Display counts of gender
    if cityentry1.lower() == 'washington':
        print("There is no gender information for Washington DC")
    if cityentry1.lower() == 'chicago' or cityentry1.lower() == 'new york city':
        print("There were a total of "+str(np.sum(df['Gender']=='Male'))+" men and "+str(np.sum(df['Gender']=='Female'))+" females using the service during the filtered period")

    # Display earliest, most recent, and most common year of birth
    if cityentry1.lower() == 'washington':
        print("There is no age information for Washington DC")
    if cityentry1.lower() == 'chicago' or cityentry1.lower() == 'new york city':
        print("/nThe youngest person to ride was born in "+str(np.max(df['Birth Year']))+", the oldest person to ride was born in "+str(np.min(df['Birth Year']))+" and the most common birth year was "+str(df['Birth Year'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Asks user to specify if they want to see raw data.

    Returns:
        A string of raw daw if requested.

    """
    print('\nCalculating Raw Data...\n')
    start_time = time.time()

    # get user input if they want to see raw data
    YES_NO = {'yes': 1, 'no': 2}
    raw_data_request = input("Would you like to see some raw data (Yes/No)?: ")
    while raw_data_request.lower() not in YES_NO:
        raw_data_request = input("Please specify either yes or no only please: ")
    if raw_data_request.lower() == 'yes':
            print(df.iloc[1],[1])
            print("\n")
            print(df.iloc[1],[2])
            print("\n")
            print(df.iloc[1],[3])
            print("\n")
            print(df.iloc[1],[4])
            print("\n")
            print(df.iloc[1],[5])
    if raw_data_request == "no":
        print("Raw data is available for future requests")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,cityentry1)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
