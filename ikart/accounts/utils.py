import uuid



def genarate_ref_code():

    code=str(uuid.uuid4()).replace("-","")[:6]
    return code



