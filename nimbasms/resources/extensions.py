"""Extension service."""

from nimbasms.resources.base import BaseRest


class Extensions(BaseRest):
    """
    Manage Extension service, including actions and pricing plans.
    """
    def __init__(self, client):
        """
        Initialize Extensions
        """
        super().__init__(client, 'extensions')

    def create(self, name, category, description, base_api_url, auth_type,
               is_paid, documentation_url=None, website_url=None,
               oauth2_config=None):
        """
        Create an extension

        :param str name: Extension name
        :param str category: Extension category
        :param str description: Extension description
        :param str base_api_url: Base URL of the extension API
        :param str auth_type: Authentication: none, api_key or oauth2
        :param bool is_paid: Whether the extension is paid
        :param str documentation_url: Documentation URL, optional
        :param str website_url: Website URL, optional
        :param dict oauth2_config: OAuth2 configuration, optional
        """
        return self.request(method='POST', data=self.payload(
            name=name,
            category=category,
            description=description,
            base_api_url=base_api_url,
            auth_type=auth_type,
            is_paid=is_paid,
            documentation_url=documentation_url,
            website_url=website_url,
            oauth2_config=oauth2_config,
        ))

    def get(self, extensionid):
        """
        Retrieve an extension

        :param str extensionid: Extension identifier
        """
        return self.request(
            method='GET',
            uri=f'{self.resource_url}/{extensionid}',
        )

    def update(self, extensionid, **fields):
        """
        Partially update an extension

        :param str extensionid: Extension identifier
        :param fields: Extension fields to update
        """
        return self.request(
            method='PATCH',
            uri=f'{self.resource_url}/{extensionid}',
            data=self.payload(**fields),
        )

    def publish(self, extensionid, is_published=True):
        """
        Publish or unpublish an extension

        :param str extensionid: Extension identifier
        :param bool is_published: Whether the extension should be published
        """
        return self.request(
            method='POST',
            uri=f'{self.resource_url}/{extensionid}/publish',
            data={'is_published': is_published},
        )

    def list_actions(self, extensionid, limit=20, offset=0):
        """
        List the actions of an extension

        :param str extensionid: Extension identifier
        :param int limit: Limit actions request
        :param int offset: Offset to begin request
        """
        return self.list_url(
            f'{self.resource_url}/{extensionid}/actions',
            self.pagination(limit, offset),
        )

    def create_action(self, extensionid, name, method, endpoint, description,
                      required_params=None, optional_params=None,
                      response_format=None):
        """
        Create an action for an extension

        :param str extensionid: Extension identifier
        :param str name: Action name
        :param str method: HTTP method of the action
        :param str endpoint: Action endpoint
        :param str description: Action description
        :param dict required_params: Required parameters, optional
        :param dict optional_params: Optional parameters, optional
        :param dict response_format: Response format, optional
        """
        return self.request(
            method='POST',
            uri=f'{self.resource_url}/{extensionid}/actions',
            data=self.payload(
                name=name,
                method=method,
                endpoint=endpoint,
                description=description,
                required_params=required_params,
                optional_params=optional_params,
                response_format=response_format,
            ),
        )

    def get_action(self, extensionid, actionid):
        """
        Retrieve an action of an extension

        :param str extensionid: Extension identifier
        :param str actionid: Action identifier
        """
        return self.request(
            method='GET',
            uri=f'{self.resource_url}/{extensionid}/actions/{actionid}',
        )

    def update_action(self, extensionid, actionid, **fields):
        """
        Partially update an action of an extension

        :param str extensionid: Extension identifier
        :param str actionid: Action identifier
        :param fields: Action fields to update
        """
        return self.request(
            method='PATCH',
            uri=f'{self.resource_url}/{extensionid}/actions/{actionid}',
            data=self.payload(**fields),
        )

    def delete_action(self, extensionid, actionid):
        """
        Delete an action of an extension

        :param str extensionid: Extension identifier
        :param str actionid: Action identifier
        """
        return self.request(
            method='DELETE',
            uri=f'{self.resource_url}/{extensionid}/actions/{actionid}',
        )

    def publish_action(self, extensionid, actionid, is_published=True):
        """
        Publish or unpublish an action of an extension

        :param str extensionid: Extension identifier
        :param str actionid: Action identifier
        :param bool is_published: Whether the action should be published
        """
        return self.request(
            method='POST',
            uri=f'{self.resource_url}/{extensionid}/actions/{actionid}/publish',
            data={'is_published': is_published},
        )

    def create_pricing_plan(self, extensionid, name, price, billing_period,
                            features):
        """
        Create a pricing plan for an extension

        :param str extensionid: Extension identifier
        :param str name: Pricing plan name
        :param str price: Price in GNF, without the currency
        :param str billing_period: Billing period: monthly or yearly
        :param dict features: Features of the pricing plan
        """
        return self.request(
            method='POST',
            uri=f'{self.resource_url}/{extensionid}/pricing-plans',
            data=self.payload(
                name=name,
                price=price,
                billing_period=billing_period,
                features=features,
            ),
        )

    def update_pricing_plan(self, extensionid, pricingplanid, **fields):
        """
        Partially update a pricing plan of an extension

        :param str extensionid: Extension identifier
        :param str pricingplanid: Pricing plan identifier
        :param fields: Pricing plan fields to update
        """
        return self.request(
            method='PATCH',
            uri=f'{self.resource_url}/{extensionid}/pricing-plans/{pricingplanid}',
            data=self.payload(**fields),
        )

    def delete_pricing_plan(self, extensionid, pricingplanid):
        """
        Delete a pricing plan of an extension

        :param str extensionid: Extension identifier
        :param str pricingplanid: Pricing plan identifier
        """
        return self.request(
            method='DELETE',
            uri=f'{self.resource_url}/{extensionid}/pricing-plans/{pricingplanid}',
        )

    def upload_logo(self, extensionid, logo):
        """
        Upload the logo of an extension

        :param str extensionid: Extension identifier
        :param str logo: Path to a square PNG or JPEG image
        """
        with open(logo, 'rb') as handle:
            return self.request(
                method='PATCH',
                uri=f'{self.resource_url}/{extensionid}/logo',
                files={'logo': handle},
            )
