import pickle as pk
import pandas as pd
import os 
import union_concat_star
import NFA_to_DFA


dir_path = os.path.dirname(os.path.realpath(__file__))


column_dict = {}

try:
    with open("".join([dir_path, '\\dataframeStore.txt']), 'rb') as f:
        column_dict = pk.load(f)
except EOFError:
    column_dict = {}



index_count_holder = [0,1,2] #this is the identifier column
data_holder = {
    
0 : [1, 1, "None"],
1 : [2, 2, "None"],
2 : ["None", "None", "None"]


    #column and cell values
        }#Column name have to specifically follow 0,1,2,3,4
acceptance_set_star = [0,0,1] #this is the pointer of index_count row
data_set_holder = pd.DataFrame(data_holder, index=index_count_holder)




def create_dataFrame(number_list, column_var:list, left_val ): #3   , [1,2,3] , 2
    """Numberlist is value assigned to value, left val is value and column_var are given column""" 
    assign_dict = {}

    current_dict_name = str(left_val)+" "+str(number_list)+str(column_var)

    if current_dict_name in column_dict:
        print('taking optimized path')
        return column_dict[current_dict_name]


    current_val = left_val

    index_count_mod = [0,0]#left side identifier
    data_struct = [["None","None"] for _ in range(0,len(column_var)) ]  #basically a dict that pair column var
    current_counter = number_list
    #print(current_counter)
    for count, columnvalue in enumerate(column_var):
        if columnvalue == current_val: #if current column value is the digit detected
            index_count_mod[1] = current_counter
            data_struct[count][0] = current_counter
        else:
            pass
    for dict_count ,i in enumerate(data_struct):#create a dictionary for pandas column
        assign_dict[dict_count] = i  
    current_set = pd.DataFrame(assign_dict, index=index_count_mod)
    #print(current_set)
    column_dict[current_dict_name] = current_set
    
    with open("".join([dir_path, '\\dataframeStore.txt']), 'wb') as f:
        pk.dump(column_dict, f)

    
    return current_set

def printname():
    for key, value in column_dict.items() :
        print(key)

def delete_specific_Val(input_value):
    if column_dict.get(input_value,-1) != -1:
        del column_dict[input_value]
        with open("".join([dir_path, '\\dataframeStore.txt']), 'wb') as f:
            pk.dump(column_dict, f)

    else:
        print('No value of that name')

def clear_all():
    column_dict.clear()

    with open("".join([dir_path, '\\dataframeStore.txt']), 'wb') as f:
        pk.dump(column_dict, f)



if __name__ == "__main__":
    print('not supporting short dfa to nfa yet, too lazy: do it on other script')
    #pulling value out of """column_dict"


    #print(create_dataFrame(3,[1,2,3],3))#space or U or *
    printname()
    #print(column_dict)
    #clear_all()
    #dictionary to store it in pickle



    #print(union_concat_star.set_concat(column_dict['2 3[1, 2, 3]'],column_dict['1 6[1, 2, 3]'],[0,1],[0,1]))
    #print(union_concat_star.set_union(data_set_L,data_set_R,acceptance_set_L,acceptance_set_R))
    #print(union_concat_star.set_star(data_set_star,acceptance_set_star))