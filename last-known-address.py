# File was originally a Jupyter notebook, but there were isues in transferring it from my work laptop so it is provided as a script here instead
# relevant libraries for working with csv/ Excel files 
import pandas as pd
import numpy as np

   

#testing string checks

#using levenshtein distance

# Z:\Group Annuity Pricing\Quote Tools\Van\Unlocated Member Search\Recipient History Files\2021\9 - SEP2021.csv

import numpy as np


def levenshteinDistanceDP(token1, token2):

    distances = np.zeros((len(token1) + 1, len(token2) + 1))


    for t1 in range(len(token1) + 1):

        distances[t1][0] = t1


    for t2 in range(len(token2) + 1):

        distances[0][t2] = t2

       

    a = 0

    b = 0

    c = 0

   

    for t1 in range(1, len(token1) + 1):

        for t2 in range(1, len(token2) + 1):

            if (token1[t1-1] == token2[t2-1]):

                distances[t1][t2] = distances[t1 - 1][t2 - 1]

            else:

                a = distances[t1][t2 - 1]

                b = distances[t1 - 1][t2]

                c = distances[t1 - 1][t2 - 1]

               

                if (a <= b and a <= c):

                    distances[t1][t2] = a + 1

                elif (b <= a and b <= c):

                    distances[t1][t2] = b + 1

                else:

                    distances[t1][t2] = c + 1


    #printDistances(distances, len(token1), len(token2))

    return distances[len(token1)][len(token2)]


def printDistances(distances, token1Length, token2Length):

    for t1 in range(token1Length + 1):

        for t2 in range(token2Length + 1):

            print(int(distances[t1][t2]), end=" ")

        print()

# formatting and filtering original csv file


def format_file(path):

    # indexing starts at 0 - minus 1 from column number 

    

    col_names = ['EMPLOYEE NUMBER', 'SIN', 'LAST NAME', 'FIRST NAME', 'MIDDLE NAME', 'CURRENT EMPLOYER', 'CURRENT PLAN',

             'CURRENT STATUS', 'CONTRACT NUMBER', 'BUY IN OR BUY OUT', 'EFFECTIVE DATE', 'TRANSACTION ID', 'PLAN CODE',

             'PLAN NAME', 'RECIPIENT EENO', 'RECIPIENT TYPE CODE', 'TYPE DESCRIPTION', 'RECIPIENT SIN',

             'RECIPIENT UNTRACEABLE FLAG', 'RECIPIENT LAST NAME', 'RECIPIENT FIRST NAME', 'RECIPIENT MIDDLE NAME',

             'RECIPIENT PREFIX', 'RECIPIENT DATE OF BIRTH', 'RECIPIENT DATE OF DEATH', 'RECIPIENT DATE OF DEATH NOTIFIED',

             'RECIPIENT DATE OF DEATH CONFIRMED', 'RECIPIENT GENDER', 'RECIPIENT LANGUAGE', 'RECIPIENT MARITAL STATUS',

             'RECIPIENT HOME ADDRESS LINE1', 'RECIPIENT HOME ADDRESS LINE2', 'RECIPIENT HOME ADDRESS LINE3',

             'RECIPIENT CITY', 'RECIPIENT PROVINCE', 'RECIPIENT COUNTRY', 'RECIPIENT POSTAL CODE',

             'RECIPIENT HOME PHONE NUMBER', 'RECIPIENT WORK PHONE NUMBER', 'RECIPIENT FAX NUMBER',

             'RECIPIENT EMAIL ADDRESS', 'RECIPIENT BANK NUMBER', 'RECIPIENT BANK ACCOUNT', 'RECIPIENT BANK TRANSIT',

             'RECIPIENT BANK PAY METHOD', 'RECIPIENT PAYMENT ADDRESS LINE1', 'RECIPIENT PAYMENT ADDRESS LINE2',

             'RECIPIENT PAYMENT ADDRESS LINE3', 'RECIPIENT PAYMENT CITY', 'RECIPIENT PAYMENT PROVINCE',

             'RECIPIENT PAYMENT COUNTRY', 'RECIPIENT PAYMENT POSTAL CODE', 'RECIPIENT CURRENTLY RESIDING TEMP LOCATION',

             'RECIPIENT COMMENTS']



    df = pd.read_csv(path, header = None, names = col_names, encoding='latin-1', low_memory=False)

    # get rid of buy-ins

    df2 = df[df['BUY IN OR BUY OUT'].str.lower() == 'buy in'].index

    df.drop(df2, inplace=True)


    # get rid of statuses that don't need to be checked

    df3 = df[(df['CURRENT STATUS'].str.lower() == 'death of retiree, no further payments') |

             (df['CURRENT STATUS'].str.lower() == 'death of deferred, paid out') |

             (df['CURRENT STATUS'].str.lower() == 'vested termination, paid out')].index

    df.drop(df3, inplace=True)


    # get rid of rows which have a DOD

    df4 = df[(df['RECIPIENT DATE OF DEATH NOTIFIED'].str.lower() != '0/00/00')].index

    df.drop(df4, inplace=True)

   

    df5 = df[(df['RECIPIENT DATE OF DEATH'].str.lower() != '0/00/00')].index

    df.drop(df5, inplace=True)


    # reset the index - if drop=True, it will replace any index you had before to 0 to n-1 rows

    # it will also turn your old index into a column if you had one

    df.reset_index(drop=True, inplace=True)

   

    return df, col_names


def invalid_address_to_csv(df, invalid_EENO_list):

    new_df = df[df['RECIPIENT EENO']==invalid_EENO_list[0]]

   

    for i in range(1, len(invalid_EENO_list)):

        row = df[df['RECIPIENT EENO']==invalid_EENO_list[i]]

        new_df = new_df.append(row)

   

    path = "invalid_addresses.csv"

   

    new_df.to_csv(path, sep="|", index = False)

   

    return

In [5]:

 

def deferred_EENO_to_csv(df, deferred_EENO_list):

    new_df = df[df['RECIPIENT EENO']==deferred_EENO_list[0]]

   

    for i in range(1, len(deferred_EENO_list)):

        row = df[df['RECIPIENT EENO']==deferred_EENO_list[i]]

        new_df = new_df.append(row)

   

    path = "deferred_members.csv"

   

    new_df.to_csv(path, sep="|", index = False)

   

    return


def missing_members_to_csv(df, EENO_list):

    new_df = df[df['RECIPIENT EENO']==EENO_list[0]]

   

    for i in range(1, len(EENO_list)):

        row = df[df['RECIPIENT EENO']==EENO_list[i]]

        new_df = new_df.append(row)

   

    path = "unlocated_members.csv"

   

    new_df.to_csv(path, sep="|", index = False)

   

    return


def get_invalid_addresses():

        recipient_history = input(str("Please enter the file path for the most recent recipient history file: "))

       

        recipient_history_df, col_names = format_file(recipient_history)

       

        # list of employee numbers associated with invalid addresses, will be appended to in next loop

        EENO_list = []

        # deferred members with invalid addresses

        deferred_EENO_list = []

        # for members who are flagged as invalid/ meet the invalid address criteria

        invalid_EENO_list = []

       

        invalid_address_list = ["6680 financial drive","6880 financial drive", "6880 financial dr",

                                "6880 financial dr 8th f", "6880 financial dr 8th fl", "nan"]

       

        # allows for eveything to be itereated through faster

        payment_address_array = np.array(recipient_history_df["RECIPIENT PAYMENT ADDRESS LINE1"])

       

        # checks to see if payment addresses are invalid

        # if they are, checks to see if they differ from the home address line

        for i in range(len(payment_address_array)):

            row = str(payment_address_array[i]).lower()

           

            if str(row).lower() in invalid_address_list:

                new_row = str(recipient_history_df["RECIPIENT HOME ADDRESS LINE1"][i]).lower()

               

                if new_row != row:

                    # regular members with blank home addresses

                    if new_row == "nan" or new_row == ".":

                        EENO_list.append(recipient_history_df["RECIPIENT EENO"][i])

                    # deferred members have blank payment addresses

                   elif row == "nan":

                        deferred_EENO_list.append(recipient_history_df["RECIPIENT EENO"][i])

                    # invalid addresses have variations of 6880 financial drive

                    elif new_row not in invalid_address_list:

                        invalid_EENO_list.append(recipient_history_df["RECIPIENT EENO"][i])

                    # members who have differing versions of 6880 financial drive in their address lines

                    else:

                        EENO_list.append(recipient_history_df["RECIPIENT EENO"][i])

                else:

                    EENO_list.append(recipient_history_df["RECIPIENT EENO"][i])

       

        # generates csv files for deferred members and invalid addresses where the last known address is currently known

        invalid_address_to_csv(recipient_history_df, invalid_EENO_list)

        deferred_EENO_to_csv(recipient_history_df, deferred_EENO_list)

      

    

        # searches for addresses of missing members, putting them into different csv files depending on whether

        # their addresses are found or not

       

        found_address_list, found_address_EENO = search_csv_files(EENO_list, col_names)

         # located members

        located_addresses_to_csv(found_address_list, col_names)

   

        # unlocated members

        remaining_missing_members(EENO_list, found_address_EENO, recipient_history_df)

       

        

        

        

        

        return


def search_csv_files(EENO_list, col_names):

    # path for most recent recipient history file, will be altering this with loops as function goes along

    path_start = "xyz"

    

    # index numbers for employee number and various address information

    #col_nums = [0, 1, 2, 3, 7, 9, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 51, 52]


    # information for string concatenation

    year = 2021

    month_num = 8 # set for the previous month, ie August at the time of creation

    month_list = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",

                 "AUG", "SEP", "OCT", "NOV", "DEC"]

   

    invalid_address_list = ["6880 financial drive", "6880 financial dr", "6880 financial dr 8th f", "6880 financial dr 8th fl", "nan", ""]

   

    

    # to iterate through EENO_list

    counter = 0

    # allows array to be iterated through more efficiently   

    EENO_list = np.array(EENO_list)

    # sets the address to appropriate length for EENO searching later

    found_address_list = [["","","","","","","","","","","","","","","","","","","","",""]]

    # captures found EENOs for later reference

    found_address_EENO = []

   

    # loops through currently found recipient history files

    while year > 2016:

       

        while month_num > 0:

           

            # skips over non existent files in directory

            if year == 2018:

                if month_num == 7:

                    month_num -= 1

                elif month_num == 3:

                    month_num = 1

            elif year == 2017:

                month_num = 1

            # adds appropriate month/ data info to pathway

            path = path_start + str(year) + "\\" + str(month_num) + " - " + month_list[month_num - 1] + str(year) + ".csv"

           

            address_check_df = pd.read_csv(path, header = None, names = col_names, encoding='latin-1', low_memory=False)

           

            # makes section of data frame that we're using into a more usable array

            new_list = np.array(address_check_df["RECIPIENT EENO"])

            while counter < len(EENO_list):

                # finds row number of member in csv

                member_pos = search(new_list, EENO_list[counter])

                flag = False

               

                # creates a variable to contain the home address of members if they're in the list

                if member_pos >= 0:

                    cell = str(address_check_df["RECIPIENT PAYMENT ADDRESS LINE1"][member_pos]).lower()

                   

                    if cell not in invalid_address_list:

                        # appends appropriate address info to list for later csv creation

                        for i in range(len(found_address_list)):

                            # specifically checks for EENO repeats inside the list

                            if EENO_list[counter] == found_address_list[i][17]:

                                flag = True

                


                        if not flag:

                            # appends appropriate row information to list

                            # pandas doesn't have a nice way to work with rows unfortunately

                            found_address_EENO.append(EENO_list[counter])

                            found_address_list.append([month_num, year, member_pos,

                                                       address_check_df["EMPLOYEE NUMBER"][member_pos],

                                                       address_check_df["SIN"][member_pos],

                                                        address_check_df["LAST NAME"][member_pos],

                                                        address_check_df["FIRST NAME"][member_pos],

                                                       address_check_df["MIDDLE NAME"][member_pos],

                                                       address_check_df["CURRENT EMPLOYER"][member_pos],

                                                       address_check_df["CURRENT PLAN"][member_pos],

                                                        address_check_df["CURRENT STATUS"][member_pos],

                                                       address_check_df["CONTRACT NUMBER"][member_pos],

                                                        address_check_df["BUY IN OR BUY OUT"][member_pos],

                                                       address_check_df["EFFECTIVE DATE"][member_pos],

                                                       address_check_df["TRANSACTION ID"][member_pos],

                                                       address_check_df["PLAN CODE"][member_pos],

                                                       address_check_df["PLAN NAME"][member_pos],

                                                        address_check_df["RECIPIENT EENO"][member_pos],

                                                        address_check_df["RECIPIENT TYPE CODE"][member_pos],

                                                        address_check_df["TYPE DESCRIPTION"][member_pos],

                                                       address_check_df["RECIPIENT SIN"][member_pos],

                                                       address_check_df["RECIPIENT UNTRACEABLE FLAG"][member_pos],

                                                        address_check_df["RECIPIENT LAST NAME"][member_pos],

                                                        address_check_df["RECIPIENT FIRST NAME"][member_pos],

                                                       address_check_df["RECIPIENT MIDDLE NAME"][member_pos],

                                                       address_check_df["RECIPIENT PREFIX"][member_pos],

                                                        address_check_df["RECIPIENT DATE OF BIRTH"][member_pos],              

                                                        address_check_df["RECIPIENT DATE OF DEATH"][member_pos],

                                                        address_check_df["RECIPIENT DATE OF DEATH NOTIFIED"][member_pos],

                                                        address_check_df["RECIPIENT DATE OF DEATH CONFIRMED"][member_pos],

                                                        address_check_df["RECIPIENT GENDER"][member_pos],

                                                        address_check_df["RECIPIENT LANGUAGE"][member_pos],

                                                       address_check_df["RECIPIENT MARITAL STATUS"][member_pos],

                                                        address_check_df["RECIPIENT HOME ADDRESS LINE1"][member_pos],

                                                        address_check_df["RECIPIENT HOME ADDRESS LINE2"][member_pos],

                                                        address_check_df["RECIPIENT HOME ADDRESS LINE3"][member_pos],

                                                        address_check_df["RECIPIENT CITY"][member_pos],

                                                        address_check_df["RECIPIENT PROVINCE"][member_pos],

                                                        address_check_df["RECIPIENT COUNTRY"][member_pos],

                                                        address_check_df["RECIPIENT POSTAL CODE"][member_pos],

                                                       address_check_df["RECIPIENT HOME PHONE NUMBER"][member_pos],

                                                       address_check_df["RECIPIENT WORK PHONE NUMBER"][member_pos],

                                                       address_check_df["RECIPIENT FAX NUMBER"][member_pos],

                                                       address_check_df["RECIPIENT EMAIL ADDRESS"][member_pos],

                                                       address_check_df["RECIPIENT BANK NUMBER"][member_pos],

                                                       address_check_df["RECIPIENT BANK ACCOUNT"][member_pos],

                                                       address_check_df["RECIPIENT BANK TRANSIT"][member_pos],

                                                       address_check_df["RECIPIENT BANK PAY METHOD"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT ADDRESS LINE1"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT ADDRESS LINE2"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT ADDRESS LINE3"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT CITY"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT PROVINCE"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT COUNTRY"][member_pos],

                                                        address_check_df["RECIPIENT PAYMENT POSTAL CODE"][member_pos],

                                                        address_check_df["RECIPIENT CURRENTLY RESIDING TEMP LOCATION"][member_pos],

                                                      address_check_df["RECIPIENT COMMENTS"][member_pos]])

                      

                counter +=1

               

            print(path)

            print(len(found_address_list))

            counter = 0

            month_num -= 1

        month_num = 12

        year -= 1

   

    # gets rid of non essential first list, then makes list easier to traverse

    found_address_list.remove(found_address_list[0])

    found_address_list = np.array(found_address_list)

    found_address_EENO = np.array(found_address_EENO)

   

    

    return found_address_list, found_address_EENO


       


def located_addresses_to_csv(found_address_list, col_names):


    found_address_df = pd.DataFrame(found_address_list)

    

    path = "found_address.csv"

  

    col_names.insert(0, "ORIGINAL MONTH")

    col_names.insert(1, "ORIGINAL YEAR")

    col_names.insert(2, "ORIGINAL ROW INDEX")

   

    

    found_address_df.to_csv(path, sep="|", header = col_names, index = False)

    return


 

# searches through older csv files in order to find last known address of membera


def search(arr, x):

 

    for i in range(len(arr)):

 

        if arr[i] == x:

            return i

 

    return -1

 

def remaining_missing_members(EENO_list, found_address_EENO, df):

   

    counter = 0

    counter2 = 0

   

    while counter < len(EENO_list):

        while counter2 < (len(found_address_EENO)):

            if EENO_list[counter] == found_address_EENO[counter2]:

                EENO_list.pop(counter)

                counter2 = len(found_address_EENO)

                counter -= 1

            counter2 += 1

        counter += 1

        counter2 = 0


   

    missing_members_to_csv(df, EENO_list)
    return
