import pandas as pd # in case of error, install pnadas using: pip install pandas
# Read the CSV file into a DataFrame
df = pd.read_csv('data.csv')

i = 0
while i<100:
    
    new_data = {
        'Temp': -400 + i,
        'Humd': 901,
        'Label': 0
        }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    i = i + 1

# Step 3: Save the DataFrame to a new CSV file
df.to_csv("data_changed.csv", index=False)