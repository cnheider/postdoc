class ModelForm(object):
  def __init__(self, model):
    self.data = {}
    self.model = model
    no_params = [
      "metadata",
      "query",
      "query_class",
      "id",
      "user_id",
      "user",
      "created_at",
      ]
    self.attributes = [
      i for i in dir(self.model) if not i.startswith("_") and i not in no_params
      ]

  def is_valid(self):
    for key, value in self.data.items():
      if key in self.attributes:
        if value == "" or not value:
          return False

    return True

  def get(self, attr):

    return self.data.get(attr)
