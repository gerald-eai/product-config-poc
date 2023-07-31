import pandas as pd 

# converts the body of a response into a dataframe
def convert_json_to_df(json_data): 
    
    new_df = pd.DataFrame.from_records(json_data)
    print(f"Dataframe created!!")
    return new_df
