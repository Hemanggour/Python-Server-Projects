import google.generativeai as ai
from . import APIs

def GenerateContent(Query):
    try:
        ai.configure(api_key=APIs.api('gemini'))
        model = ai.GenerativeModel("gemini-1.5-flash")
        res = (model.generate_content(Query))
    except Exception as err:
        print(f"Error In GenerateContent: {err}")
    else:
        return res.text