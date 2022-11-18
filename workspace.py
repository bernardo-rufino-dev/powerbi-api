import os
import json
import requests
import pandas as pd
from typing import Dict


class Workspace:

    def __init__(self, token: str):
        """
        Initialize variables.
        """
        self.main_url = 'https://api.powerbi.com/v1.0/myorg'
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}

        if not os.path.exists('./data'):
            os.makedirs('./data')


    def list_workspace(
                self, 
                workspace_id: str = '', 
                workspace_name: str = '', 
                filters: str = '') -> Dict:
        """
        List all workspaces that the user has access to.

        Args:
            workspace_id (str, optional): workspace id to search for.
            workspace_name (str, optional): workspace name to search for.
            filters (str, optional): filters to be applied.

        Returns:
            Dict: status message and content.
        """
        # Main URL
        request_url = self.main_url + '/groups'

        # If no parameter, list all workspaces with access to...
        if (workspace_id == '') & (workspace_name == '') & (filters == ''):
            filename = 'workspaces_all.xlsx'

        # If workspace ID was informed...
        elif workspace_id != '':
            request_url = f"{request_url}/{workspace_id}"
            filename = f'{workspace_id}.xlsx'

        # If workspace name was informed...
        elif workspace_name != '':
            request_url = f"{request_url}/?$filter=name%20eq%20'{workspace_name}'"
            filename = f"{workspace_name.replace(' ', '_').upper()}.xlsx"
        
        # If any custom (OData) filters were informed...
        # Example: passing -> filters="contains(name,'Databrew')"
        # Filters for workspaces that contain Databrew on it's name.
        elif filters != '':
            request_url = f'{request_url}/{workspace_id}/?$filter={filters}'
            filename = 'workspaces_filtered.xlsx'
        else: 
            return {'message': 'Success', 'content': response}

        # Make the request
        r = requests.get(url=request_url, headers=self.headers)

        # Get HTTP status and content
        status = r.status_code
        response = json.loads(r.content).get('value', '')

        # If success...
        if status == 200:
            # Save to Excel file
            df = pd.DataFrame(response)
            df.to_excel(f'./data/{filename}', index=False)
            
            return {'message': 'Success'}

        else:                
            # If any error happens, return message.
            response = json.loads(r.content)
            error_message = response['error']['message']

            return {'message': {'error': error_message, 'content': response}}


    def add_user(
                self, 
                user_principal_name: str = '', 
                workspace_id: str = '', 
                access_right: str = 'Member',
                user_type: str = 'user') -> Dict:
        """
        Add an user to a workspace.

        Args:
            user_principal_name (str): user e-mail or identifier of service principal.
            workspace_id (str): workspace id to add the user to.
            access_right (str, optional): access right type. Defaults to 'Member'.
            user_type (str, optional): user type, 'SP' for service accounts. Defaults to 'user'.

        Returns:
            Dict: status message.
        """

        # If both, user and workspace if are provided...
        if (user_principal_name != '') & (workspace_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/users'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Add user to workspace with the specified access right.
            # https://learn.microsoft.com/en-us/rest/api/power-bi/groups/add-group-user#groupuseraccessright

            # If service principal account
            if user_type == 'SP':
                data = {
                    "identifier": user_principal_name,
                    "groupUserAccessRight": access_right
                }

            else:

                data = {
                    "emailAddress": user_principal_name,
                    "groupUserAccessRight": access_right
                }

            # Make the request
            r = requests.post(url=request_url, headers=headers, json=data)

            # Get HTTP status and content
            status = r.status_code
            response = json.loads(r.content)

            # If success...
            if status == 200:
                return {'message': 'Success'}
            
            else:                
                # If any error happens, return message.
                error_message = response['error']['message']

                return {'message': {'error': error_message, 'content': response}}

        else:
            return {'message': 'Missing parameters, please check.'}


    def update_user(
                self, 
                user_principal_name: str = '', 
                workspace_id: str = '', 
                access_right: str = 'Member') -> Dict:
        """
        Update an user on a workspace.

        Args:
            user_principal_name (str, optional): user e-mail or identifier of service principal.
            workspace_id (str, optional): workspace id to add the user to.
            access_right (str, optional): access right type. Defaults to 'Member'.

        Returns:
            Dict: status message.
        """

        # If both, user and workspace if are provided...
        if (user_principal_name != '') & (workspace_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/users'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Add user to workspace with the specified access right.
            # https://learn.microsoft.com/en-us/rest/api/power-bi/groups/update-group-user
            data = {
                "identifier": user_principal_name,
                "groupUserAccessRight": access_right,
                "principalType": "User"
            }

            # Make the request
            r = requests.put(url=request_url, headers=headers, json=data)

            # Get HTTP status and content
            status = r.status_code
            response = json.loads(r.content)

            # If success...
            if status == 200:
                return {'message': 'Success'}
            
            else:                
                # If any error happens, return message.
                error_message = response['error']['message']

                return {'message': {'error': error_message, 'content': response}}

        else:
            return {'message': 'Missing parameters, please check.'}


    def remove_user(self, user_principal_name: str = '', workspace_id: str = '') -> Dict:
        """
        Remove an user from a workspace.

        Args:
            user_principal_name (str, optional): user e-mail or identifier of service principal.
            workspace_id (str, optional): workspace id to add the user to.

        Returns:
            Dict: status message
        """

        # If both, user and workspace if are provided...
        if (user_principal_name != '') & (workspace_id != ''):

            request_url = self.main_url + f'/groups/{workspace_id}/users/{user_principal_name}'

            headers = {'Authorization': f'Bearer {self.token}'}

            # Make the request
            r = requests.delete(url=request_url, headers=headers)

            # Get HTTP status and content
            status = r.status_code
            response = json.loads(r.content)

            # If success...
            if status == 200:
                return {'message': 'Success'}

            else:                
                # If any error happens, return message.
                error_message = response['error']['message']

                return {'message': {'error': error_message, 'content': response}}

        else:
            return {'message': 'Missing parameters, please check.'}
