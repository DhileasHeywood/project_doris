""" Test session login and logout """

import pytest
from flask import url_for, session


def test_login(client, app):
    """ Check we can set a user correctly in the session """

    with app.test_request_context():
        with client:
            # GET should be supported
            assert client.get(url_for('auth.login')).status_code == 200

            # POST should set our user
            assert session.get("username") is None

            response = client.post(url_for('auth.login'), data={'username': 'doris'})
            assert response.status_code == 302  # Found - redirect to the main app
            assert response.location == url_for('application.index', _external=True)

            assert session['username'] == 'doris'


def test_logout(client, app):
    """ Ensure that logging out unsets the session """

    with app.test_request_context():
        with client:
            _ = client.post(url_for('auth.login'), data={'username': 'horatio'})

            assert session['username'] == 'horatio'

            response = client.get(url_for('auth.logout'))
            assert response.status_code == 302  # Found - redirect to the app index
            assert response.location == url_for('application.index', _external=True)

            with pytest.raises(KeyError):
                _ = session['username']
