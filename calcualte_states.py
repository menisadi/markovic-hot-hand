import pandas as pd

def states(quarter, make, value, previous_quarter, previous_make, previous_value):
    if pd.isna(previous_make) or previous_quarter < quarter:
        return "START_TO_" + make + "_" + str(int(value))
    return previous_make + "_" + str(int(previous_value)) + "_TO_" + make +  "_" + str(int(value))

def generate_states(df):
    previous = df[['QUARTER','MAKE_MISS', 'VALUE']].shift(1)
    previous.columns = ['PREVIOUS_QUARTER','PREVIOUS_MAKE_MISS', 'PREVIOUS_VALUE']
    df_with_previous = pd.concat([df, previous], axis=1)

    df_states = df_with_previous.apply(lambda x: states(x.QUARTER, x.MAKE_MISS, x.VALUE, x.PREVIOUS_QUARTER, x.PREVIOUS_MAKE_MISS, x.PREVIOUS_VALUE), axis=1)

    return df.assign(STATE=df_states)
    
    
