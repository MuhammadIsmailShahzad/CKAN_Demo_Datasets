import requests
import json
import sys
from urllib.parse import urljoin
import os

# URL(s) for 2 geojson and 2 csv resources in alternate sequence
dataset_url= ['https://pkgstore.datahub.io/examples/geojson-tutorial/example/data/db696b3bf628d9a273ca9907adcea5c9/example.geojson',
              'https://raw.githubusercontent.com/datopian/CKAN_Demo_Datasets/main/resources/org1_sample.csv',
              'https://raw.githubusercontent.com/datopian/CKAN_Demo_Datasets/main/resources/sample.geojson',
              'https://raw.githubusercontent.com/datopian/CKAN_Demo_Datasets/main/resources/org2_sample.csv']

def start_workflow():
    BASE_URL, API_KEY = get_ckan_url()
    url_status = check_url(BASE_URL)    
    if url_status != 200:
        start_workflow()
    create_user(BASE_URL, API_KEY)
    create_org(BASE_URL, API_KEY)

def get_ckan_url():
    '''
    Gets the ckan_url and API key from the user
    '''
    print('Please provide complete CKAN_SITE_URL e.g http://ckan:5000')
    BASE_URL = input()
    print('Enter the API Key')
    API_KEY = input()
    return BASE_URL, API_KEY

def check_url(BASE_URL):
    '''
    Check if the url provided is accessible
    '''
    try:
        resp = requests.get(BASE_URL)
        return resp.status_code
    except:
        print('Please recheck the url provided')

def create_user(BASE_URL, API_KEY):
    '''
    Creates three ckan users
    '''
    print('Creating SYS_ADMIN user')
    name = 'admin_scriptgen'
    email = 'your_email@example.com'
    password = 'Testpassword1'
    try:
        no_users = 3
        for user in range(no_users):
            data = {
                'name': 'test_user_{0}'.format(user), 
                'email': 'your_email@example',
                'password': 'Testpassword{0}'.format(user)
                }
            resp = requests.post(
                urljoin(BASE_URL, '/api/3/action/user_create'),
                data=data,
                headers = {'Authorization': API_KEY})
            if resp.status_code == 200:
                print('User Created: {0}'.format(data['name']))
    except Exception as e:
        print('Unable to create the user')
        print(e)

def org_member_create(org_id, username, role, BASE_URL, API_KEY):
    '''
    Add owners to the created organizations
    '''
    data = {
    'id': org_id,
    'username': username,
    'role': role  
    }
    resp = requests.post(
    urljoin(BASE_URL, '/api/3/action/organization_member_create'),
    data=data,
    headers={'Authorization': API_KEY},
    )
    print('MEMBERS ADDED')

def create_org(BASE_URL, API_KEY):
    '''
    Create an organization
    '''
    no_orgs = 2
    for org_index in range(no_orgs):
        print('Please Enter the name of Organization in small letters with "-" for spaces \nfor example test-org')
        org_id = input()
        resp = requests.get(
            urljoin(BASE_URL, '/api/3/action/organization_show?id={0}'.format(org_id)),
            headers={'Authorization': API_KEY}
        )

        if not resp.status_code == 200:
            data = {
            'name': org_id,
            'image_url': 'https://github.com/datopian/CKAN_Demo_Datasets/raw/main/resources/datopian.png'
            }
            resp = requests.post(
                urljoin(BASE_URL, '/api/3/action/organization_create'),
                data=data,
                headers={'Authorization': API_KEY},
            )
            username = 'test_user_{0}'.format(org_index)
            org_member_create(org_id, username, 'admin', BASE_URL, API_KEY)
            print('ORG {0} ADDED '.format(org_id))
        
        start_index = org_index * 2
        stop_index = start_index + 2
        for i in range(start_index, stop_index):
            dataset_name = 'test_dataset_{0}'.format(i)
            add_dataset(BASE_URL, API_KEY, org_id, dataset_name, dataset_url[i])

def add_dataset(BASE_URL, API_KEY, org_id, dataset_name, dataset_url, extras={}):
    '''
    Add dataset in the organizations
    '''
    data = {
      'maintainer': 'ckan_admin',
      'license_id': 'cc-by',
      'author': 'ckan_admin',
      'title': 'Test Dataset',
      'publisher': 'ckan_admin',
      'geographic_level': 'global',
      'maintainer_email': 'your_email@example.com',
      'information_classification': 'public-public-external',
      'visibility': 'public',
      'data_privacy_regulated': True,
      'data_privacy_country': ['ARG'],
      'author_email': 'your_email@example.com',
      'tag_string': 'test_tag',
      'notes': 'This is a test dataset generated through script api.',
      'owner_org': org_id,
      'name': dataset_name,
    }
    data.update(extras)
    resp = requests.post(
        urljoin(BASE_URL, '/api/3/action/package_create'),
        data=data,
        headers={'Authorization': API_KEY},
    )
    create_resource(BASE_URL, API_KEY, dataset_name, dataset_url)
    print('RESOURCE CREATED!')

def create_resource(BASE_URL, API_KEY, dataset_name, dataset_url):
    '''
    Add resource in datasets
    '''
    print('CREATING RESOURCE')
    data = {
      'package_id': dataset_name,
      'url': dataset_url,
      'name': dataset_name 
    }
    resp = requests.post(
        urljoin(BASE_URL, '/api/3/action/resource_create'),
        data=data,
        headers={'Authorization': API_KEY},
    )

if __name__ == '__main__':
    start_workflow()
