from functions import get_credentials_from_env, enter_credentials_to_website, check_successful_login

if __name__ == "__main__":
    credential_list = get_credentials_from_env()
    driver = enter_credentials_to_website(credential_list)
    check_successful_login(driver)