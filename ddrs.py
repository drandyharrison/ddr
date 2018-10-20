import os
import sys
import random
from calendar import monthrange
import datetime
import csv

# check the working directory
wd = os.getcwd()
print("Working directory: ", wd)

# define the config data
# list of domicile groups
domiciles = ['1.ALL', '2.UK', '3.EU', '4.OV']
# list of fields/column headers
fields = ['Cycle', 'Date', 'Day_of_the_week', 'Day', 'Month', 'Year', 'Domicile_Group', 'New_apps', '7-Day Moving Ave', 'Days to Deadline', 'Working Days to Deadline', 'Days Since Cycle Opened', 'Bank Holiday']
# current cycle
cycle = 2018
# header rows
# TODO read in rather than hard code
header = ["\"---------------------------------------------------\"",
            "\"UCAS Analysis and Insights - Daily Domicile Report\"",
            "\"---------------------------------------------------\"",
            "\"This data file should be used in conjunction with ...\"",
            "\"File: filename\"",
            "\"Cycle: 2018\"",
            "\"Reporting coverage: 6 Sep 2017 - 18 Feb 18\"",
            "\"Applicant coverage: 18 year old applicants\"",
            "\"Analysis class: Domicile\"",
            "\"---------------------------------------------------\"",
            "The 'Days to Deadline' variable Lorem ipsum dolor sit amet, consectetur adipiscing elit,",
            "The ' 7-Day Moving Average' variable sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "Data lines are comma delimited.",
            "Data follows - 9999 lines in total",
            "---------------------------------------------------"]

# ================
# define functions
# ================

# -----------------------------------------------------------------------
# Read in an integer from the stdin
#   prompt      the prompt to use when requesting user input
#   reminder    message when input isn't a valid integer and asking again
# -----------------------------------------------------------------------
def read_int_stdin(prompt, reminder="Try again!"):
    # keep asking until correct
    is_input_valid = False
    while not is_input_valid:
        try:
            num_rows_str = input("{}".format(prompt))
        except:
            # I don't the exceptions this can throw, so list them if they occur
            print("Unexpected error:", sys.exc_info()[0])
            raise
        # convert string to integer
        # TODO make into a sub-function
        try:
            num_rows = int(num_rows_str)
        except ValueError:
            print("String is not a valid integer: {}".format(num_rows_str))
            print("{}".format(reminder))
        except:
            # I don't the exceptions this can throw, so list them if they occur
            print("Unexpected error (when converting string to integer):", sys.exc_info()[0])
            raise
        else:
            # no exceptions thrown, so ok to proceed
            is_input_valid = True
    return num_rows

# ---------------------------------------------------------------
# Generate some random DDR data
#   num_rows    number of rows of random data to generate
#   fname       the name of the file to write the random data to
# --------------------------------------------------------------
def gen_rand_ddr(num_rows, fname):
    # append .csv suffix to filename
    fname = fname + '.csv'
    print('Generate {}'.format(fname))

    # generate random data
    year = cycle - 1
    try:
        # write the data to the named file
        with open(fname, "w") as f:
            sys.stdout = f
            # write header rows
            for h in header:
                print("{}".format(h))

            # write column headers
            lim = len(fields) - 1
            for idx, val in enumerate(fields):
                print("{}".format(val), end='', flush=True)
                # add column after each field except the last one
                if idx < lim:
                    print(",", end='', flush=True)
            # new line
            print("")
            for lp1 in range(num_rows):
                # generate a value for each field
                month = random.randint(1, 12)
                day = random.randint(1, monthrange(year, month)[1])
                date = datetime.date(year, month, day)
                month_name = date.strftime('%b')        # Get the three letter name for the month
                dow = date.strftime("%A")               # Get day of week name
                for f in fields:
                    if f == 'Cycle':
                        print('2018,', end='', flush=True)
                    elif f == 'Date':
                        print('{:02d}{}{},'.format(day, month_name, year), end='', flush=True)
                    elif f == 'Day_of_the_week':
                        print('{},'.format(dow), end='', flush=True)
                    elif f == 'Day':
                        print('{},'.format(day), end='', flush=True)
                    elif f == 'Month':
                        print('{},'.format(month), end='', flush=True)
                    elif f == 'Year':
                        print('{},'.format(year), end='', flush=True)
                    elif f == 'Domicile_Group':
                        print('{},'.format(domiciles[random.randrange(len(domiciles))]), end='', flush=True)
                    elif f == 'New_apps':
                        val = random.randint(1, 10000)
                        print('{},'.format(val), end='', flush=True)
                    elif f == '7-Day Moving Ave':
                        val = random.randint(1, 10000)
                        print('{},'.format(val), end='', flush=True)
                    elif f == 'Days to Deadline':
                        val = random.randint(1, 10000)
                        print('{},'.format(val), end='', flush=True)
                    elif f == 'Working Days to Deadline':
                        val = random.randint(1, 10000)
                        print('{},'.format(val), end='', flush=True)
                    elif f == 'Days Since Cycle Opened':
                        val = random.randint(1, 10000)
                        print('{},'.format(val), end='', flush=True)
                    elif f == 'Bank Holiday':
                        print('{}'.format(random.randint(0,1)), end='', flush=True)
                print('')   # clear to next line
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: # handle other exceptions
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        # reset stdout
        sys.stdout = sys.__stdout__

# Read in a csv file
#   fname       name of the csv file to read
#   delim       delimiter
#   skip_rows   number of initial rows to skip until reach the column headers
#   hdr         boolean flag to indicate whether there are column headers of go straight to data
def read_csv(fname, delim=',', skip_rows=0, hdr=True):
    csv_data = []
    try:
        with open(fname) as f:
            # read csv
            csv_contents = csv.reader(f, delimiter=delim)
            for idx, row in enumerate(csv_contents):
                if hdr and idx == skip_rows:
                    print("Headers::{}".format(row))
                elif hdr and idx > skip_rows:
                    print("[{:03d}] {}".format(idx, row))
                    csv_data.append(row)
                elif (not hdr) and idx == skip_rows:
                    print("[{:03d}] {}".format(idx, row))
                    csv_data.append(row)
    except IOError as e:
        # check file exists (assumes it's in the working directory)
        print("Unable to open file: {}".format(fname))  # either doesn't exist or no read permissions
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        is_valid_file = False
    else:
        is_valid_file = True
    return is_valid_file, csv_data


# ---------------------------------
# Interface to generate random data
# ---------------------------------
def rand_data_ui():
    # Read the number of rows from stdin
    num_rows = read_int_stdin("How many rows to generate? ")

    # Read name of file to generate
    try:
        fname = input("Name of file to generate: ")
    except:
        # I don't the exceptions this can throw, so list them if they occur
        print("Unexpected error:", sys.exc_info()[0])
        raise

    gen_rand_ddr(num_rows, fname)

# ==================
# define main script
# ==================

#rand_data_ui()

is_valid_file = False
while not is_valid_file:
    fname = input("Name of the first file to read? ")
    is_valid_file, csv_data1 = read_csv(fname, skip_rows=18)

print("CSV data")
for idx, elt in enumerate(csv_data1):
    print("\t[{:03d}]{}".format(idx, elt))

print("\n---------\nFinished!\n---------")
