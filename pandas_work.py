import pandas as pd
import os

# Get the absolute file path of 'kd_csv.csv'
csv_file = os.path.abspath('kd_csv.csv')

# Read in the CSV file
df = pd.read_csv(csv_file)

# Shift the values of the 'QUARTER' column by one row
df['prev_quarter'] = df['QUARTER'].shift(1)

# Add a new column named 'Current_State' to the dataframe
df = df.assign(Current_State=0)

# Set the value of the 'Current_State' column based on the value of the 'VALUE' and 'MAKE_MISS' columns
df.loc[(df['VALUE'] == 2) & (df['MAKE_MISS'] == 'MISS'), 'Current_State'] = 20
df.loc[(df['VALUE'] == 2) & (df['MAKE_MISS'] == 'MAKE'), 'Current_State'] = 21
df.loc[(df['VALUE'] == 3) & (df['MAKE_MISS'] == 'MISS'), 'Current_State'] = 30
df.loc[(df['VALUE'] == 3) & (df['MAKE_MISS'] == 'MAKE'), 'Current_State'] = 31

## Shift the values of the 'Current_State' column by one row and store the result in a new column named 'Previous_State'
df['Previous_State'] = df['Current_State'].shift(1)



# Set the value of 'Previous_State' to 0 if one of the following conditions is met:
# 1. It is the first row in the dataframe
# 2. The value of 'QUARTER' is less than the value of 'prev_quarter'
# 3. The value of 'QUARTER' is 3 and the value of 'prev_quarter' is 2
df.loc[df['QUARTER'].index == 0, 'Previous_State'] = 0
df.loc[df['QUARTER'] < df['prev_quarter'], 'Previous_State'] = 0
df.loc[(df['QUARTER'] == 3) & (df['prev_quarter'] == 2), 'Previous_State'] = 0

df = df.assign(Start_To_Make_2=0)
df.loc[(df['Previous_State'] == 0) & (df['Current_State'] == 21), 'Start_To_Make_2'] = 1
df = df.assign(Start_To_Miss_2=0)
df.loc[(df['Previous_State'] == 0) & (df['Current_State'] == 20), 'Start_To_Miss_2'] = 1
df = df.assign(Start_To_Make_3=0)
df.loc[(df['Previous_State'] == 0) & (df['Current_State'] == 31), 'Start_To_Make_3'] = 1
df = df.assign(Start_To_Miss_3=0)
df.loc[(df['Previous_State'] == 0) & (df['Current_State'] == 30), 'Start_To_Miss_3'] = 1

df = df.assign(Miss_2_To_Miss_2=0)
df.loc[(df['Previous_State'] == 20) & (df['Current_State'] == 20), 'Miss_2_To_Miss_2'] = 1
df = df.assign(Miss_2_To_Make_2=0)
df.loc[(df['Previous_State'] == 20) & (df['Current_State'] == 21), 'Miss_2_To_Make_2'] = 1
df = df.assign(Miss_2_To_Miss_3=0)
df.loc[(df['Previous_State'] == 20) & (df['Current_State'] == 30), 'Miss_2_To_Miss_3'] = 1
df = df.assign(Miss_2_To_Make_3=0)
df.loc[(df['Previous_State'] == 20) & (df['Current_State'] == 31), 'Miss_2_To_Make_3'] = 1

df = df.assign(Make_2_To_Miss_2=0)
df.loc[(df['Previous_State'] == 21) & (df['Current_State'] == 20), 'Make_2_To_Miss_2'] = 1
df = df.assign(Make_2_To_Make_2=0)
df.loc[(df['Previous_State'] == 21) & (df['Current_State'] == 21), 'Make_2_To_Make_2'] = 1
df = df.assign(Make_2_To_Miss_3=0)
df.loc[(df['Previous_State'] == 21) & (df['Current_State'] == 30), 'Make_2_To_Miss_3'] = 1
df = df.assign(Make_2_To_Make_3=0)
df.loc[(df['Previous_State'] == 21) & (df['Current_State'] == 31), 'Make_2_To_Make_3'] = 1

df = df.assign(Miss_3_To_Miss_2=0)
df.loc[(df['Previous_State'] == 30) & (df['Current_State'] == 20), 'Miss_3_To_Miss_2'] = 1
df = df.assign(Miss_3_To_Make_2=0)
df.loc[(df['Previous_State'] == 30) & (df['Current_State'] == 21), 'Miss_3_To_Make_2'] = 1
df = df.assign(Miss_3_To_Miss_3=0)
df.loc[(df['Previous_State'] == 30) & (df['Current_State'] == 30), 'Miss_3_To_Miss_3'] = 1
df = df.assign(Miss_3_To_Make_3=0)
df.loc[(df['Previous_State'] == 30) & (df['Current_State'] == 31), 'Miss_3_To_Make_3'] = 1

df = df.assign(Make_3_To_Miss_2=0)
df.loc[(df['Previous_State'] == 31) & (df['Current_State'] == 20), 'Make_3_To_Miss_2'] = 1
df = df.assign(Make_3_To_Make_2=0)
df.loc[(df['Previous_State'] == 31) & (df['Current_State'] == 21), 'Make_3_To_Make_2'] = 1
df = df.assign(Make_3_To_Miss_3=0)
df.loc[(df['Previous_State'] == 31) & (df['Current_State'] == 30), 'Make_3_To_Miss_3'] = 1
df = df.assign(Make_3_To_Make_3=0)
df.loc[(df['Previous_State'] == 31) & (df['Current_State'] == 31), 'Make_3_To_Make_3'] = 1



df.drop('prev_quarter', axis=1, inplace=True)
df.drop('team', axis=1, inplace=True)


data = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
index = ["Start","After Miss of 2 point shot", "After Make of 2 point shot","After Miss of 3 point shot", "After Make of 3 point shot"]
columns = ["2 Make %", "3 Make %"]
# Create an empty dataframe with the desired row and column labels
Shot_Making_Results = pd.DataFrame(data, index=index, columns=columns)

# Calculate the percentage of successful 2-point shots and 3-point shots after each event and assign the value to the appropriate cell in the dataframe
Shot_Making_Results.loc["Start", "2 Make %"] = df['Start_To_Make_2'].sum() / (df['Start_To_Make_2'].sum() + df['Start_To_Miss_2'].sum())
Shot_Making_Results.loc["Start", "3 Make %"] = df['Start_To_Make_3'].sum() / (df['Start_To_Make_3'].sum() + df['Start_To_Miss_3'].sum())

Shot_Making_Results.loc["After Miss of 2 point shot", "2 Make %"] = df['Miss_2_To_Make_2'].sum() / (df['Miss_2_To_Make_2'].sum() + df['Miss_2_To_Miss_2'].sum())
Shot_Making_Results.loc["After Miss of 2 point shot", "3 Make %"] = df['Miss_2_To_Make_3'].sum() / (df['Miss_2_To_Make_3'].sum() + df['Miss_2_To_Miss_3'].sum())
Shot_Making_Results.loc["After Make of 2 point shot", "2 Make %"] = df['Make_2_To_Make_2'].sum() / (df['Make_2_To_Make_2'].sum() + df['Make_2_To_Miss_2'].sum())
Shot_Making_Results.loc["After Make of 2 point shot", "3 Make %"] = df['Make_2_To_Make_3'].sum() / (df['Make_2_To_Make_3'].sum() + df['Make_2_To_Miss_3'].sum())

Shot_Making_Results.loc["After Miss of 3 point shot", "2 Make %"] = df['Miss_3_To_Make_2'].sum() / (df['Miss_3_To_Make_2'].sum() + df['Miss_3_To_Miss_2'].sum())
Shot_Making_Results.loc["After Miss of 3 point shot", "3 Make %"] = df['Miss_3_To_Make_3'].sum() / (df['Miss_3_To_Make_3'].sum() + df['Miss_3_To_Miss_3'].sum())
Shot_Making_Results.loc["After Make of 3 point shot", "2 Make %"] = df['Make_3_To_Make_2'].sum() / (df['Make_3_To_Make_2'].sum() + df['Make_3_To_Miss_2'].sum())
Shot_Making_Results.loc["After Make of 3 point shot", "3 Make %"] = df['Make_3_To_Make_3'].sum() / (df['Make_3_To_Make_3'].sum() + df['Make_3_To_Miss_3'].sum())

print(Shot_Making_Results)


Start_Total = df['Start_To_Make_2'].sum() + df['Start_To_Miss_2'].sum() + df['Start_To_Make_3'].sum() + df['Start_To_Miss_3'].sum()
Miss_2_Total = df['Miss_2_To_Make_2'].sum() + df['Miss_2_To_Miss_2'].sum() + df['Miss_2_To_Make_3'].sum() + df['Miss_2_To_Miss_3'].sum()
Make_2_Total = df['Make_2_To_Make_2'].sum() + df['Make_2_To_Miss_2'].sum() + df['Make_2_To_Make_3'].sum() + df['Make_2_To_Miss_3'].sum()
Miss_3_Total = df['Miss_3_To_Make_2'].sum() + df['Miss_3_To_Miss_2'].sum() + df['Miss_3_To_Make_3'].sum() + df['Miss_3_To_Miss_3'].sum()
Make_3_Total = df['Make_3_To_Make_2'].sum() + df['Make_3_To_Miss_2'].sum() + df['Make_3_To_Make_3'].sum() + df['Make_3_To_Miss_3'].sum()

data = [
    [0, df['Start_To_Miss_2'].sum()/Start_Total, df['Start_To_Make_2'].sum()/Start_Total, df['Start_To_Miss_3'].sum()/Start_Total, df['Start_To_Make_3'].sum()/Start_Total],
    [0, df['Miss_2_To_Miss_2'].sum()/Miss_2_Total, df['Miss_2_To_Make_2'].sum()/Miss_2_Total, df['Miss_2_To_Miss_3'].sum()/Miss_2_Total, df['Miss_2_To_Make_3'].sum()/Miss_2_Total],
    [0, df['Make_2_To_Miss_2'].sum()/Make_2_Total, df['Make_2_To_Make_2'].sum()/Make_2_Total, df['Make_2_To_Miss_3'].sum()/Make_2_Total, df['Make_2_To_Make_3'].sum()/Make_2_Total],
    [0, df['Miss_3_To_Miss_2'].sum()/Miss_3_Total, df['Miss_3_To_Make_2'].sum()/Miss_3_Total, df['Miss_3_To_Miss_3'].sum()/Miss_3_Total, df['Miss_3_To_Make_3'].sum()/Miss_3_Total],
    [0, df['Make_3_To_Miss_2'].sum()/Make_3_Total, df['Make_3_To_Make_2'].sum()/Make_3_Total, df['Make_3_To_Miss_3'].sum()/Make_3_Total, df['Make_3_To_Make_3'].sum()/Make_3_Total]
]
index = ["Start","Miss 2 pts", "Make 2 pts","Miss 3 pts", "Make 3 pts"]
columns = ["Start","Miss 2 pts", "Make 2 pts","Miss 3 pts", "Make 3 pts"]
# Create a dataframe with for the transition probabilities matrix
Transition_Probabilities_Matrix = pd.DataFrame(data, index=index, columns=columns)

print(Transition_Probabilities_Matrix)

"""
# Get the directory of the original file
dirname = os.path.dirname('C:\\Users\\Dvir\\Documents\\מחקר\\פוסט דוקטורט\\היד החמה\\kd_csv.csv')

# Write the modified dataframe back to a CSV file in the same directory as the original file
df.to_csv(os.path.join(dirname, 'modified_file.csv'), index=False)
"""


# Get the directory of the original file
dirname = os.path.dirname(csv_file)

# Create an ExcelWriter object
writer = pd.ExcelWriter(os.path.join(dirname, 'modified_file.xlsx'), engine='xlsxwriter')

# Write each dataframe to a separate sheet in the Excel file
df.to_excel(writer, sheet_name='Data')
Shot_Making_Results.to_excel(writer, sheet_name='Shot Making')
Transition_Probabilities_Matrix.to_excel(writer, sheet_name='Transition Probabilities Matrix')

# Save the Excel file
writer.save()