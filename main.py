import tkinter

#build up the panel
root = tkinter.Tk()
root.geometry("500*350")

def login():
    print("Test")

frame = tkinter.Tkframe(master = root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

label = tkinter.TkLabel(master = frame, text ="Career Tasker" , text_font=("Roboto", 24))
label.pack(pady = 12, padx = 18)

entry1 = tkinter.TkEntry(master=frame, placeholder_text= "Task Title")
entry1.pack(pady = 12, padx = 10)

checkbox = tkinter.TkCheckbox(master=frame, text="Completed?")
checkbox.pack(pady=12, padx=10)

root.mainloop()
#build up the boxes to contain information

#request the user to enter the goals for the month to build the work list
#interact = input("add / complete / delete / set rewards")
#return1 = interact.lower()

#if return1 == "add":
#    add()
#if return1 == "complete":
#    complete()
#if return1== "delete":
#    delete()
#if return1 == "set rewards":
#    set_rewards()

#show the list, exp, reward points in the panel

#reset the list per day

#if reward points met, pop out a window

#character growth panel

#create the 7 day plan
#days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#def weekly_plan():

#    plan = []
#    for days in days_of_the_week:
#        plan.append(days)
#        plan.append("")

#all the functions
def add():
    addTitle = input("Title: ")
    addContent = input("Content: ")

    return addTitle, addContent

