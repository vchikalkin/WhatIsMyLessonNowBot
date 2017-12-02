import settings


def log(message):
    print("-----------------------------")
    print("[{0}]".format(settings.get_current_date_and_time()))
    print("User: {0} {1} (id = {2}) \nMessage: {3}".format(message.from_user.first_name,
                                                           message.from_user.last_name,
                                                           str(message.from_user.id),
                                                           message.text))
    print("-----------------------------\n")


def alert(message):
    print("------------------------------------")
    print("System Message: \n" + message + "\n------------------------------------\n")
