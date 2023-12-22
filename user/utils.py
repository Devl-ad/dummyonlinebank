from user.forms import CreateTXSBSerializer


def getTxForm(type):
    if type == "DO":
        return CreateTXSBSerializer
    elif type == "OB":
        return "Other bank"
    elif type == "IN":
        return "Inter bak"
    else:
        return None
