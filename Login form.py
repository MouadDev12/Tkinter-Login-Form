import tkinter as tk

# Create the main Tkinter window
root = tk.Tk()
root.title("Login Form")
root.geometry("400x300")


# Create labels and entry fields
login_label = tk.Label(root, text="Login" ,font=("Arial", 12, "bold") ,fg="blue" , bg="white" )
username_label = tk.Label(root, text="Username:" ,font=("Arial", 12) ,fg="blue" , bg="white" )
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="Password:" ,font=("Arial", 12) ,fg="blue" , bg="white" )
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create login button
login_button = tk.Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get() ,font=("Arial", 11) ,fg="blue" ,bg="green" ))
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10 ,sticky="news")

# Run the Tkinter event loop
root.mainloop()
