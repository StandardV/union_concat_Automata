import pandas as pd

index_count_L = [0,1,2,3,4] #this is the identifier column

data_L = {0:  [(1,2),(1,2),3,4,(1,2)]
        #column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_L = [1,1,0,0,1] #this is the pointer of index_count row
 
data_set_L = pd.DataFrame(data_L, index=index_count_L)






index_count_R = [0,5,6,7,8] #this is the identifier column

data_R = {0:  [(5,6),"None",7,8,"None"]#column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_R = [0,1,0,0,1] #this is the pointer of index_count row
 
data_set_R = pd.DataFrame(data_R, index=index_count_R)









index_count_star = [0,1,2,3,4] #this is the identifier column

data_star = {0:  [(1,2),"None",3,4,"None"]#column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_star = [0,1,0,0,1] #this is the pointer of index_count row
 
data_set_star = pd.DataFrame(data_star, index=index_count_star)








def compare_and_combine(a, b):
    """compare and combine 2 elements"""

    if isinstance(a, int) and isinstance(b, int):
        return tuple(sorted([a, b]))
    elif isinstance(a, int) and isinstance(b, tuple):
        return tuple(sorted([a] + list(b)))
    elif isinstance(a, tuple) and isinstance(b, int):
        return tuple(sorted(list(a) + [b]))
    elif isinstance(a, tuple) and isinstance(b, tuple):
        return tuple(sorted(list(a) + list(b)))
    elif isinstance(a, int) and isinstance(b, str):
        return a
    elif isinstance(a, str) and isinstance(b, int):
        return b
    elif isinstance(a, tuple) and isinstance(b, str):
        return a
    elif isinstance(a, str) and isinstance(b, tuple):
        return b
    elif isinstance(a, str) and isinstance(b, str):
        return a if len(a) > len(b) else b


def set_union(L:pd.DataFrame,R:pd.DataFrame,Lacceptance,Racceptance):
    """union"""
    new_df = pd.DataFrame(columns=data_L.keys())

    tracking_column = {}
    combined_acceptance_set = []
    
    similar_indexes = L.index.intersection(R.index)
    
    #print(len(similar_indexes),similar_indexes)
    for i in similar_indexes:#list of overlap indexes    #put overlapped indexes row in first
        print(i)
        for column_count in range(0,len(new_df.columns)):

            tracking_column[column_count] = compare_and_combine(L[column_count][i],R[column_count][i])
        combined_acceptance_set.append((Lacceptance[i] or Racceptance[i]))
        new_row = pd.DataFrame([tracking_column], index=[i])
        new_df = pd.concat([new_df, new_row], ignore_index=False)
    #print(new_df)
    new_df['acceptance'] = combined_acceptance_set
    L['acceptance'] = Lacceptance
    R['acceptance'] = Racceptance

    for i in L.index.tolist():#list of overlap indexes    #put overlapped indexes row in first
        if i not in similar_indexes:
            #combined_acceptance_set.append(Lacceptance[i])
            new_row = pd.DataFrame([L.loc[i]], index=[i])
            new_df = pd.concat([new_df, new_row], ignore_index=False) 
        else:
            continue 

    for i in R.index.tolist():#list of overlap indexes    #put overlapped indexes row in first
        if i not in similar_indexes:
            
            #combined_acceptance_set.append(Racceptance[i])
            new_row = pd.DataFrame([R.loc[i]], index=[i])
            new_df = pd.concat([new_df, new_row], ignore_index=False) 
        else:
            continue
    return new_df.sort_index()

def set_concat(L:pd.DataFrame,R:pd.DataFrame,Lacceptance,Racceptance):
    """concat"""
    new_df = pd.DataFrame(columns=data_L.keys())

    combined_acceptance_set = []

    first_Right_li = (R.iloc[0]).tolist()


    for pos_count,i in enumerate(Lacceptance):
      #print(i)
      if i == 1:
        tracking_column = {}
        for column_count,column_value in enumerate((L.iloc[pos_count]).tolist()):
            input_1,input_2,output = column_value,first_Right_li[column_count],compare_and_combine(column_value,first_Right_li[column_count])
            #print(input_1,input_2,output,type(output))
            tracking_column[column_count] = output
        combined_acceptance_set.append((Lacceptance[pos_count] and Racceptance[0]))
        new_row = pd.DataFrame([tracking_column], index=[L.index.values[pos_count]])
        new_df = pd.concat([new_df, new_row], ignore_index=False)
        # Adding an additional column to the concatenated dataset from the list
        
      else:
        re_write_L = L.iloc[pos_count]
        combined_acceptance_set.append(0)
        re_write_L = pd.DataFrame(re_write_L).T
        new_df = pd.concat([new_df, re_write_L], ignore_index=False)
    #also need to generate new acceptance
    #print(combined_acceptance_set)
    setR_without_first_row = R.iloc[1:]
    combined_acceptance_set+=Racceptance[1:]
    new_df = pd.concat([new_df, setR_without_first_row], ignore_index=False)

    new_df['acceptance'] = combined_acceptance_set
    return new_df.sort_index()


def set_star(input_set,set_acceptance):
    """add star"""
    set_acceptance[0] = 1

    data_set_pointer = input_set.iloc[0]

    new_df = pd.DataFrame(data_set_pointer).T

    combined_acceptance_set = [1]

    first_Right_li = (data_set_pointer).tolist()

    for i in range(1,len(set_acceptance)):
      if set_acceptance[i] == 1:
        tracking_column = {}
        for column_count,column_value in enumerate((input_set.iloc[i]).tolist()):
            input_1,input_2,output = column_value,first_Right_li[column_count],compare_and_combine(column_value,first_Right_li[column_count])
            #print(input_1,input_2,output,type(output))
            tracking_column[column_count] = output
        combined_acceptance_set.append((set_acceptance[i] or set_acceptance[0]))

        new_row = pd.DataFrame([tracking_column], index=[input_set.index.values[i]])

        new_df = pd.concat([new_df, new_row], ignore_index=False)
        # Adding an additional column to the concatenated dataset from the list
        
      else:
        re_write_L = input_set.iloc[i]
        combined_acceptance_set.append(0)
        re_write_L = pd.DataFrame(re_write_L).T
        new_df = pd.concat([new_df, re_write_L], ignore_index=False)
    #print(combined_acceptance_set)
    new_df['acceptance'] = combined_acceptance_set
    return new_df


#print(data_set_L)
#print(data_set_R)



print(set_concat(data_set_L,data_set_R,acceptance_set_L,acceptance_set_R))
#print(set_union(data_set_L,data_set_R,acceptance_set_L,acceptance_set_R))
#print(set_star(data_set_star,acceptance_set_star))