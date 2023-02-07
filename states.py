import pandas as pd
from scipy.stats import chi2_contingency


def states_builder(quarter, make, value, previous_quarter, previous_make, previous_value):
    """
    Helper function to generate a state based on current and previous quarter, make and value
    Given values for a single row of a dataframe, this function computes the previous state and the current state.

    Parameters:
    quarter (int): The current quarter.
    make (str): The current value of MAKE_MISS.
    value (int): The current value of VALUE.
    previous_quarter (int): The previous quarter.
    previous_make (str): The previous value of MAKE_MISS.
    previous_value (int): The previous value of VALUE.

    Returns:
    tuple: A tuple containing the previous state and the current state.
    """

    # if the previous make and quarter are not available (meaning it is the first shot in the game)
    # or the previous quarter is less than the current quarter (meaning it is the first shot in the quarter)
    if pd.isna(previous_make) or previous_quarter < quarter:
        # the previous state is set to "START"
        prev_state = "START"
        # the current state is set as make\miss + shot value
        state = make + "_" + str(int(value))
    else:
        # the previous state is set to previous make\miss + pervious shot value
        prev_state = previous_make +  "_" + str(int(previous_value))
        # the current state is set as make\miss + shot value
        state = make +  "_" +str(int(value))
    # return the previous state and the current state as a tuple
    return (prev_state, state)

def add_states(df):
    """
    Given a dataframe of shots data, this function adds two new columns to the dataframe: PREV_STATE and STATE.

    The PREV_STATE column contains the previous state for each row, computed using the `states_builder` function.
    The STATE column contains the current state, also computed using the `states_builder` function.

    Parameters:
    df (pandas.DataFrame): The input dataframe.

    Returns:
    None. The input dataframe is modified in place.
    """

    # Check if the states had not been added already
    if 'PREV_STATE' in df.columns:
        return

    # create a data frame with the shifted values of QUARTER, MAKE_MISS and VALUE
    previous = df[['QUARTER','MAKE_MISS', 'VALUE']].shift(1)
    # rename the columns of the shifted data frame
    previous.columns = ['PREVIOUS_QUARTER','PREVIOUS_MAKE_MISS', 'PREVIOUS_VALUE']
    # concatenate the original data frame and the shifted data frame
    df_with_previous = pd.concat([df, previous], axis=1)

    # create the states using the states_builder function
    df_with_states = df_with_previous.apply(lambda x: states_builder(x.QUARTER, x.MAKE_MISS, x.VALUE, x.PREVIOUS_QUARTER, x.PREVIOUS_MAKE_MISS, x.PREVIOUS_VALUE), axis=1)

    # split the previous and current states into two separate columns of the original data frame
    df[['PREV_STATE', 'STATE']] = pd.DataFrame(df_with_states.to_list())

def transitions(df):
    """
    Given a dataframe, this function creates a transition matrix for the underlying Markov model's states.

    If the PREV_STATE and STATE columns are not present in the input dataframe, they are added using the `add_states` function.

    Parameters:
    df (pandas.DataFrame): The input dataframe.

    Returns:
    pandas.DataFrame: A normalized transition matrix for the states.
    """    
    # if the PREV_STATE column is not present in the data frame, add it
    if 'PREV_STATE' not in df.columns:
        add_states(df)

    # normalization helper function to divide the count of each state transition by the sum of the state transitions
    # applied below to the pivot table in order to normalize it's values
    def normalization(x):
        return x / float(x.sum())

    # use the pivot_table function to generate a table with PREV_STATE as the index and STATE as the columns
    # the values of the table are the count of each state transition
    # apply the normalization function to the table to get the empirical probabilities of each state transition                            
    return df.pivot_table(index="PREV_STATE", columns="STATE", 
            aggfunc='count')['MAKE_MISS'].apply(normalization, axis=1)

def preform_test(df):
    """
    Performs a chi-square independence test on the counts of the previous state and the state in the given dataframe.
    
    Parameters:
    df (pandas.DataFrame): the dataframe to perform the test on
    
    Returns:
    cross (pandas.DataFrame): the contingency table (i.e. cross-tabulation) of the counts of the previous state and the state
    chi2_result (tuple): the result of the chi-square independence test, including the test statistic, degrees of freedom,
        p-value, and expected frequencies of each combination of previous state and state
    """    
    # If the PREV_STATE and STATE columns are not present in the dataframe, run the add_states function to create them
    if 'PREV_STATE' not in df.columns:
        add_states(df)

    # Create a cross-tabulation of the counts of the PREV_STATE and STATE columns
    cross = pd.crosstab(df.PREV_STATE, df.STATE)

     # Perform the chi-square independence test on the cross-tabulation
    return cross, chi2_contingency(cross)

################################################################## 
# Older version. I think it is a bit less clean 
################################################################## 
# def states(quarter, make, value, previous_quarter, previous_make, previous_value):
#     if pd.isna(previous_make) or previous_quarter < quarter:
#         return "START_TO_" + make + "_" + str(int(value))
#     return previous_make + "_" + str(int(previous_value)) + "_TO_" + make +  "_" + str(int(value))

# def generate_states(df):
#     previous = df[['QUARTER','MAKE_MISS', 'VALUE']].shift(1)
#     previous.columns = ['PREVIOUS_QUARTER','PREVIOUS_MAKE_MISS', 'PREVIOUS_VALUE']
#     df_with_previous = pd.concat([df, previous], axis=1)

#     df_states = df_with_previous.apply(lambda x: states(x.QUARTER, x.MAKE_MISS, x.VALUE, x.PREVIOUS_QUARTER, x.PREVIOUS_MAKE_MISS, x.PREVIOUS_VALUE), axis=1)

#     return df.assign(STATE=df_states)
    