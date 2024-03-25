"""NFA to DFA"""

import pandas as pd
import numbers
#print('\nDO REMEMBER TO ADD ACCEPT REJECT STATE AND ARROW POINTER\n')

#INPUT VALUE FOR THE TABLE


index_count = [0,1,4,5,2,6,3] #this is the identifier column

data_set_pointer = 0 #this is the pointer of index_count row

data = {
    
0 : [1, 1, (4,5), (5,6), 5, 6, 6],
1 : [4, 4, (2,4), (3,5), 2, 6, 3],
2 : [4, 4, (4,5), (5,6), 5, 6, 6]


       }#Column name have to specifically follow 0,1,2,3,4
 
acceptance_set = [0,0,0,0,0,1,0]








##DONT MODIFY THINGS BELLOW##
def index_check_hasNone(new_df: pd.DataFrame,new_value):
    # Check if the index contains "None"
    has_none_index = "None" in new_df.index
    if has_none_index:
        # Get the maximum value in the index, excluding "None"
        max_value = new_df.index.drop("None").max()
        # Create a new value for replacing "None"
        if new_value == 0:
            new_value = max_value + 1
        # Replace cell values of "None" with the new value
        new_df = new_df.replace("None", new_value)
        # Replace index values of "None" with the new value
        new_df.index = new_df.index.where(new_df.index != "None", new_value)
    return new_df

def add_acceptanceState(new_df:pd.DataFrame,index_dict,if_complement:bool, manual_value):
    acceptance_set = []
    one_exist = False
    for index_value in new_df.index:
        if isinstance(index_value, int):
            acceptance_set.append(index_dict[index_value])
        elif index_value == "None":
            acceptance_set.append(0)
        else:
            one_exist = False
            
            for i in index_value:
                if i.isdigit() and index_dict[int(i)] == 1:
                    one_exist = True
                    break
            acceptance_set.append(int(one_exist))


    if if_complement is False:
        #just pure append new acceptance_set into new_df
        new_df['acceptance'] = acceptance_set
    else:
        inverted_list = [1 - x for x in acceptance_set]
        new_df = index_check_hasNone(new_df,manual_value)

        new_df['acceptance'] = inverted_list
        if one_exist != True:
            new_df.sort_index()
    
    return new_df

def add_non_duplicate(name_at_rank2):
    """Removes duplicates and returns a tuple."""

    if isinstance(name_at_rank2, tuple):
        # If it's already a tuple, create a set from its elements
        new_rank2_row = set(name_at_rank2)
    else:
        # If it's a single integer, create a set with just that integer
        new_rank2_row = {name_at_rank2}  # Use a set for efficient duplicate removal

    return tuple(new_rank2_row)  # Convert the set back to a tuple

def combine_tuples_dedupe(tuple1, tuple2):
  """combine tuple together or int & tuple"""
  unique_elements = set(tuple1) | set(tuple2)  # Combine and remove duplicates
  return tuple(unique_elements)


primary_existed_value = {}
primary_existed_value[data_set_pointer] = 1


def panda_tuple_display(my_dict):
    """pack up tuple for displaying in pan"""
    for key, value in my_dict.items():
        my_dict[key] = [value]
    return my_dict


def check_and_fill_dict(dic, check_range):
    """fill value to match with column amount
    """
    for i in range(check_range):
        if i not in dic:
            dic[i] = "None"
    return dic


#data["None"] = ["None"] * len(index_count)

# Creates pandas DataFrame.
data_set = pd.DataFrame(data, index=index_count)

data_set_pointer = data_set.loc[data_set_pointer]

new_df = pd.DataFrame(data_set_pointer).T
row_value = new_df.iloc[0]


#print(new_df)

index_dict = {}
for count,index_value in enumerate(data_set.index):
    index_dict[index_value] = acceptance_set[count]    






value_adding = None

row_value = row_value.tolist()

while len(row_value) > 0:
    unused_value = []
    for i in row_value:
        if isinstance(i, list):#this might not be needed
            i=tuple(i)
        value_adding = primary_existed_value.get(i,-1)
        if value_adding == -1:# if i not in primary_existed
            primary_existed_value[i] = 1
            #pull value out of compare list

            if isinstance(i, tuple):
                row_value_store = {}#supposed to store value each row
                for column_count in range(0,len(data.keys())):#loop equal to columns amount
                    new_rank2_row = ()

                    for count,j in enumerate(i):#iterate tuple like (2,4) into 2 then 4
                        #data_set_pointer= (data_set.loc[j]).tolist()#convert list value to individual list value
                        try:
                            name_at_rank2 = data_set.loc[j][column_count]
                            if name_at_rank2 == 'None':
                                continue
                        except Exception as e:
                            print('\nerror at:',column_count,j)
                        new_rank2_row = add_non_duplicate(name_at_rank2)

                        if row_value_store.get(column_count,-1) ==-1:
                            row_value_store[column_count]=  new_rank2_row
                        else:
                            row_value_store[column_count] = combine_tuples_dedupe(row_value_store[column_count],new_rank2_row)
                
                for key,values in row_value_store.items():
                    if len(values) ==1:
                        values = values[0]
                        row_value_store[key] = values
                    if primary_existed_value.get(values,-1) == -1:
                        unused_value.append(values)

                row_value_store = check_and_fill_dict(row_value_store,len(new_df.columns))
                row_value_store=panda_tuple_display(row_value_store)
                #print(row_value_store)
                
                pd_index = [repr(i)]
                
                new_row = pd.DataFrame(row_value_store, index=pd_index)
                #print(row_value_store)
                new_df = pd.concat([new_df, new_row], ignore_index=False)

            else:
                if i == "None":
                    row_value_store = {}
                    for i in range(0,len(data.keys())):
                        row_value_store[i]="None"
                    new_row = pd.DataFrame(row_value_store, index=["None"])
                    new_df = pd.concat([new_df, new_row], ignore_index=False)
                    continue
                new_rank2_row = data_set.loc[i]#this will pull requested row from origin dataset 
                for row_read in new_rank2_row.tolist():
                    if primary_existed_value.get(row_read,-1) == -1:
                        unused_value.append(row_read)
                new_rank2_row = pd.DataFrame(new_rank2_row).T
                new_df = pd.concat([new_df, new_rank2_row], ignore_index=False)
        else:
            pass
    row_value = unused_value
    #print(row_value)
        

#print(row_existed_value)
    
if __name__ == "__main__":
    print('\nIf complement:Set it to true   ## REMEMBER MANUAL VALUE--IT SHOULD BE THE MAXVALUE IN ALL ITERATION + 1##')
    new_df = add_acceptanceState(new_df,index_dict,if_complement=True,  manual_value=0)
    # print the data.
    print(new_df)


    print('\nIn total have ',len(new_df),'states\n')

#print('DO REMEMBER TO ADD ACCEPT REJECT STATE AND ARROW POINTER, Accept rejection state is an OR for every index in list\n')

