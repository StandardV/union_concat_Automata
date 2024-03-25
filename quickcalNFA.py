import union_concat_star as leiss1
import pandas as pd
import pickle


input_string = "1*"

#call function with def input(0 , 1, [6,7], [0,1,2], union/star/concat)  # remember to form a string int list: 0U1 for example
union_flag   = False


number_list = [1]
column_var = [1,2,3]

placeholder_var = 0 
acceptance_set = [0,1]



#data_struct = {0:[var_from_numberlist if match column var,"None"]* len(column_var)  #basically a dict that pair column var

column_dict = {}





def function_process(number_list:list, column_var:list, process_type:str, left_val = None , right_val = None):  
    value_stack = []
    current_val = left_val
    if_star = 2

    if process_type == "*":
        if_star = 1

    for i in range(if_star):
        index_count_mod = [0,placeholder_var]#left side identifier
        data_struct = [["None","None"] for _ in range(0,len(column_var)) ]  #basically a dict that pair column var
        current_counter = number_list[i]
        #print(current_counter)
        for count, columnvalue in enumerate(column_var):
            if columnvalue == current_val: #if current column value is the digit detected
                index_count_mod[1] = current_counter
                data_struct[count][0] = current_counter
            else:
                pass
        for dict_count ,i in enumerate(data_struct):#create a dictionary for pandas column
            column_dict[dict_count] = i  
        current_set = pd.DataFrame(column_dict, index=index_count_mod)
        value_stack.append(current_set)
        current_val = right_val

    #print(value_stack[0])
    #print(value_stack[1])
    if process_type == "U":
        return leiss1.set_union(value_stack[0],value_stack[1],acceptance_set,acceptance_set)
    elif process_type == "*":
        return leiss1.set_star(value_stack[0],acceptance_set)
    else: #process_type == concat
        return leiss1.set_concat(value_stack[0],value_stack[1],acceptance_set,acceptance_set)



counter=0
current_counter = number_list[0]




#if value in columnvar fit num from input string, add that same numberlist iterative to index_count_mod, datastruct

if __name__ == "__main__":
    print(function_process([3],[1,2,3],"*",3))#space or U or *
    #dictionary to store it in pickle

#add function to, read, delete, clear all, and use