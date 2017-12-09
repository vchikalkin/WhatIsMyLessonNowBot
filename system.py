import os


def log(message):
    from settings import get_current_date_and_time
    print("------------------------------------")
    print("[{0}]".format(get_current_date_and_time()))
    print("User: {0} {1} (id = {2}) \nMessage: {3}".format(message.from_user.first_name,
                                                           message.from_user.last_name,
                                                           str(message.from_user.id),
                                                           message.text))
    print("------------------------------------\n")


def alert(message):
    print("------------------------------------")
    print("System Message: \n" + message)
    print("------------------------------------\n")


def read_file(file):
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        with open(file) as text_file:
            content = text_file.readline()
            return content
