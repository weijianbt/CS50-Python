# CS50P Final Project 2023 - Fixed Deposit Manager
## Video Demo:  https://www.youtube.com/watch?v=4L8yXb9OupM
## Description:
This program can perform 2 tasks:

1. Allow users to key in bank name, principal amount, interest rate, tenure and deposit date. Then the program will calculate what is the maturity date, maturity amount, and nett earnings before inserting the entry into a csv file for storage

2. Allow users to view past entries that was inserted into the csv file.

By creating this program, we can easily track all of the the fixed deposits that we are interested in from multiple banks.

## Explaining the project

1. **Inserting new entries**:

    - A list of questions are defined and stored in the form of a dictionary called "questions_config", which allow easy access of the list of questions throughout the program. User will be required to respond to each of the questions.


            questions_config = {
                "bank" : "Input bank name: ",
                "principal_amount" : "Input principal amount (MYR): ",
                "interest" : "Input annual interest rate (%): ",
                "tenure" : "Input tenure (months): ",
                "deposit_date": "Input deposit date (yyyy-mm-dd): "
            }

    - To prompt the user for inputs, the program loops through the "questions_config" dictionary and based on the count from enumerating the dictionary, numbered questions were displayed for the user.

    - Validation functions are implemented for each user inputs. If the input passes the validation, the user will then only be allowed to answer the next question. However, instead of using a big "if-else" block to determine what question will need to go for which validation function, a "transmitter" function is implemented to pass the question type (etc: "bank") and user input (etc: "Bank ABC") to the validation function whereby user inputs will be validated based on appropriate logics.


                def valid_input(ques_type,user_in):
                    match ques_type:
                        case "bank":
                            return validate_bank(user_in)
                        case "principal_amount":
                            return validate_principal_amount(user_in)
                        case "interest":
                            return validate_interest(user_in)
                        case "tenure":
                            return validate_tenure(user_in)
                        case "deposit_date":
                            return validate_deposit_date(user_in)
                        case _:
                            print("no valid question")
                            sys.exit()

    - When each of the validation passes, the answers to each question will be inserted into the "valid_answers" dictionary as the value of the "value" key. In the "valid_answers" dictionary, a key called "unit" is included, this is so that when displaying the answers in table form using the tabulate module later on, the "question_type" will be concatenated with the "unit" (etc: "principal_amount (MYR)") which would easily allow the user to know what kind of data is being inserted.

                valid_answers = {
                    "q1" : {
                        "question_type" : "bank",
                        "unit"          : None,
                        "value"         : None
                    },

                    "q2" : {
                        "question_type" : "principal_amount",
                        "unit"          : "MYR",
                        "value"         : None
                    },

                    "q3" : {
                        "question_type" : "interest",
                        "unit"          : "%",
                        "value"         : None
                    },
                    "q4": {
                        "question_type" : "tenure",
                        "unit"          : "month",
                        "value"         : None
                    },
                    "q5": {
                        "question_type" : "deposit_date",
                        "unit"          : None,
                        "value"         : None
                    },
                }
    - After answering the questions and passing all validation checks,the program will prompt the user for confirmation on whether to proceed with the current data through the get_confirmation() function. The tabulate module is used to display the user input as a table, allowing an easier visualization of what data were inserted.

    - A function called edit_inputs() was implemented to re-display the questions based on the question number if the user decides to modify the current entry. The program will prompt the user to key in which question number that needs to be edited. The questions are displayed by program by searching for the question number key (etc: "q1" for re-entering bank name). If the user key in a question number that do not exist, the program will prompt the user to select the correct question number. The total number of questions are defined by using the len() function the "question_config" dictionary.

    - Once the user confirmed the entry, the program will calculate the maturity date, maturity amount, and nett amount in the process_inputs() function and then:

        1. Display the entry in the terminal window in the form of a table using the tabulate module.
        2. Insert the entry into the database using the csv module's DictWriter.


    - The write_into_db() function will take care of inserting the new data into the database. Since the program has an existing table generated when user first answered the questions. 2 functions were written to merge the existing table containing only the bank, principal_amount, interest, tenure & desposit date with the calculation output, which is the maturity_amount, nett_amount & maturity_date.

<br>

2. **Viewing past entries**

    - To view past entries, the program will read the existing csv file with a DictReader from the csv module and populate the table using the tabulate module.

<br>

3. **Including new questions for user input**

    - The program is written such that if a new question is required to be added, there are 3 changes that needs to be done:
        1. Add the question type and question as a key-value pair in the "questions_config" dictionary.
        2. In the get_fd_details() function, modify the "valid_answers" dictionary by incrementing the question number (etc: "q6") and add the "question_type", "unit", "value" as a key value pair to the question number.
        3. In the valid_input() function, add a match case for the new "ques_type".

<br>

4. **Test functions on all user inputs**

    - Additional test functions has been created to validate all user input functions to ensure all corner cases are accounted for.


## Potential future enhancement

1. Implement "edit" and "delete" function for existing entries in the database to allow user to modify and delete any entries.
2. Implement compound interest calculator to allow user to gain insights on how much the money grows overtime.
