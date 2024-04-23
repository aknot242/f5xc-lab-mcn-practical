from orijenpy import session, site, registration
import sys
import time

def get_token():
    token = ''
    return token

def get_tenant_url():
    tenant = ''
    return tenant

def get_registrations(reg) -> list|None:
    try:
        p = reg.list_by_state_payload(state='PENDING')
        new_regs = reg.list_by_state(p)
        return new_regs
    except Exception as e:
        print(f"Failed to get registrations: {e}")
        return None
    
def approve_registration(reg, object) -> bool:
    try:
        reg_name = reg._get_reg_name(object)
        passport = reg._get_passport(object)
        p = reg.approve_payload(reg_name, passport)
        return True
    except Exception as e:
        print(f"Failed to approve registration: {e}")
        return False

def site_upgrade_os(site, reg, object: dict, version: str = '7.2009.45') -> bool:
    try:
        cluster_name = reg._get_cluster_name(object)
        payload = site.upgrade_payload(cluster_name, version)
        site.upgrade_os(payload, cluster_name)
        return True
    except Exception as e:
        print(f"Failed to submit site OS upgrade: {e}")
        return False

def main():
    """
    Main Function
    """
    try:
        tenant = get_tenant_url()
        api_token = get_token()
        auth = session(tenant_url=tenant, api_token=api_token)
        this_reg = registration(auth)
        this_site = site(auth)
    except Exception as e:
        print(f"Unable to get API client: {e}")
        print("Exiting.")
        sys.exit(1)

    retries = 0
    max_retries = 6
    retry_delay = 60

    while retries < max_retries:    
        regs = get_registrations(this_reg)
        if regs:
            for obj in regs:
                reg_success = approve_registration(this_reg, obj)
                upgrade_success = site_upgrade_os(this_site, this_reg, obj)
                if reg_success and upgrade_success:
                    print(f"Successfully Approved and Sent Upgrade for {this_reg._get_cluster_name(obj)}.")
                    retries = 0
                else:
                    retries += 1
                    print(f"Error Approving and Upgrading for {this_reg._get_cluster_name}")
                    pass
                time.sleep(retry_delay)
        else:
            print(f"No Registrations to process. Sleeping for {retry_delay}s.")
            time.sleep(retry_delay)
    print("Max retries reached. Exiting.")
    sys.exit(1)


if __name__ == "__main__":
    main()
