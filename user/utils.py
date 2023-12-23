from user.forms import CreateTXSBSerializer, CreateTXOBSerializer


def getTxForm(type):
    if type == "DO":
        return CreateTXSBSerializer
    elif type == "OB":
        return CreateTXOBSerializer
    elif type == "IN":
        return "Inter bak"
    else:
        return None
