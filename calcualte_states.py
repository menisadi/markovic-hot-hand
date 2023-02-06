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
    
    
# Second and probably better version (including the transition calculation)
def create_states(quarter, make, value, previous_quarter, previous_make, previous_value):
    if pd.isna(previous_make) or previous_quarter < quarter:
        prev_state = "START"
        state = make + "_" + str(int(value))
    else:
        prev_state = previous_make +  "_" +str(int(previous_value))
        state = make +  "_" +str(int(value))
    return (prev_state, state)

def calculate_transitions(df):
    previous = df[['QUARTER','MAKE_MISS', 'VALUE']].shift(1)
    previous.columns = ['PREVIOUS_QUARTER','PREVIOUS_MAKE_MISS', 'PREVIOUS_VALUE']
    df_with_previous = pd.concat([df, previous], axis=1)

    df_with_states = df_with_previous.apply(lambda x: states(x.QUARTER, x.MAKE_MISS, x.VALUE, x.PREVIOUS_QUARTER, x.PREVIOUS_MAKE_MISS, x.PREVIOUS_VALUE), axis=1)

    df[['PREV_STATE', 'STATE']] = pd.DataFrame(df_with_states.to_list())
    df['BINARY_MAKE_MISS'] = df['MAKE_MISS'].apply(lambda m: m=='MAKE')

    # cross = pd.crosstab(df.PREV_STATE, df.STATE)

    def normalization(x):
        return x / float(x.sum())
                            
    return df.pivot_table(index="PREV_STATE", columns="STATE", 
            aggfunc='count')['MAKE_MISS'].apply(normalization, axis=1)