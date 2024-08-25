import sys
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import csv
import os

def main():

    #do you want to insert new entry or view history
    introduction = """
    Welcome to fixed deposit manager!
    Press 1 to view past entries.
    Press 2 to insert new entries.
    """
    print(introduction)

    while True:
        try:
            desired_action = int(input("Please select which action you want to perform: "))

            if desired_action == 1 or desired_action == 2:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please key in either 1 or 2")

    if desired_action == 1:
        print_db()
    else:
        user_inputs = get_fd_details()
        while True:
            confirmed_input = get_confirmation(user_inputs)

            if confirmed_input == False:
                user_inputs = edit_inputs(user_inputs)
                continue
            else:
                break

        calculation_output = process_inputs(confirmed_input)
        write_into_db(confirmed_input, calculation_output)

def print_db():

    table_data = []
    try:
        with open("output.csv","r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                table_data.append(row)

        print(tabulate(table_data,headers="keys",tablefmt="simple_grid"))
    except FileNotFoundError:
        print("There is no output file. Please key in some data first")
        sys.exit()


def edit_inputs(user_inputs):

    #display questions
    for count , key in enumerate(questions_config):
        # question_type = key
        question = questions_config[key]
        question = question.replace(":","")
        print(f"Q{count+1}: {question}",sep="\n")

    total_question = len(questions_config)

    #allow user to edit inputs before inserting into storage
    while True:
        question_number = input("Which input you want to change? Please key in question number. Such as 1, 2, 3 etc: ")
        try:
            if 1 <= int(question_number) <= total_question:
                break
            else:
                continue
        except ValueError:
            print(f"Please ensure question number is between 1 and {total_question}")

    new_question = user_inputs[f"q{question_number}"]["question_type"]

    while True:
        new_answer = input(f"{questions_config[new_question]}")
        if not valid_input(new_question,new_answer) == False:
            user_inputs[f"q{question_number}"]["value"] = new_answer
            return user_inputs
        else:
            continue

def get_fd_details():

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


    for count , key in enumerate(questions_config):
        question_type = key
        question = questions_config[key]

        while True:
            user_input=input(f"Question {count+1} - {question}")
            if not valid_input(question_type,user_input) == False:
                # valid_answers[question_type] = user_input
                valid_answers[f"q{count+1}"]["value"] = user_input
                break
            else:
                continue

    # print(valid_answers)
    return valid_answers


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


def validate_bank(user_in):
    if len(user_in) > 0:
        return True
    else:
        return False

def validate_principal_amount(user_in):
    err_msg = "Please key in whole number larger than 0 and without any symbols"
    # clean_user_in = user_in.replace(",","")

    try:
        if int(user_in) > 0:
            return int(user_in)
        else:
            print(err_msg)
            return False

    except ValueError:
        print(err_msg)
        return False


def validate_interest(user_in):
    err_msg = "Please key in a a number between 0 to 100"

    try:
        if float(user_in) > 0 and float(user_in) < 100:
            return True
        else:
            print(err_msg)
            return False
    except ValueError:
        print(err_msg)
        return False


def validate_tenure(user_in):
    err_msg = "Please key in a whole number > 1"

    try:
        if int(user_in) > 0:
            return True
        else:
            print(err_msg)
            return False
    except ValueError:
        print(err_msg)
        return False

def validate_deposit_date(user_in):
    err_msg = "Please ensure format is yyyy-mm-yy and date is valid"

    try:
        valid_date = datetime.strptime(user_in,"%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        print(err_msg)
        return False


def get_confirmation(user_inputs):

    # table_data = generate_input_table(user_inputs)

    input_table_header, input_table_data = extract_input_table_info(user_inputs)
    generated_table = generate_input_table(input_table_header, input_table_data)

    print(generated_table)

    while True:
        ask_user = input("Do you confirm to insert the above details into database? (Y/N) ").lower()
        if ask_user == "y":
            return user_inputs
        elif ask_user == "n":
            return False
        else:
            print("Please choose Y/N")
            continue

def extract_input_table_info(user_inputs):
    table_header_list = []
    table_data_list = []
    for _, key in enumerate(user_inputs):
        unit = user_inputs[key]["unit"]
        if unit == None:
            table_header = user_inputs[key]["question_type"]
        else:
            table_header = f"{user_inputs[key]['question_type']} ({user_inputs[key]['unit']})"

        table_header_list.append(table_header)

        table_data = user_inputs[key]["value"]
        table_data_list.append(table_data)

    return (table_header_list, table_data_list)


def extract_output_table_info(calculation_output):

    table_header_list = list(calculation_output.keys())
    table_data_list = list(calculation_output.values())

    return (table_header_list,  table_data_list)


def generate_input_table(input_table_header,input_table_data):

    output_table = tabulate([input_table_data], headers=input_table_header, tablefmt="simple_grid")

    return output_table

def generate_output_table(calculation_output):

    output_table = tabulate([calculation_output],headers="keys",tablefmt="simple_grid")

    return output_table

def generate_final_table(input_table_header, input_table_data, output_table_header, output_table_data):

    final_header = input_table_header + output_table_header
    final_data = input_table_data + output_table_data

    final_table = tabulate([final_data],headers=final_header, tablefmt="simple_grid")

    return final_table

def process_inputs(checked_inputs):
    '''
    interest calculation = P + (P x r x t/100)
    P = principal amount you deposit
    r = rate of interest per annum
    t = tenure in years

    '''
    # print(checked_inputs)

    # principal_amount = float(checked_inputs["q2"]["value"])
    # interest = float(checked_inputs["q3"]["value"])
    # tenure = float(checked_inputs["q4"]["value"])

    principal_amount, interest, tenure, deposit_date = return_input_values(checked_inputs)

    maturity_amount = principal_amount + (principal_amount * interest * (tenure/12) /100)
    nett_amount =  round(maturity_amount - principal_amount,2)
    maturity_date = add_months(deposit_date, tenure)

    # print(f"Total amount: {maturity_amount}")
    # print(f"Nett earnings: {nett_amount}")

    answer_dict = {
        "maturity_amount" : maturity_amount,
        "nett_amount" : nett_amount,
        "maturity_date" : maturity_date
    }

    return answer_dict

def add_months(initial_date, months):
    new_date = initial_date + relativedelta(months=months)
    new_date = datetime.strftime(new_date, "%Y-%m-%d")
    return new_date

def return_input_values(checked_inputs):
    principal_amount = float(checked_inputs["q2"]["value"])
    interest = float(checked_inputs["q3"]["value"])
    tenure = float(checked_inputs["q4"]["value"])
    deposit_date = datetime.strptime(checked_inputs["q5"]["value"],"%Y-%m-%d")

    return (principal_amount, interest, tenure, deposit_date)

def return_output_values(calculation_output):
    maturity_amount = float(calculation_output["maturity_amount"])
    nett_amount = float(calculation_output["nett_amount"])

    return (maturity_amount,nett_amount)

def write_into_db(confirmed_input, calculation_output):

    input_table_header, input_table_data = extract_input_table_info(confirmed_input)
    output_table_header, output_table_data = extract_output_table_info(calculation_output)

    final_header = input_table_header + output_table_header
    final_data = input_table_data + output_table_data

    output_file = 'output.csv'
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='') as f:
        csv_writer = csv.writer(f)
        if not file_exists:
            csv_writer.writerow(final_header)

        csv_writer.writerows([final_data])

    final_table = generate_final_table(input_table_header, input_table_data, output_table_header, output_table_data)

    print("This entry has been inserted into the csv file for storage")
    print(final_table)


questions_config = {
    "bank" : "Input bank name: ",
    "principal_amount" : "Input principal amount (MYR): ",
    "interest" : "Input annual interest rate (%): ",
    "tenure" : "Input tenure (months): ",
    "deposit_date": "Input deposit date (yyyy-mm-dd): "
}


if __name__ == '__main__':
    main()



