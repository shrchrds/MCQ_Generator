import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file")
            
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format only pdf and text file supported")
    
def get_table_data(quize_str):
    try:
        #convert the quiz from str to dict
        print(f"Quiz in String format {quize_str}")
        print(type(quize_str))
        quiz_dict = json.loads(quize_str)
        print(f"Quiz in Dictionary format {quiz_dict}")
        print(type(quiz_dict))
        quiz_table_data = []

        # iterate over the quize dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ":mcq, "Choces":options, "Correct":correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False