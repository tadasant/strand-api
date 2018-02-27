import pytest


class TestMarkDiscussionAsPendingClosedFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosed(input: {{id: "{discussion.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosed(input: {{id: "{discussion.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_discussion_state(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='OPEN')

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosed(input: {{id: "{discussion.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'OPEN' using method " \
                                                          "'mark_as_pending_closed'"

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory, auto_close_pending_closed_discussion_factory,
                   slack_app_request_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosed(input: {{id: "{discussion.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack']['discussion'][
                   'status'] == 'PENDING CLOSED'
