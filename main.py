from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import json
import random

asked = []
#A lambda function is a small anonymous function(usually we dont need to reuse it)
#A lambda function can take any number of arguments, but can only have one expression 
class Start(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

#First frame users will see which is the login screen 
      
        self.border = LabelFrame(self, text='Login', bg='ivory', bd = 10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx = 150, pady=150)
        
        self.user_label = Label(self.border, text="Username", font=("Arial Bold", 15), bg='ivory')
        self.user_label.place(x=50, y=20)
        self.user_entry = Entry(self.border, width = 30, bd = 5)
        self.user_entry.place(x=180, y=20)
        
        self.password_label = Label(self.border, text="Password", font=("Arial Bold", 15), bg='ivory')
        self.password_label.place(x=50, y=80)
        self.password_entry = Entry(self.border, width = 30, show='*', bd = 5)
        self.password_entry.place(x=180, y=80)
      
#This is just the design layout numbers I used for the layout of my login screen, the password length, width, etc. 
      
        def verify():
            try:
                with open("users.txt", "r") as f:
                    info = f.readlines()
                    i  = 0
                    for e in info:
                        self.user_name, self.user_password =e.split(",")
                        if self.user_name.strip() == self.user_entry.get() and self.user_password.strip() == self.password_entry.get():
                            controller.show_frame(Second)
                            i = 1
                            break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Couldnt open file")
#this is for when the users dont enter anything he program will say different messages for different empty slections the "except" code is for if users dont submit anything during the login fram and the "if" code is for when users dont submit anything during the register frame.
     
         
        self.submitbutton = Button(self.border, text="Submit", font=("Arial", 15), command=verify)
        self.submitbutton.place(x=320, y=115)
        
        def register():
            register_window = Tk()
            register_window.resizable(0,0)
            register_window.configure(bg="ivory")
            register_window.title("Register")
            reg_name_label = Label(register_window, text="Username:", font=("Arial",15), bg="ivory")
            reg_name_label.place(x=10, y=10)
            reg_name_entry = Entry(register_window, width=30, bd=5)
            reg_name_entry.place(x = 200, y=10)
            
            reg_password_label = Label(register_window, text="Password:", font=("Arial",15), bg="ivory")
            reg_password_label.place(x=10, y=60)
            reg_password_entry = Entry(register_window, width=30, show="*", bd=5)
            reg_password_entry.place(x = 200, y=60)
            
            confirm_password_label = Label(register_window, text="Confirm Password:", font=("Arial",15), bg="ivory")
            confirm_password_label.place(x=10, y=110)
            confirm_password_entry = Entry(register_window, width=30, show="*", bd=5)
            confirm_password_entry.place(x = 200, y=110)

#register frame code above, this is the code that allows users to regirster and make an account that enable them to take the quiz.
            
            def check():
                if reg_name_entry.get()!="" or reg_password_entry.get()!="" or confirm_password_entry.get()!="":
                    if reg_password_entry.get()==confirm_password_entry.get():
                        with open("users.txt", "a") as f:
                            f.write(reg_name_entry.get()+","+reg_password_entry.get()+"\n")
                            messagebox.showinfo("Welcome","You are registered successfully!!")
                            register_window.destroy()
                    else:
                        messagebox.showinfo("Error","Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                    
            self.register_button = Button(register_window, text="Sign in", font=("Arial",15), bg="#ffc22a", command=check)
            self.register_button.place(x=170, y=150)
            
            register_window.geometry("470x220")
            register_window.mainloop()
            
        self.register_button = Button(self, text="Register", bg = "dark orange", font=("Arial",15), command=register)
        self.register_button.place(x=650, y=20)

class Second(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    
    self.title_label = Label(self, text="Welcome To the General Mathematic & Scientific Quiz", bg = "ivory", font=("Arial Bold", 20))
    self.title_label.place(x=40, y=150)     
#this is the second frame, this is the frame the program will take the users to once they have signed in.
# maths
  
    self.take_quiz = Button(self, text="Take Quiz", font=("Arial", 15), command=lambda: controller.show_frame(QuestionsContainer))
    self.take_quiz.place(x=650, y=450)
    
    self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Start))
    self.back_button.place(x=100, y=450)



class Third(Frame):
  def __init__(self, parent, controller):
    
    Frame.__init__(self, parent)
    
    self.configure(bg='ivory')
    
    self.app_label = Label(self, text="Store some content related to your \n project or what your application made for. \n All the best!!", bg = "orange", font=("Arial Bold", 25))
    self.app_label.place(x=40, y=150)
    
    self.home_button = Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(Start))
    self.home_button.place(x=650, y=450)
    
    self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Second))
    self.back_button.place(x=100, y=450)

class QuestionsContainer(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.questions = []
    self.buttons = []
    self.current_question_number = 1
    self.controller = controller
    

    self.answer_score = {
      "correct": 0,
      "incorrect": 0
    }

#This code is for the program to collect the data that the users put in, whether they get it correct or incorrect. This is also used to transfer the data to the data section which is used to calculate whether the user passes or not.
    
    self.load_questions('questions.json')
    
    self.create_question_answers()

    self.exit_button = Button(self, text="Exit", font=("Arial", 15), command=lambda: controller.show_frame(Start))
    self.exit_button.place(x=650, y=450)
    
    self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Second))
    self.back_button.place(x=100, y=450)

#this is where the program takes a random question from my questions.json file and imports them to the quiz.
  '''
  call it validate_question
    - takes question
  '''

  def create_question_answers(self):
    self.title_label = Label(self, text="{}/{} - {}".format(self.current_question_number,len(self.questions), self.current_question['question']), bg = "ivory", font=("Arial Bold", 20))
    self.title_label.place(x=40, y=80)        

    self.offset = 0
    for question_answer in self.current_question['answers']:
        answer_btn = Button(self, text=question_answer, font=("Arial", 15), command=lambda selected_answer=question_answer: self.validate_question(selected_answer))
        answer_btn.place(x=80, y=140 + self.offset)
        self.offset += 60
        self.buttons.append(answer_btn)

#offset = the spacing and alignment,

  def validate_question(self, selected_answer):
    '''
    if we select the right answer: we add 1 to correct otherwise we add 1 to incorrect.
    '''
    self.current_question_number += 1
    print(selected_answer, self.current_question["correct_answer"])
    if (self.current_question["correct_answer"] == selected_answer):
      self.answer_score['correct'] += 1
    else:
      self.answer_score['incorrect'] += 1

#this is where the program adds a point for whatever the user get incorrect +1 correct +1. 
    
    if self.current_question_number <= len(self.questions):
      for btn in self.buttons:
        btn.destroy()
      
      self.title_label.destroy()
      
      self.current_question = self.questions[self.get_random_question_index()]
      self.create_question_answers()
    else:
      print(self.answer_score)
      #save correct and incorrect score to file.
      with open('score.json', 'w') as fp:
        json.dump(self.answer_score, fp)
    
      self.controller.show_frame(End)
    
  def get_random_question_index(self):
    # gets a random non repeated number from the number of 
    global qnum
    no_of_questions = len(self.questions)
    qnum = random.sample(range(no_of_questions), 1)
    if qnum not in asked:
      asked.append(qnum)
    elif qnum in asked:
      self.get_random_question_index()
    return qnum[0]
  
  def load_questions(self, questions_file_name):
    #reads the json file
    f = open(questions_file_name)
    data = f.read()
    self.questions = json.loads(data)
  
    self.current_question = self.questions[self.get_random_question_index()]

    
class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
      
        self.window = Frame(self)
        self.window.pack()
        
        self.window.grid_rowconfigure(0, minsize = 500)
        self.window.grid_columnconfigure(0, minsize = 800)
        
        self.frames = {}
        for F in (Start, Second, Third, QuestionsContainer, End):
            frame = F(self.window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(Start)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Maths & Sceince Quiz")

class End(Frame):
  def __init__(self, parent, controller):
    
    Frame.__init__(self, parent)
    
    self.configure(bg='ivory')
  
    #Read the saved score and display it.
    f = open("score.json", "r")
    data = f.read()
    self.answers = json.loads(data)
    self.passing_score = (self.answers["correct"] + self.answers["incorrect"]) // 2
    self.correct_score = self.answers["correct"]
    
    self.title_label = Label(self, text="What is your score?", bg = "ivory", font=("Arial Bold", 20))
    self.title_label.place(x=40, y=80)  

    self.your_score = Label(self, text="You got: {}".format(self.correct_score), bg = "ivory", font=("Arial Bold", 20))
    self.your_score.place(x=40, y=180)

    self.your_score = Label(self, text="Passing score: {}".format(self.passing_score), bg = "ivory", font=("Arial Bold", 20))
    self.your_score.place(x=40, y=220)    

    self.pass_or_fail = ""

    #if you got >= to passing_score
    #self.pass_or_fail = "passed" else self.pass_or_fail = "fail"

    if self.correct_score >= self.passing_score:
      self.pass_or_fail = "passed"
    else:
      self.pass_or_fail = "failed"
      
    
    self.your_score = Label(self, text="You have {}".format(self.pass_or_fail).format(self.passing_score), bg = "ivory", font=("Arial Bold", 20))
    self.your_score.place(x=40, y=290)  
    
    
    self.home_button = Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(Start))
    self.home_button.place(x=650, y=450)


      
#start of program
if __name__ == '__main__':           
    app = Application()
    app.maxsize(800,500)
    app.mainloop()