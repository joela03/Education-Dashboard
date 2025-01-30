import time
from functions import (get_credentials_from_env, enter_credentials_to_website,
                       check_successful_login, find_account_by_search,
                       verify_valid_account_found)

if __name__ == "__main__":
    credential_list = get_credentials_from_env()
    driver = enter_credentials_to_website(credential_list)
    driver = check_successful_login(driver)
    driver = find_account_by_search("Eve Waugh", driver)
    
    