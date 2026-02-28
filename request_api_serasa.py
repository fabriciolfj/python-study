import requests

from CreditInfo import CreditInfo

BASE_URL = "http://localhost:9000"

def get_credit_info(cpf: str) -> dict:
    url = f"{BASE_URL}/api/serasa/v1/{cpf}"

    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()

def main():
    cpf =  33

    data = get_credit_info(cpf)
    print(type(data))
    credit_info = CreditInfo.from_dict(data)

    print(credit_info)



if __name__ == "__main__":
    main()