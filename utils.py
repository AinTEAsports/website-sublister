import requests
import termcolor


def subname_exists(websiteUrl : str, name : str) -> tuple():
    """Fuction that returns if a website subfolder/subfile exists

    Args:
        websiteUrl (str) : the website's URL
        name (str) : the name of the file/folder you want to verify that exists
        type (str) : the type of what you want to verify ('file' or 'folder')
    
    Returns:
        (bool), (int), (str) : returns if the file/folder exists in the website, the status code and some text information
    """
    
    try:
        response = requests.get(f"{websiteUrl}/{name}")
    except requests.exceptions.ConnectionError:
        error_code = termcolor.colored("\n[!] '{websiteUrl}/{name}' is not a valid URL", 'red')
        print(error_code)
        return False, 404, "URL is invalid"


    # You can check all the return codes meaning and infos on https://kinsta.com/blog/http-status-codes/
    return_codes = {
        '200' : {'returnvalue' : True, 'text' : "Resource found successfully"},
        '204' : {'returnvalue' : True, 'text' : "No content"},
        '205' : {'returnvalue' : True, 'text' : "Reset content"},

        '300' : {'returnvalue' : True, 'text' : "Multiple choice"},
        '301' : {'returnvalue' : True, 'text' : "Resource moved permanently"},
        '302' : {'returnvalue' : True, 'text' : "Resource moved but found"},
        '304' : {'returnvalue' : False, 'text' : "You accessed the file/folder before but it is no longer existing"},
        '307' : {'returnvalue' : False, 'text' : "Redirect, HTTP process not allowed to redirect"},
        '308' : {'returnvalue' : False, 'text' : "Redirect, HTTP process not allowed to redirect"},

        '400' : {'returnvalue' : False, 'text' : "Bad request"},
        '401' : {'returnvalue' : True, 'text' : "Unauthorized / Authorization required"},
        '402' : {'returnvalue' : True, 'text' : "Payment required"},
        '403' : {'returnvalue' : True, 'text' : "Unauthorized"},
        '404' : {'returnvalue' : False, 'text' : "Not found"},
        '405' : {'returnvalue' : True, 'text' : "Method not allowed"},
        '406' : {'returnvalue' : True, 'text' : "Not acceptable response"},
        '407' : {'returnvalue' : True, 'text' : "Proxy authentication required"},
        '408' : {'returnvalue' : False, 'text' : "Conflict"},
        '410' : {'returnvalue' : False, 'text' : "The requested resource is gone and won't be coming back"},
        '411' : {'returnvalue' : True, 'text' : "Lenght required"},
        '412' : {'returnvalue' : True, 'text' : "Precondition Failed"},
        '413' : {'returnvalue' : True, 'text' : "Payload too large"},
        '414' : {'returnvalue' : False, 'text' : "URL too long"},
        '415' : {'returnvalue' : False, 'text' : "Unsupported media type"},
        '416' : {'returnvalue' : False, 'text' : "Range not satisfiable"},
        '417' : {'returnvalue' : False, 'text' : "Expectation Failed"},
        '418' : {'returnvalue' : False, 'text' : "I'm a teapot"},
        '422' : {'returnvalue' : False, 'text' : "Unprocessable entity"},
        '451' : {'returnvalue' : False, 'text' : "Unavailible for legal reasons"},
    }

    status_code = str(response.status_code)

    if not status_code in return_codes.keys():
        return response.ok, int(status_code), 'No information registered for this status code'

    return return_codes[status_code]['returnvalue'], int(status_code), return_codes[status_code]['text']
