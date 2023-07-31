import pandas as pd 

# converts the body of a response into a dataframe
def convert_json_to_df(json_data): 
    # print(f"Type of json_data: {type(json_data)}")
    # for entry in json_data: 
    #     print(entry)
    new_df = pd.DataFrame.from_records(json_data)
    return new_df
