import string

class StringHandler:
  def __init__(self):
    pass

  def separate_into_list(self, string_data : str, separator : str) -> list[str]:
    if len(separator)!=1:
      raise Exception("Separator size is not one.")

    data = string_data.split(separator)
    data = [x for x in data if len(x) > 0]
    return data

  def list_to_str(self, string_list : list[str] , separator : str) -> str:
    if len(separator)!=1:
      raise Exception("Separator size is not one.")
    return separator.join(string_list)

  def __del__(self):
    pass
