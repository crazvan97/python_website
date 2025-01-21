import requests
from requests.auth import HTTPBasicAuth


class TestRailWrapper:
    _initialize = None

    def __new__(cls, *args):
        if not cls._initialize:
            print("not initialized yet")
            cls._initialize = super().__new__(cls)
        else:
            print("initialized")
        return cls._initialize

    def __init__(self, testrail_url, user_email, user_token):
        if not hasattr(self, "testrail_url"):
            print("accessed __init__")
            self.testrail_url = testrail_url
            self.user_email = user_email
            self.user_token = user_token
            self.sesion = False
        else:
            print("not need to access __init__")

    def create_session(self):
        if self.sesion:
            print("Session created")
            return
        auth = HTTPBasicAuth(self.user_email, self.user_token)
        self.sesion = True
        print("Session exists")
        # response = requests.get(f'{self.testrail_url}/index.php?/api/v2/get_projects', auth=auth)
        #
        # if response.status_code == 200:
        #     print("Session created")
        #     self.sesion = auth
        # else:
        #     raise Exception(f"Authentication failed. Status code = {response.status_code}")

    def get_projects(self):
        if not self.sesion:
            print("Session not established. Call create_session() first.")
            return

        response = requests.get(f'{self.testrail_url}/index.php?/api/v2/get_projects', auth=self.sesion)

        if response.status_code == 200:
            print("Session created")
        else:
            raise Exception(f"Authentication failed. Status code = {response.status_code}")

def main():
    test_rail_object = TestRailWrapper("a","b","c")
    test_rail_object1 = TestRailWrapper("d", "e", "f")
    test_rail_object2 = TestRailWrapper("g", "h", "i")
    test_rail_object.create_session()
    test_rail_object1.create_session()
    test_rail_object2.create_session()
    print(test_rail_object2.testrail_url)

if __name__ == "__main__":
    main()