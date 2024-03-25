import pandas as pd
import numbers



 
#THE FOLLOWING IMPLEMENT PSEUDO FILLING VALUE
# input_string = "(0*1)*0(0*1)*"

# #call function with def input(0 , 1, [6,7], [0,1,2], union/star/concat)  # remember to form a string int list: 0U1 for example
# union_flag   = False


# number_list = [1,2,3,4,5]
# column_var = [0,1,2]

# placeholder_var = 0 
# acceptance_set = [0,1]


# index_count_mod = [0,placeholder_var]#left side identifier
# data_struct = [["None","None"] for _ in range(0,len(column_var)) ]  #basically a dict that pair column var
# #data_struct = {0:[var_from_numberlist if match column var,"None"]* len(column_var)  #basically a dict that pair column var

# column_dict = {}
# value_stack = []

# counter=0


# for current_val in input_string:
#     if_prev_digit = False
#     #if current_val is U
#     #if current_val is concat
#     #if current_val is star
#     if current_val.isdigit():#parsing the string if value is int
#         if_prev_digit = True

#         current_val = int(current_val)
#         current_counter = number_list[counter]
#         print(current_counter)
#         counter+=1
#         for count, columnvalue in enumerate(column_var):
#             if columnvalue == current_val: #if current column value is the digit detected
#                 index_count_mod[1] = current_counter
#                 data_struct[count][0] = current_counter
#             else:
#                 pass

#         for dict_count ,i in enumerate(data_struct):#create a dictionary for pandas column
#             column_dict[dict_count] = i  
#         current_set = pd.DataFrame(column_dict, index=index_count_mod)

#     if if_prev_digit is True and len(value_stack) >= 2: #this is concat:

#         if union_flag == True:
#             union_flag = False
#     else:
#         if current_val == "*":
#             return 1
#         elif current_val == "U":
#             union_flag = True
    
#if value in columnvar fit num from input string, add that same numberlist iterative to index_count_mod, datastruct
#



index_count_L = [0,2] #this is the identifier column

data_L = {

0 : [2, "None"],
1 : ["None", "None"],
2 : ["None", "None"]


        #column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_L = [0,1] #this is the pointer of index_count row
 
data_set_L = pd.DataFrame(data_L, index=index_count_L)






index_count_R = [0,3] #this is the identifier column

data_R = {
    
0 : ["None", "None"],
1 : [3, "None"],
2 : ["None", "None"]
    
    #column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_R = [0,1] #this is the pointer of index_count row
 
data_set_R = pd.DataFrame(data_R, index=index_count_R)









index_count_star = [0,1,2] #this is the identifier column

data_star = {
    
0 : [1, 1, "None"],
1 : [2, 2, "None"],
2 : ["None", "None", "None"]
    #column and cell values
        }#Column name have to specifically follow 0,1,2,3,4


acceptance_set_star = [0,0,1] #this is the pointer of index_count row
 
data_set_star = pd.DataFrame(data_star, index=index_count_star)








def compare_and_combine(a, b):
    """compare and combine 2 elements"""
    #panda have a weird behavior where we assign the column with all int, it will give them data type of numpy.int64 but if column comprised of string and int it will give string and int 64 only
    #due to this, a use of numbers.intergral is needed as it look for the common in numbers: (This class is a base class for all built-in integral types, including int and np.int64.)
    if isinstance(a, numbers.Integral) and isinstance(b, numbers.Integral):
        return tuple(sorted([a, b]))
    elif isinstance(a, numbers.Integral) and isinstance(b, tuple):
        return tuple(sorted([a] + list(b)))
    elif isinstance(a, tuple) and isinstance(b, numbers.Integral):
        return tuple(sorted(list(a) + [b]))
    elif isinstance(a, tuple) and isinstance(b, tuple):
        return tuple(sorted(list(a) + list(b)))
    elif isinstance(a, numbers.Integral) and isinstance(b, str):
        return a
    elif isinstance(a, str) and isinstance(b, numbers.Integral):
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

    first_Right_li = (R.iloc[0]).tolist()#pick first row on the right, convert all to list


    for pos_count,i in enumerate(Lacceptance):#iterate in left  acceptance
      #print(i)
      if i == 1:#if 1 perform action
        tracking_column = {}
        for column_count,column_value in enumerate((L.iloc[pos_count]).tolist()):#convert current left row to list and iterate by column
            input_1,input_2,output = column_value,first_Right_li[column_count],compare_and_combine(column_value,first_Right_li[column_count])
            #print(input_1,input_2,output,type(output))
            #print(column_value,(first_Right_li[column_count]), f'pick:{compare_and_combine(column_value,first_Right_li[column_count])}')
            tracking_column[column_count] = output
        combined_acceptance_set.append((Lacceptance[pos_count] and Racceptance[0]))
        new_row = pd.DataFrame([tracking_column], index=[L.index.values[pos_count]])
        new_df = pd.concat([new_df, new_row], ignore_index=False)
        # Adding an additional column to the concatenated dataset from the list
        
      else:#if 0 perform action
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

if __name__ == "__main__":

    #print(set_concat(data_set_L,data_set_R,acceptance_set_L,acceptance_set_R))
    #print(set_union(data_set_L,data_set_R,acceptance_set_L,acceptance_set_R))
    #print(set_star(data_set_star,acceptance_set_star))
    print('')