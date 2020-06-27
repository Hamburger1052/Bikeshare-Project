import time
import pandas as pd


CITY_DATA = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}
CITIES = ['Chicago', 'New York', 'Washington']
MONTHS = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday']


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
        city=input("Which city's data would you like to see? (Chicago, New York, Washington)\n")
        city=city.title()
        if city in CITIES:
            break
        else:
            print("Please enter a valid input...")
    print("\n")
    # get user input for month (all, january, february, ... , june)
    while True:
        month=input("Would you like to filter your data by month?\nSpecify the month name\n(january, february, march, april, may, june, july, august, september, october, november, december)\nFor no filter type 'n'\n")
        if month.title() in MONTHS:
            month=month.title()
            break
        elif month=='n':
            break
        else:
            print("Please enter a valid input...")
    print("\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Would you like to filter your data according to day?\nSpecify the day\n(sunday, monday, tuesday, wednesday, thursday, friday, saturday)\nFor no filter type 'n'\n")
        if day.title() in DAYS:
            day=day.title()
            break
        elif day =='n':
            break
        else:
            print("Please enter a valid input...")
    print('-'*40)
    print("Please wait while data is being collected!")
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
    #import csv file
    df=pd.read_csv(CITY_DATA[city])
    #convert into datetime format
    df['Start Time']=pd.to_datetime(df["Start Time"])
    #make month column
    df['Month']=df['Start Time'].dt.month
    #make weekday column
    df['Day of week']=df['Start Time'].dt.day_name()
    #filter by month
    if month !='n':
        month=MONTHS.index(month) + 1
        df=df[df['Month']==month]
    #filter by day of week
    if day !='n':
        df=df[df['Day of week']==day]
    #make hour column
    df['Hour']=df['Start Time'].dt.hour

    return df

#to print filtered data without creating extra columns

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-'*45)
    print("-"*15+"Time Statistics"+"-"*15)
    print('-'*45)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['Month'].mode()[0]
    print("The most common month is",MONTHS[common_month-1],".\n")
    # display the most common day of week
    common_day=df['Day of week'].mode()[0]
    print("The most common day of the week is",common_day,".\n")
    # display the most common start hour
    common_hour=df['Hour'].mode()[0]
    if common_hour<=12:
        print("The most common hour for travel is",common_hour,"am.\n")
    else:
        common_hour-=12
        print("The most common hour for travel is",common_hour,"pm.\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('-'*44)
    print("-"*13+"Station Statistics"+"-"*13)
    print('-'*44)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations=df['Start Station'].value_counts()
    most_used_start_station=start_stations.idxmax()
    print("The most popular start station is "+most_used_start_station,".\n")
    # display most commonly used end station
    end_stations=df['End Station'].value_counts()
    most_used_end_station=end_stations.idxmax()
    print("The most popular end station is "+most_used_end_station,".\n")
    # display most frequent combination of start station and end station trip
    df['Combo Station']="\""+df['Start Station']+"\" & \""+df['End Station']+"\""
    combo_stations=df['Combo Station'].value_counts()
    most_used_combo_station=combo_stations.idxmax()
    print("The most frequent combination of start station and end station is "+most_used_combo_station+".\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*44)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('-'*44)
    print("-"*10+"Trip Duration Statistics"+"-"*10)
    print('-'*44)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is",df['Trip Duration'].sum(),".\n")

    # display mean travel time
    print("The mean travel time is",round(df['Trip Duration'].mean(),2),".\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*44)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('-'*45)
    print("-"*15+"User Statistics"+"-"*15)
    print('-'*45)
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print(df["User Type"].value_counts(),"\n")
    # Display counts of gender
    if city=="Washington":
        print("Sorry but Washington does not have the required user data for gender and birth year.\n")
    else:
        print(df['Gender'].value_counts(),"\n")

    # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is",int(df['Birth Year'].min()),".\n")
        print("The most recent birth year is",int(df['Birth Year'].max()),".\n")
        most_common_year=df['Birth Year'].value_counts()
        print("The most common year of birth is",int(most_common_year.idxmax()),".\n")
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #to check if dataframe is empty or not
        if df.empty:
            print("Sorry but there is no data for this filter...\n")

        else:
            while True:
                option=input("What would you like to see?\n\nTime Statistic(type 1)\nStation Statistics(type 2)\nTrip Duration Statistics(type 3)\nUser Statistics(type 4)\nTo exit type 'e'\n")
                if option=='1':
                    time_stats(df)
                elif option=='2':
                    station_stats(df)
                elif option=='3':
                    trip_duration_stats(df)
                elif option=='4':
                    user_stats(df,city)
                elif option=='e':
                    break
                else:
                    print("Please enter a valid option...")
            n=0
            #to show user data
            while True:
                rawdata = input("Would you like to see raw user data? Enter y or n\n")
                if rawdata=='y':
                    print(df1[n:n+5].to_string(index=False))
                    n+=5
                else:
                    break

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            if restart.lower()=='n':
                break
            else:
                print("Please enter valid input...")



if __name__ == "__main__":
	main()
