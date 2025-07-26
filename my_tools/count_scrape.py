import requests
from bs4 import BeautifulSoup
from agents.tool import function_tool 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def format_number_to_words(number: int) -> str:
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f} billion"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f} million"
    elif number >= 1_000:
        return f"{number / 1_000:.1f} thousand"
    else:
        return str(number)

@function_tool
def get_account_total() -> str:
    """
    Scrapes the live h1 and h4 heading values from Asaan Mobile Account counter site and returns numeric and word format.
    """
    try:
        url = "https://amacounter.vrgworld.net:8080/AmaCounter/"
        response = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        h1 = soup.find("h1", {"id": "lblAmaAccountNo"})
        h1_val = int(h1.text.strip().replace(",", "")) if h1 else 0
        return {
            "Number of Accounts": f"{h1_val:,}",
            "Accounts in Word": format_number_to_words(h1_val)
        }
    except Exception as e:
        return f"Error: {e}"

# <h4 id="lblAmaAccountNoFigures">13.1 Million</h4>




