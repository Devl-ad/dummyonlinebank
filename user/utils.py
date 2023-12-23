from user.forms import CreateTXSBSerializer, CreateTXOBSerializer, CreateTXInSerializer


def getTxForm(type):
    if type == "DO":
        return CreateTXSBSerializer
    elif type == "OB":
        return CreateTXOBSerializer
    elif type == "IN":
        return CreateTXInSerializer
    else:
        return None
