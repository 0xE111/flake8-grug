

def test():
    response = requests.get('https://google.com')
    response.raise_for_status()
    print(response.text)

    response = requests.get('https://google.com')
    if not response.ok:
        exit(0)
    print(response.text)

    response = requests.get('https://google.com')
    print(response.text)
