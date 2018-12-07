from . import OAuthSignIn


class OutlookSignIn(OAuthSignIn):
    def __init__(self):
        super(OutlookSignIn, self).__init__('outlook')
        self.service = OAuth2Service(
            'microsoft',
        	consumer_key='Register your app at apps.dev.microsoft.com',
        	consumer_secret='Register your app at apps.dev.microsoft.com',
        	request_token_params={'scope': 'offline_access User.Read'},
        	base_url='https://graph.microsoft.com/v1.0/',
        	request_token_url=None,
        	access_token_method='POST',
        	access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
        	authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],  # Facebook does not provide
                                            # username, so the email's user
                                            # is used instead
            me.get('email')
        )
