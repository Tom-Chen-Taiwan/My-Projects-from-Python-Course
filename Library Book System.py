#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

title = ["所有的過去，都將以另一種方式歸來",
         "惡意如何帶來正義？：被誤解的第四種行為",
         "開始在英國自助旅行",
         "寫過就不忘！韓文自學達人的單字整理術",
         "城邦國際名表",
         "Beautiful World, Where Are You",
         "What If? 2 : Additional Serious Scientific Answers to Absurd Hypothetical Questions",
         "Lonely Planet’s Best in Travel 2022",
         "Think Again: The Power of Knowing What You Don’t Know",
         "Thinking, Fast and Slow"]
genre = ["文學",
         "科學",
         "旅遊", 
         "語言學習", 
         "流行",
         "Literature",
         "Science",
         "Travel",
         "Finance",
         "Psychology"]
language = ["Chinese","Chinese","Chinese", "Chinese", "Chinese", "English", "English", "English", "English", "English"]
number = [20712, 20908, 20710, 20901, 20707, 20907, 20913, 20402, 20518, 20531]
status = ["In", "In", "In", "Out", "In", "Out", "Out", "In", "In", "Out"]
return_date = ["No", "No", "No", "2022-10-10", "No", "2022-10-15", "2022-11-10", "No", "No", "2022-12-10"]


library = pd.DataFrame({"Number": number, "Title": title, 
                        "Genre": genre, "Language": language,
                        "Status": status,
                        "Return Date": return_date})

library.to_csv("library.csv")


# Library Book System
import sys
import pandas as pd
from datetime import datetime, timedelta
import re

class Library:
    
    def __init__(self):
        # return current library dataset
        self.library = pd.read_csv("library.csv").drop(columns = ["Unnamed: 0"])
        # reset index starting from 1
        self.library.index += 1 
        
    # inquire the user's password to log into the system    
    def Login(self):    
        while True:
            password = input("Enter your password(Ex:1234): ").strip()
            if password == "1234":
                print("Log in successfully!")
                break
            else:
                continue     
        
    # list all books            
    def ListBook(self):
        return self.library
    

    
    # use keyword to search titles
    def TitleKeywordSearch(self):
        while True:
            word = input("Enter Title Keyword: ").title().strip()
            if self.library[self.library["Title"].apply(lambda x: word in x)].empty == False:
                return self.library[self.library["Title"].apply(lambda x: word in x)]
            else:
                print("No Result Found")
                continue

        
    # use keyword to search book genres    
    def GenreKeywordSearch(self):
        while True:
            word = input("Enter Genre Keyword: ").title().strip()
            if self.library[self.library["Genre"].apply(lambda x: word in x)].empty == False:
                return self.library[self.library["Genre"].apply(lambda x: word in x)]
            else:
                print("No Result Found")
                continue

            
    # use reference number to retrieve the book
    def BookNumberSearch(self):
        while True:
            number = input("Enter book reference number(Ex: 20907): ").strip()
            
            # if the number is less than length 5, it prompts the user again
            if len(number) != 5:
                print("Reference number must be 5 digits!")
                continue
            # if the number is not in digit, it prompts the user again
            elif number.isdigit() == False:
                print("Reference number must be digits!")
                continue
                
            if self.library[self.library["Number"].apply(lambda x: int(number) == int(x))].empty == False:
                return self.library[self.library["Number"].apply(lambda x: int(number) == int(x))]
            else:
                print("No Result Found")
                continue

        
    # insert new book information into the database    
    def AddBook(self):
        
        # empty lists to store data
        ref_number = []
        title = []
        genre = []
        language = []
        status = []
        return_date = []
        
        # inquire the number of books to add into the dataset
        number_books_to_add = int(input("How many books to add in? "))
        
        # use while loop to iterate the inputs
        while number_books_to_add > 0:
            
            # inquire the user for reference book
            number = input("Enter book reference number(Ex: 20907): ").strip()
            
            # if the number is less than length 5, it prompts the user again
            if len(number) != 5:
                print("Reference number must be 5 digits!")
                continue
            # if the number is not in digit, it prompts the user again
            elif number.isdigit() == False:
                print("Reference number must be digits!")
                continue
                    
            ref_number.append(number)
            title.append(input("Enter book title: ").title().strip())
            genre.append(input("Enter book genre: ").title().strip())
            language.append(input("Enter book's language (Ex: Chinese or English): ").title().strip())
            status.append(input("Is book 'In' or 'Out'? ").title().strip())
            return_date.append(input("Enter the return date (Ex: 2022.10.10): ").title().strip())
                
            # making a new library dataset
            new_library = pd.DataFrame({"Number": number, 
                                        "Title": title, 
                                        "Genre": genre, 
                                        "Language": language, 
                                        "Status": status, 
                                        "Return Date": return_date})
            new_library = pd.concat([self.library, new_library],axis=0)
            new_library = new_library.reset_index()
            new_library.index += 1
            new_library = new_library.drop(columns = ["index"])
            number_books_to_add -= 1

        new_library.to_csv("library.csv")
        return new_library
    
    # delete book from the database          
    def DeleteBook(self):
        while True:
            ref_num = input("Enter the reference number of the book: ")

            # if the number is not equal to length 5, it prompts the user again
            if len(ref_num) != 5:
                print("Reference number must be 5 digits!")
                continue

            # if the number is not in digit, it prompts the user again
            elif ref_num.isdigit() == False:
                print("Reference number must be digits!")
                continue

            # check if the book is in the library
            if self.library[self.library["Number"].apply(lambda x: x== int(ref_num))].empty == False:

                # get book index
                book_index = list(self.library[self.library["Number"] == int(ref_num)].index)

                # remove the book by using its index in drop fuction
                self.library = self.library.drop(book_index[0])
                print ("The book has been successfully deleted.")

                # update the library
                self.library.to_csv("library.csv")
                self.library = self.library.reset_index()
                self.library.index += 1
                self.library = self.library.drop(columns = ["index"])
                return self.library
            else:
                return ("The book does not exist.")
        
    
    # check if book is in or out of the library
    def CheckStatus(self):
        ref_num = input("Enter the reference number of the book: ")
        if self.library[self.library["Number"] == int(ref_num)].empty == False:
            
            # get book index to get value in "Status" 
            book_index = list(self.library[self.library["Number"] == int(ref_num)].index)
            if self.library["Status"][book_index[0]] == "In":
                print("The book is currently in the library.")
            elif self.library["Status"][book_index[0]] == "Out":
                print("The book is currently out of the library.", f"The return date is {self.library['Return Date'][book_index[0]]}")
        else:
            print("The book does not exist.")
                                
    # borrow a book from the library
    def BorrowBook(self):            
        while True:
            book_borrow = input("Enter book reference number(Ex: 20907): ")
            
            # if the number is not equal to length 5, it prompts the user again
            if len(book_borrow) != 5:
                print("Reference number must be 5 digits!")
                continue
                
            # if the number is not in digit, it prompts the user again
            elif book_borrow.isdigit() == False:
                print("Reference number must be digits!")
                continue
                
            if self.library[self.library["Number"] == int(book_borrow)].empty == False:
                
                # get book index
                book_index = list(self.library[self.library["Number"] == int(book_borrow)].index)
                if self.library["Status"][book_index[0]] == "In":
                    borrow_or_not = input("The book is currently in the library. Do you want to borrow the book? (Y/N)? ").upper().strip()
                    if borrow_or_not == "Y":
                        # count a 30 days period of borrowing
                        # current time
                        today = datetime.now() 
                        # current time + 30 days
                        borrow_period = today + timedelta(days = 30) 
                        # make into string format
                        borrow_period = f"{borrow_period.year}-{borrow_period.month}-{borrow_period.day}" 
                        # update the info
                        self.library["Return Date"][book_index[0]] = self.library["Return Date"][book_index[0]].replace("No", borrow_period)
                        self.library["Status"][book_index[0]] = self.library["Status"][book_index[0]].replace("In", "Out")
                        # update the library
                        self.library.to_csv("library.csv")
                        print ("You have successfully borrowed the book.")
                        return self.library
                    else:
                        sys.exit("See you next time!")                 
                else:
                    return "Sorry! The book is currently out of the library", f"The return date is {self.library['Return Date'][book_index[0]]}"
            else:
                return "No Result Found!"
    
    def ReturnBook(self):
        while True:
            book_to_return = input("Enter the reference number of the book: ").strip()
            # if the number is not equal to length 5, it prompts the user again
            if len(book_to_return) != 5:
                print("Reference number must be 5 digits!")
                continue
            # if the number is not in digit, it prompts the user again 
            elif book_to_return.isdigit() == False:
                print("Reference number must be digits!")
                continue
            
            if library[library["Number"] == int(book_to_return)].empty == False:
                # get book index
                book_index = list(self.library[self.library["Number"] == int(book_to_return)].index)
                # update the info using regular expression
                self.library["Return Date"][book_index[0]] = re.sub(r"^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}", "No", self.library["Return Date"][book_index[0]])
                self.library["Status"][book_index[0]] = self.library["Status"][book_index[0]].replace("Out", "In")
                # update the library
                self.library.to_csv("library.csv")
                print("You have successfully returned the book.")
                return self.library
              
              
lib = Library()      
lib.Login()
lib.ListBook()
lib.TitleKeywordSearch()
lib.GenreKeywordSearch()
lib.BookNumberSearch()
lib.AddBook()
lib.CheckStatus()
lib.BorrowBook()
lib.ReturnBook()
lib.DeleteBook()
