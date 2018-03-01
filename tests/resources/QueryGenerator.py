class DialoguesQueryGenerator:
    @staticmethod
    def get_message(message_id):
        query = f'''
          query {{
            message(id: {message_id}) {{
              text
            }}
          }}
        '''
        return query

    @staticmethod
    def get_messages():
        query = '''
          query {
            messages {
              text
            }
          }
        '''
        return query

    @staticmethod
    def get_reply(reply_id):
        query = f'''
          query {{
            reply(id: {reply_id}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        return query

    @staticmethod
    def get_replies():
        query = '''
          query {
            replies {
              text
            }
          }
        '''
        return query


class GroupsQueryGenerator:
    @staticmethod
    def get_group(group_name):
        query = f'''
          query {{
            group(name: "{group_name}") {{
              id
            }}
          }}
        '''
        return query

    @staticmethod
    def get_groups():
        query = '''
          query {
            groups {
              name
            }
          }
        '''
        return query


class SlackIntegrationQueryGenerator:
    @staticmethod
    def get_slack_application_installation(slack_application_installation_id):
        query = f'''
          query {{
            slackApplicationInstallation(id: {slack_application_installation_id}) {{
              botAccessToken
            }}
          }}
        '''
        return query

    @staticmethod
    def get_slack_application_installations():
        query = '''
          query {
            slackApplicationInstallations {
              botAccessToken
            }
          }
        '''
        return query

    @staticmethod
    def get_active_slack_application_installations():
        query = '''
          query {
            slackApplicationInstallations (agentStatus: "ACTIVE") {
              botAccessToken
            }
          }
        '''
        return query

    @staticmethod
    def get_slack_channel(slack_channel_id):
        query = f'''
          query {{
            slackChannel(id: "{slack_channel_id}") {{
              name
            }}
          }}
        '''
        return query

    @staticmethod
    def get_slack_channels():
        query = '''
          query {
            slackChannels {
              name
            }
          }
        '''
        return query

    @staticmethod
    def get_slack_team(slack_team_id):
        query = f'''
          query {{
            slackTeam(id: "{slack_team_id}") {{
              name
            }}
          }}
        '''
        return query

    @staticmethod
    def get_slack_teams():
        query = '''
          query {
            slackTeams {
              slackAgent {
                group {
                  name
                }
              }
            }
          }
        '''
        return query

    @staticmethod
    def get_slack_user(slack_user_id):
        query = f'''
          query {{
            slackUser(id: "{slack_user_id}") {{
              displayName
              id
            }}
          }}
        '''
        return query

    @staticmethod
    def get_slack_users():
        query = '''
          query {
            slackUsers {
              user {
                id
              }
            }
          }
        '''
        return query


class TopicsQueryGenerator:
    @staticmethod
    def get_discussion(discussion_id):
        query = f'''
          query {{
            discussion(id: {discussion_id}) {{
              status
              topic {{
                title
              }}
            }}
          }}
        '''
        return query

    @staticmethod
    def get_discussions():
        query = '''
          query {
            discussions {
              id
            }
          }
        '''
        return query

    @staticmethod
    def get_tag(tag_name):
        query = f'''
          query {{
            tag(name: "{tag_name}") {{
              id
            }}
          }}
        '''
        return query

    @staticmethod
    def get_tags():
        query = '''
          query {
            tags {
              name
            }
          }
        '''
        return query

    @staticmethod
    def get_topic(topic_id):
        query = f'''
          query {{
            topic(id: {topic_id}) {{
              title
            }}
          }}
        '''
        return query

    @staticmethod
    def get_topics():
        query = '''
          query {
            topics {
              title
            }
          }
        '''
        return query


class UsersQueryGenerator:
    @staticmethod
    def get_user(user_id):
        query = f'''
          query {{
            user(id: {user_id}) {{
              alias
            }}
          }}
        '''
        return query

    @staticmethod
    def get_user_authorized(user_id):
        query = f'''
          query {{
            user(id: {user_id}) {{
              slackUsers {{
                id
              }}
            }}
          }}
        '''
        return query

    @staticmethod
    def get_users_authorized():
        query = '''
          query {
            users {
              slackUsers {
                id
              }
            }
          }
        '''
        return query


class QueryGenerator(DialoguesQueryGenerator,
                     GroupsQueryGenerator,
                     SlackIntegrationQueryGenerator,
                     TopicsQueryGenerator,
                     UsersQueryGenerator):
    pass
