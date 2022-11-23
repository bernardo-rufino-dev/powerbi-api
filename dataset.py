import json
import requests
import pandas as pd
from typing import Dict
from utilities import create_directory


class Dataset:

    def __init__(self, token: str):
        """
        Initialize variables.
        """
        self.main_url = 'https://api.powerbi.com/v1.0/myorg'
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}
        self.data_dir = './data/datasets'

        create_directory(self.data_dir)


    def list_datasets(
                self, 
                workspace_id: str = '') -> Dict:
        """
        List all datasets on a specific workspace_id that the user has access to.

        Args:
            workspace_id (str, optional): workspace id to search datasets from.

        Returns:
            Dict: status message and content.
        """

        # Main URL
        request_url = f'{self.main_url}/groups/{workspace_id}/datasets'

        # If workspace ID was not informed, return error message...
        if workspace_id == '':
            return {'message': 'Missing workspace id, please check.', 'content': ''}

        # If workspace ID was informed...
        else: 
            filename = f'datasets_{workspace_id}.xlsx'

            # Make the request
            r = requests.get(url=request_url, headers=self.headers)

            # Get HTTP status and content
            status = r.status_code
            response = json.loads(r.content).get('value', '')

            # If success...
            if status == 200:
                # Save to Excel file
                df = pd.DataFrame(response)
                df.to_excel(f'{self.data_dir}/{filename}', index=False)
                
                return {'message': 'Success', 'content': response}

            else:                
                # If any error happens, return message.
                response = json.loads(r.content)
                error_message = response['error']['message']

                return {'message': {'error': error_message, 'content': response}}


    def add_user(
                self, 
                user_principal_name: str = '', 
                workspace_id: str = '', 
                dataset_id: str = '',
                access_right: str = 'Read',
                user_type: str = 'User') -> Dict:
        """
        Grants an user access to a specific dataset.

        Args:
            user_principal_name (str): user e-mail or identifier of service principal.
            workspace_id (str): workspace id to add the user to.
            dataset_id (str): dataset id to grant access to.
            access_right (str, optional): access right type. Defaults to 'Member'.
            user_type (str, optional): user type, 'SP' for service accounts. Defaults to 'user'.

        Returns:
            Dict: status message.
        """

        # If both, user, workspace and dataset are provided...
        if (user_principal_name != '') & (workspace_id != '') & (dataset_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/datasets/{dataset_id}/users'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Add user to dataset with the specified access right.
            # https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/post-dataset-user-in-group
            data = {
                "identifier": user_principal_name,
                "principalType": user_type,
                "datasetUserAccessRight": access_right
            }

            # Make the request
            r = requests.post(url=request_url, headers=headers, json=data)

            # Get HTTP status and content
            status = r.status_code

            # If success...
            if status == 200:
                return {'message': 'Success'}
            
            else:                
                # If any error happens, return message.
                response = json.loads(r.content)
                error_message = response['error']['details']['message']

                return {'message': {'error': error_message, 'content': response}}

        else:
            return {'message': 'Missing parameters, please check.'}


    def update_user(
                self, 
                user_principal_name: str = '', 
                workspace_id: str = '',
                dataset_id: str = '',
                access_right: str = 'Read',
                user_type: str = 'User') -> Dict:
        """
        Update an user access to a specific dataset.

        Args:
            user_principal_name (str): user e-mail or identifier of service principal.
            workspace_id (str): workspace id to add the user to.
            dataset_id (str): dataset id to grant access to.
            access_right (str, optional): access right type. Defaults to 'Member'.
            user_type (str, optional): user type, 'SP' for service accounts. Defaults to 'user'.

        Returns:
            Dict: status message.
        """

        # If both, user, workspace and dataset are provided...
        if (user_principal_name != '') & (workspace_id != '') & (dataset_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/datasets/{dataset_id}/users'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Add user to dataset with the specified access right.
            # https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/post-dataset-user-in-group
            data = {
                "identifier": user_principal_name,
                "principalType": user_type,
                "datasetUserAccessRight": access_right
            }

            # Make the request
            r = requests.put(url=request_url, headers=headers, json=data)

            # Get HTTP status and content
            status = r.status_code

            # If success...
            if status == 200:
                return {'message': 'Success'}
            
            else:                
                # If any error happens, return message.
                response = json.loads(r.content)
                error_message = response['error']['code']

                return {'message': {'error': {'status': status, 'description': error_message}, 'content': response}}

        else:
            return {'message': 'Missing parameters, please check.'}


    def remove_user(
                self, 
                user_principal_name: str = '', 
                workspace_id: str = '',
                dataset_id: str = '',
                user_type: str = 'User') -> Dict:
        """
        Removes an user access to a specific dataset.

        Args:
            user_principal_name (str): user e-mail or identifier of service principal.
            workspace_id (str): workspace id to add the user to.
            dataset_id (str): dataset id to grant access to.
            access_right (str, optional): access right type. Defaults to 'Member'.
            user_type (str, optional): user type, 'SP' for service accounts. Defaults to 'user'.

        Returns:
            Dict: status message.
        """

        # If both, user, workspace and dataset are provided...
        if (user_principal_name != '') & (workspace_id != '') & (dataset_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/datasets/{dataset_id}/users'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Add user to dataset with the specified access right.
            # https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/post-dataset-user-in-group
            data = {
                "identifier": user_principal_name,
                "principalType": user_type,
                "datasetUserAccessRight": "None"
            }

            # Make the request
            r = requests.put(url=request_url, headers=headers, json=data)

            # Get HTTP status and content
            status = r.status_code

            # If success...
            if status == 200:
                return {'message': 'Success'}
            
            # Too many requests
            elif status == 429:
                return {'message': {'error': {'status': 429, 'description': 'too many requests'}, 'content': ''}}
            
            # Cannot change admin access
            elif status == 401:
                return {'message': {'error': {'status': 401, 'description': 'not authorized'}, 'content': ''}}
            else:                
                # If any error happens, return message.
                response = json.loads(r.content)
                error_message = response['error']['code']
                return {'message': {'error': {'status': status, 'description': error_message}, 'content': ''}}                    

        else:
            return {'message': 'Missing parameters, please check.'}
