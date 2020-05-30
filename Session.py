import pandas as pd


class Session:
    def __init__(self):  # jaki typ będzie miało
        self.stored_data = {}

    def get_all_data(self):
        return list(self.stored_data.keys())

    def get_data(self, name: str):
        if name in self.stored_data:
            return self.stored_data[name]
        else:
            raise DataNotFoundException

    def add_data(self, data, name: str) -> str:
        """
        Attempts to add data DataFrame to stored_data at key name.
        If name is already taken, a new name is generated and used as key.
        :returns key at which added data can be accessed
        """
        if name in self.stored_data:
            name = self.__generate_name(name)
        self.stored_data[name] = data
        return name

    def __generate_name(self, name: str) -> str:
        counter = 1
        while (name + str(counter)) in self.stored_data:
            counter += 1
        return name + str(counter)


class DataNotFoundException(Exception):
    pass
