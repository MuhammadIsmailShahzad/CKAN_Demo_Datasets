# CKAN_Demo_Datasets

This repo contains demo datasets in the `resources` folder being used to create datasets on CKAN instances by running python script available in the `script` folder.

## Running the script

* The script is written in python3. So run the script
  ```
  python3 script.py
  ```
* It is going to ask for `CKAN_SITE_URL`. Provide the site url with `http://` and make sure no extra `/` are there at the end of the address. For example, enter the site address in format `http://ckan:5000`
* Next it is going to ask for the `API_KEY` (API_KEY of a sys_admin ckan user) which must be provided.
* Enter the name of organization you want to be added in small letters without spaces. For example `test-org-1`. After creating the org and adding the users and datasets to it will ask for the name of organization again. Enter the name of second organization you want to be added.
* The script will create two users `test_user_1` and `test_user_2`. Both the organizations are going to be owned (admin rights) by any one of the user.
* One `csv` and one `geojson` is going to be added to both the organizations.

## Rerunning the script

* If you want to rerun the script. Make sure the previously added datasets and organizations by the script are **deleted** and **purged**. Then rerun the script.