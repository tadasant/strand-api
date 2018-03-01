class DialoguesMutationGenerator:
    @staticmethod
    def create_message(text, discussion_id, author_id, time):
        mutation = f'''
          mutation {{
            createMessage(input: {{text: "{text}", discussionId: {discussion_id},
                                   authorId: {author_id}, time: "{time}"}}) {{
              message {{
                text
                discussion {{
                  status
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_reply(text, message_id, author_id, time):
        mutation = f'''
          mutation {{
            createReply(input: {{text: "{text}", messageId: {message_id},
                                 authorId: {author_id}, time: "{time}"}}) {{
              reply {{
                text
                message {{
                  discussion {{
                    status
                  }}
                }}
              }}
            }}
          }}
        '''
        return mutation


class GroupsMutationGenerator:
    @staticmethod
    def create_group(group_name):
        mutation = f'''
              mutation {{
                createGroup(input: {{name: "{group_name}"}}) {{
                  group {{
                    name
                  }}
                }}
              }}
            '''
        return mutation


class SlackIntegrationMutationGenerator:
    @staticmethod
    def attempt_slack_installation(code, client_id, redirect_uri):
        mutation = f'''
          mutation {{
            attemptSlackInstallation(input: {{code: "{code}",
                                              clientId: "{client_id}",
                                              redirectUri: "{redirect_uri}"}}) {{
              slackTeam {{
                name
              }}
            }}
          }}        
        '''
        return mutation

    @staticmethod
    def close_discussion_from_slack(slack_channel_id, slack_user_id):
        mutation = f'''
          mutation {{
            closeDiscussionFromSlack(input: {{slackChannelId: "{slack_channel_id}",
                                              slackUserId: "{slack_user_id}"}}) {{
              discussion {{
                id
                status
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_discussion_from_slack(time_start, topic_id, id, name, slack_team_id):
        mutation = f'''
          mutation {{
            createDiscussionFromSlack(input: {{discussion: {{timeStart: "{time_start}",
                                                             topicId: {topic_id}}},
                                               id: "{id}",
                                               name: "{name}",
                                               slackTeamId: "{slack_team_id}"}}) {{
              discussion {{
                id
                topic {{
                  id
                }}
              }}
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_message_from_slack(text, slack_channel_id, slack_user_id, origin_slack_event_ts):
        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{text}", slackChannelId: "{slack_channel_id}",
                                            slackUserId: "{slack_user_id}",
                                            originSlackEventTs: "{origin_slack_event_ts}"}}) {{
              message {{
                author {{
                  id
                }}
                discussion {{
                  id
                  participants {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_reply_from_slack(text, message_origin_slack_event_ts, slack_channel_id, slack_user_id,
                                origin_slack_event_ts):
        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{text}",
                                          messageOriginSlackEventTs: "{message_origin_slack_event_ts}",
                                          slackChannelId: "{slack_channel_id}",
                                          slackUserId: "{slack_user_id}",
                                          originSlackEventTs: "{origin_slack_event_ts}"}}) {{
              reply {{
                time
                message {{
                  author {{
                    id
                  }}
                  discussion {{
                    participants {{
                      id
                    }}
                  }}
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_slack_channel(id, name, slack_team_id, discussion_id):
        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{id}", name: "{name}", slackTeamId: "{slack_team_id}",
                                        discussionId: {discussion_id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_slack_user(id, name, real_name, display_name, image_72, is_bot, is_admin,
                          slack_team_id, user_id):
        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{id}", name: "{name}", realName: "{real_name}", displayName: "{display_name}",
                                     image72: "{image_72}", isBot: {is_bot}, isAdmin: {is_admin},
                                     slackTeamId: "{slack_team_id}", userId: {user_id}}}) {{
              slackUser {{
                id
              }}
            }}
          }}
        '''
        return mutation


class MutationGenerator(DialoguesMutationGenerator,
                        GroupsMutationGenerator,
                        SlackIntegrationMutationGenerator):
    pass
