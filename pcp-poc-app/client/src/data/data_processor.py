import pandas as pd 

# converts the body of a response into a dataframe
def convert_json_to_df(json_data) -> pd.DataFrame: 
    
    new_df = pd.DataFrame.from_records(json_data)
    return new_df

def load_hydraulic_systems() -> list: 
    # load the hydraulic systems data
    with open("./data/hydraulic_system_names.txt", 'r') as file: 
        hydraulic_systems_data = []
        for name in file: 
            clean_name = name.strip()
            hydraulic_systems_data.append(clean_name)
            
    # hydraulic_systems_data = pd.read_csv("./hydraulic_systems.txt", delimiter="\n")
    return hydraulic_systems_data
