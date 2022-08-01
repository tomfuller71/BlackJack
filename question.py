class Question:

  @classmethod
  def get_bool_YN_response(cls, question):
    response = cls.get_response_from_list(question, ["Yes", "No"])
    return response == "Yes"

  @classmethod
  def get_response_from_list(cls,
    question,
    valid_responses,
    allow_first_char_only=True
  ):
    question = question.strip() + " >> "
    parsed_list = [*valid_responses]

    if allow_first_char_only:
      parsed_list = [e.upper()[0] for e in valid_responses]

    response = ""
    while True:
      response = input(question)
      if allow_first_char_only:
         response = response.upper().strip()[0]
      
      if response in parsed_list:
        break
      else:
        print("Invalid selection")

    return valid_responses[parsed_list.index(response)]

  @classmethod
  def get_numeric_response(cls, question, min=None, max=None, num_type=int):
    num = 0
    question = question.strip() + " >> "

    def is_valid(response):
      nonlocal num
      try:
        num = num_type(response)

      except ValueError:
        return False
      finally:
        if min != None and num < min:
          return False
        elif max != None and num > max:
          return False
        else:
          return True

    def print_error_message():
      error_str = "Must be a number"
      if min != None and max != None:
        error_str += f" between {min} and {max}"
      elif min != None:
        error_str += f" greater than {min}"
      else:
        error_str += f" less than {max}"
      error_str += "."
      print(error_str)

    while True:
      if is_valid(input(question)):
        break
      else:
        print_error_message()

    return num