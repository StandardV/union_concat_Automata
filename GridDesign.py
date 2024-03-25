import tkinter as tk

class MatrixInputApp:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.matrix = [[] for _ in range(cols)]  # List of lists representing columns
        
        self.entries = [[None for _ in range(rows)] for _ in range(cols)]
        
        self.create_widgets()
        
    def create_widgets(self):
        for j in range(self.cols):
            for i in range(self.rows):
                self.entries[j][i] = tk.Entry(self.master, width=5)
                self.entries[j][i].grid(row=i, column=j)
                
        submit_button = tk.Button(self.master, text="Submit", command=self.submit_matrix)
        submit_button.grid(row=self.rows, columnspan=self.cols, pady=10)
        
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_entries)
        clear_button.grid(row=self.rows+1, columnspan=self.cols, pady=5)
        
        # Bind the Return key event to the submit_matrix function
        self.master.bind('<Return>', self.submit_matrix)
        
    def submit_matrix(self, event=None):
        self.matrix = [[] for _ in range(self.cols)]
        for j in range(self.cols):
            for i in range(self.rows):
                self.matrix[j].append(str(self.entries[j][i].get()))
        
        print("Matrix:")
        for count,row in enumerate(self.matrix):
            print(count, ": [",end="")
            self.print_val(row)
            print("]",end="")
            if count < len(self.matrix)-1:
                print(',')

    def print_val(self, input_list:list):
        
        for count,i in enumerate(input_list):
            if i != "/":
                if "," in i:
                    print(f"({i})",end="")
                else:
                    print(i,end="")
            else:
                print('"None"',end="")
            
            if count < len(input_list)-1:
                print(',',end=" ")
            
    def clear_entries(self):
        for j in range(self.cols):
            for i in range(self.rows):
                self.entries[j][i].delete(0, tk.END)

def main():
    rows = 7
    cols = 3
    
    root = tk.Tk()
    root.title("Matrix Input")
    root.attributes('-topmost', True)
    app = MatrixInputApp(root, rows, cols)
    
    root.mainloop()

if __name__ == "__main__":
    main()