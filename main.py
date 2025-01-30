import time
from functions import (get_credentials_from_env, enter_credentials_to_website, 
                       download_reports)

if __name__ == "__main__":
    credential_list = get_credentials_from_env()
    driver = enter_credentials_to_website(credential_list)
    # driver = find_account_by_search("Eve Waugh", driver)
    driver = download_reports(driver)
    
    