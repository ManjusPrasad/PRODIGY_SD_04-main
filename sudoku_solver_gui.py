import tkinter as tk
from tkinter import messagebox
import time
class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        title_label = tk.Label(self.root, text=" 🧩Sudoku Solver", font=("Helvetica", 26, "bold"),
                       bg="#fef6e4", fg="#001858", pady=10)
        title_label.grid(row=0, column=0, columnspan=9)
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#fef6e4")
        self.entries = []
        self.create_grid()
        self.create_buttons()
    def load_example_puzzle(self):
        puzzle = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ] 

        self.clear_grid()  
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, str(puzzle[i][j]))

    def add_hover_effect(self,entry, normal_bg, hover_bg):
        def on_enter(event):
            event.widget.config(bg=hover_bg)
        def on_leave(event):
            try:
                event.widget.config(bg=event.widget.cell_bg)  
            except AttributeError:
                pass 
        entry.bind("<Enter>", on_enter)
        entry.bind("<Leave>", on_leave)
    def create_grid(self):
        vcmd = (self.root.register(self.validate_cell), "%P")
        for i in range(9):
            row = []
            for j in range(9):
                if (i // 3 + j // 3) % 2 == 0:
                    cell_bg = "#c1f0f1"
                else: 
                    cell_bg = "#bee6e6"
                entry = tk.Entry(self.root, width=4, font=("Arial", 18), justify="center",
                                 bg=cell_bg, fg="#001858", borderwidth=2, relief="ridge",highlightthickness=0,
                                 validatecommand=vcmd,validate="key")
                entry.cell_bg = cell_bg
                print(f"Setting cell_bg for Entry at ({i},{j}):", cell_bg)
                pad_x = 2
                pad_y = 2
                if j in [2, 5]:
                    pad_x = 10
                if i in [2, 5]:
                    pad_y = 10

                entry.grid(row=i+1, column=j, padx=(2, pad_x), pady=(2, pad_y))
                self.add_hover_effect(entry, cell_bg, "#58bcd8")
                row.append(entry)
            self.entries.append(row)
    def validate_cell(self, new_value):
        if new_value == "":
            return True
        return new_value.isdigit() and 1 <= int(new_value) <= 9 and len(new_value) == 1
    def find_best_cell(self, board):
        min_options = 10
        best_cell = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    options = [n for n in range(1, 10) if self.is_valid(board, n, i, j)]
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (i, j)
                        if min_options == 1:
                            return best_cell  
        return best_cell


    def create_buttons(self):
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_with_animation,
                                 font=("Arial", 14), bg="#8bd3dd", fg="#001858", width=10)
        self.solve_button.grid(row=10, column=2, columnspan=2, pady=10)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid,
                                 font=("Arial", 14), bg="#f582ae", fg="#001858", width=10)
        self.clear_button.grid(row=10, column=4, columnspan=2, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit,
                                font=("Arial", 14), bg="#ffc6ff", fg="#001858", width=10)
        self.exit_button.grid(row=10, column=6, columnspan=2, pady=10)
        self.load_button = tk.Button(self.root, text="Load Puzzle", command=self.load_example_puzzle,
                        font=("Arial", 14), bg="#caffbf", fg="#001858", width=12)
        self.load_button.grid(row=11, column=3, columnspan=3, pady=10)

        self.add_hover_effect(self.load_button, "#caffbf", "#b2fab9")

        self.add_hover_effect(self.solve_button, "#8bd3dd", "#6dc9e0")
        self.add_hover_effect(self.clear_button, "#f582ae", "#f25d94")
        self.add_hover_effect(self.exit_button, "#ffccf9", "#ffbdf4")
    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get().strip()
                if val == "":
                    row.append(0)
                elif val.isdigit():
                    num = int(val)
                    if 1 <= num <= 9:
                        row.append(num)
                    else:
                        messagebox.showerror("Invalid Input ❌", f"Invalid number '{val}' at cell ({i+1}, {j+1}). Please enter numbers between 1 and 9.")
                        return None  
                else:
                    messagebox.showerror("Invalid Input ❌", f"Invalid character '{val}' at cell ({i+1}, {j+1}). Please enter digits only.")
                    return None  
            board.append(row)
        return board
    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(bg=entry.cell_bg)
                entry.delete(0, tk.END)
                if board[i][j] != 0:
                    entry.insert(0, str(board[i][j]))
                    entry.config(bg=self.entries[i][j].cell_bg, fg="#001858") 
                else:
                    entry.config(bg=self.entries[i][j].cell_bg, fg="#001858")
                entry.config(bg=self.entries[i][j].cell_bg)
                print(f"Restoring bg at ({i},{j}):", entry.cell_bg)
                entry.cell_bg = entry.cget("bg") 

    def clear_grid(self):
        for row in self.entries:
            for cell in row:
                cell.delete(0, tk.END)
                cell.config(bg="white")
    def solve_with_animation(self):
        self.solve_button.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.exit_button.config(state="disabled")
        self.load_button.config(state="disabled")
        try:
            board = self.get_board()
            if board is None:
                self.solve_button.config(state="normal")
                self.clear_button.config(state="normal")
                self.exit_button.config(state="normal")
                self.load_button.config(state="normal")
                return
            if self.solve_with_animation_helper(0, 0, board):
                print("Solved!")
            else:
                messagebox.showinfo("Sudoku Solver", "No solution exists.")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"Something went wrong:\n{str(e)}")
        finally:
            self.solve_button.config(state="normal")
            self.clear_button.config(state="normal")
            self.exit_button.config(state="normal")
            self.load_button.config(state="normal")
    def solve_with_animation_helper(self, row, col,board):
        best = self.find_best_cell(board)
        if not best:
            return True 
        i, j = best
        cell = self.entries[i][j]
        for num in range(1, 10):
            if self.is_valid(board,num, i,j):
                board[i][j] = num
                cell.delete(0, tk.END)
                cell.insert(0, str(num))
                cell.config(bg="#fcd5ce")  
                self.root.update()
                self.root.after(50)  
                if self.solve_with_animation_helper(i,j, board):
                   return True
                board[i][j] = 0
                cell.delete(0, tk.END)
                cell.config(bg="#f8edeb")  
                self.root.update()
                self.root.after(50)
        return False
    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            print("Board solved!")
            return True 
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, num, row, col):
                board[row][col] = num
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(num))
                self.entries[row][col].config(bg="#518be0")
                self.root.update()
                time.sleep(0.05)

                if self.solve(board):
                    return True
                board[row][col] = 0
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].config(bg=self.entries[row][col].cell_bg)
                self.root.update()
                time.sleep(0.05)
        return False
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None
    def is_valid(self,board, num, row, col):
        if num in board[row]:
           return False
        for i in range(9):
           if board[i][col] == num:
            return False
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
