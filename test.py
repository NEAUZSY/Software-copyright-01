import tkinter as tk
from tkinter import messagebox as msgbox

root = tk.Tk()
root.withdraw()
rv= msgbox.showinfo('i\'m showinfo','Now you are at www.pynote.net! Welcome...:)')
print(rv)
root.wm_deiconify()
root.mainloop()