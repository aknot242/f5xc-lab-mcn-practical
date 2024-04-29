"""Module managing an XC CE Site"""
import time 
import requests
import boto3
import yaml
import urllib3

urllib3.disable_warnings()
  
def fetch_metadata(url: str, max_retries: int=5) -> dict|None:
    """
    Fetch metadata.
    Retry up to max_retries if the request fails.
    """
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Fetch Metadata Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("Fetch Metadata Max retries reached. Giving up.")
                return None

def find_aws_cred(cloud_accounts: dict) -> dict|None:
    """
    Find the first cloud account with "type": "AWS_API_CREDENTIAL".
    Return a dict containing the cred.
    """
    try:
        for account in cloud_accounts.get("cloudAccounts", []):
            for credential in account.get("credentials", []):
                if credential.get("type") == "AWS_API_CREDENTIAL":
                    return credential
    except Exception as e:
        return None
    
def find_user_tags(meta_tags: list, tags: list) -> dict|None:
    """
    Find user_tags from instance metadata.
    Return a dict with all b64 decoded tags needed for this service.
    """
    try:
        all_tags = meta_tags[0].get("userTags", [])
        user_tags = {}
        tag_list = [t for t in all_tags if t.get("name") in tags]
        for tag in tag_list:
            user_tags[tag["name"]] = tag["value"]
    except Exception as e:
        return None
    if len(user_tags) == len(tags):
        return user_tags
    else:
        print(f"Unable to find User Tags.")
        return None
        
def query_metadata(metadata_base_url: str="http://metadata.udf") -> dict|None:
    """
    Query metadata service.
    """
    #Deployment Info
    deployment = fetch_metadata(f"{metadata_base_url}/deployment")
    if deployment is None:
        print("Unable to find Deployment Metadata.")
        return None
    #Runner Info
    runner_user_tags = find_user_tags(fetch_metadata(f"{metadata_base_url}/userTags/name/XC/value/runner"), ["LabID"])
    if runner_user_tags is None:
        print("Unable to find Runner Metadata.")
        return None
    #AWS Info
    aws_credential = find_aws_cred(fetch_metadata(f"{metadata_base_url}/cloudAccounts"))
    if aws_credential is None:
        print("Unable to find AWS Metadata.")
        return None
    #
    try:
        return {
            "depID": deployment.get("deployment")["id"],
            "labID": runner_user_tags.get("LabID"),
            "awsSecret": aws_credential.get("secret"),
            "awsKey": aws_credential.get("key")
        }
    except (KeyError, IndexError) as e:
        print(f"Error extracting metadata: {e}")
        return None

def fetch_lab_info(metadata: dict) -> dict|None:
    """
    Get Lab Info from S3.
    """
    try:
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id=metadata['awsKey'],
            aws_secret_access_key=metadata['awsSecret']
        )
        obj = client.get_object(Bucket='orijen-udf-lab-registry', Key=f"{metadata['labID']}.yaml")
        data = obj['Body'].read().decode('utf-8')
        info = yaml.safe_load(data)
        return info
    except Exception as e:
        print(f"Error retrieving lab info: {e}")
        return None

def fetch_ce_info(metadata: dict, labInfo: dict, metadata_base_url: str="http://metadata.udf") -> dict:
    try:
        ce_ip = fetch_metadata(f"{metadata_base_url}/userTags/name/XC/value/CE")[0]["mgmtIp"]
        ce_port = "65500"
        ce_url = f"https://{ce_ip}:{ce_port}/api/ves.io.vpm/introspect/read/ves.io.vpm.health"
        headers = {'Authorization': labInfo['siteStatic']['auth']}
        cluster_name = f"cluster-{metadata['depID'].split('-')[0]}"
        return {
            "url": ce_url,
            "headers": headers,
            "site_name": cluster_name
        }
    except Exception as e:
        raise Exception(e)
    
def get_ce_state(ce_info: dict) -> dict:
    """
    Current CE State
    """
    try:
        response = requests.get(ce_info['url'], headers = ce_info['headers'], verify=False, timeout=1)
        response.raise_for_status()
        if response.status_code == 200 and response.json():
            ce_state = response.json()['state']
            return {
                "err": False,
                "state": ce_state,
                "site_name": ce_info['site_name']
            }
        else:
            raise Exception(e)
    except Exception:
        return {
            "err": True
        }

def get_ce_info():
    """
    Static CE Info
    """
    try:
        metadata = query_metadata()
        labInfo = fetch_lab_info(metadata)
        ce_info = fetch_ce_info(metadata, labInfo)
        ce_info['err'] = False
        if ce_info:
            return ce_info
        else:
            raise Exception
    except Exception:
        return {
            "err": True
        }