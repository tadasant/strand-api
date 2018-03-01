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
    def create_user_and_message(email, username, first_name, last_name, avatar_url, is_bot, groups, text, discussion_id,
                                time):
        mutation = f'''
          mutation {{
            createUserAndMessage(input: {{user: {{email: "{email}",
                                                  username: "{username}",
                                                  firstName: "{first_name}",
                                                  lastName: "{last_name}",
                                                  avatarUrl: "{avatar_url}",
                                                  isBot: {is_bot},
                                                  groupIds: {[group.id for group in groups]}}},
                                          message: {{text: "{text}",
                                                     discussionId: {discussion_id},
                                                     time: "{time}"}}}}) {{
              message {{
               text
               discussion {{
                 status
               }}
              }}
              user {{
                alias
                groups {{
                  name
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

    @staticmethod
    def create_user_and_reply(email, username, first_name, last_name, avatar_url, is_bot, groups, text, message_id,
                              time):
        mutation = f'''
          mutation {{
            createUserAndReply(input: {{user: {{email: "{email}",
                                                username: "{username}",
                                                firstName: "{first_name}",
                                                lastName: "{last_name}",
                                                avatarUrl: "{avatar_url}",
                                                isBot: {is_bot},
                                                groupIds: {[group.id for group in groups]}}},
                                        reply: {{text: "{text}",
                                                 messageId: {message_id},
                                                 time: "{time}"}}}}) {{
              reply {{
               text
               message {{
                 text
               }}
              }}
              user {{
                alias
                groups {{
                  name
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

    @staticmethod
    def create_topic_from_slack(title, description, is_private, original_poster_slack_user_id,
                                tags):
        tags = ','.join([f'{{name: "{tag.name}"}}' for tag in tags])
        mutation = f'''
          mutation {{
            createTopicFromSlack(input: {{title: "{title}",
                                          description: "{description}",
                                          isPrivate: {is_private},
                                          originalPosterSlackUserId: "{original_poster_slack_user_id}",
                                          tags: [{tags}]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_user_and_message_from_slack(id, name, first_name, last_name, real_name, display_name, email,
                                           image_72, is_bot, is_admin, slack_team_id, origin_slack_event_ts,
                                           slack_channel_id, text):
        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{id}",
                                                                name: "{name}",
                                                                firstName: "{first_name}",
                                                                lastName: "{last_name}",
                                                                realName: "{real_name}",
                                                                displayName: "{display_name}",
                                                                email: "{email}",
                                                                image72: "{image_72}",
                                                                isBot: {is_bot},
                                                                isAdmin: {is_admin},
                                                                slackTeamId: "{slack_team_id}"}},
                                                    originSlackEventTs: "{origin_slack_event_ts}",
                                                    slackChannelId: "{slack_channel_id}",
                                                    text: "{text}"}}) {{
              slackUser {{
                user {{
                  alias
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_user_and_reply_from_slack(id, name, first_name, last_name, real_name, display_name, email,
                                         image_72, is_bot, is_admin, slack_team_id, message_origin_slack_event_ts,
                                         origin_slack_event_ts, slack_channel_id, text):
        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{id}",
                                                   name: "{name}",
                                                   firstName: "{first_name}",
                                                   lastName: "{last_name}",
                                                   realName: "{real_name}",
                                                   displayName: "{display_name}",
                                                   email: "{email}",
                                                   image72: "{image_72}",
                                                   isBot: {is_bot},
                                                   isAdmin: {is_admin},
                                                   slackTeamId: "{slack_team_id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{message_origin_slack_event_ts}",
                                                 originSlackEventTs: "{origin_slack_event_ts}",
                                                 slackChannelId: "{slack_channel_id}",
                                                 text: "{text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_user_and_topic_from_slack(id, name, first_name, last_name, real_name, display_name, email,
                                         image_72, is_bot, is_admin, slack_team_id, title, description,
                                         is_private, tags):
        tags = ','.join([f'{{name: "{tag.name}"}}' for tag in tags])
        mutation = f'''
          mutation {{
            createUserAndTopicFromSlack(input: {{title: "{title}",
                                                 description: "{description}",
                                                 isPrivate: {is_private},
                                                 originalPosterSlackUser: {{
                                                   id: "{id}",
                                                   name: "{name}",
                                                   firstName: "{first_name}",
                                                   lastName: "{last_name}",
                                                   realName: "{real_name}",
                                                   displayName: "{display_name}",
                                                   email: "{email}",
                                                   image72: "{image_72}",
                                                   isBot: {is_bot},
                                                   isAdmin: {is_admin},
                                                   slackTeamId: "{slack_team_id}"
                                                 }},
                                                 tags: [{tags}]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
              slackUser {{
                id
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_user_from_slack(id, name, first_name, last_name, real_name, display_name, email,
                               image_72, is_bot, is_admin, slack_team_id):
        mutation = f'''
          mutation {{
            createUserFromSlack(input: {{id: "{id}",
                                         name: "{name}",
                                         firstName: "{first_name}",
                                         lastName: "{last_name}",
                                         realName: "{real_name}",
                                         displayName: "{display_name}",
                                         email: "{email}",
                                         image72: "{image_72}",
                                         isBot: {is_bot},
                                         isAdmin: {is_admin},
                                         slackTeamId: "{slack_team_id}"}}) {{
              slackUser {{
                user {{
                  id
                  alias
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def mark_discussion_as_pending_closed_from_slack(slack_channel_id):
        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel_id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def update_slack_agent_topic_channel_and_activate(slack_team_id, topic_channel_id):
        mutation = f'''
          mutation {{
            updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team_id}",
                                                            topicChannelId: "{topic_channel_id}"}}) {{
              slackAgent {{
                topicChannelId
                status
              }}
            }}
          }}
        '''
        return mutation


class TopicsMutationGenerator:
    @staticmethod
    def close_discussion(discussion_id):
        mutation = f'''
          mutation {{
            closeDiscussion(input: {{id: {discussion_id}}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_discussion(time_start, time_end, topic_id):
        mutation = f'''
          mutation {{
            createDiscussion(input: {{timeStart: "{time_start}", timeEnd: "{time_end}",
                                      topicId: {topic_id}}}) {{
              discussion {{
                topic {{
                  id
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_tag(name):
        mutation = f'''
          mutation {{
            createTag(input: {{name: "{name}"}}) {{
              tag {{
                name
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_topic(title, description, is_private, original_poster_id, group_id, tags=''):
        tags = ','.join([f'{{name: "{tag.name}"}}' for tag in tags]) if tags else tags
        mutation = f'''
          mutation {{
            createTopic(input: {{title: "{title}",
                                 description: "{description}",
                                 isPrivate: {is_private},
                                 originalPosterId: {original_poster_id},
                                 groupId: {group_id},
                                 tags: [{tags}]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def create_user_and_topic(email, username, first_name, last_name, avatar_url, is_bot, groups,
                              title, description, is_private, group_id, tags=''):
        tags = ','.join([f'{{name: "{tag.name}"}}' for tag in tags]) if tags else tags
        mutation = f'''
          mutation {{
            createUserAndTopic(input: {{user: {{email: "{email}",
                                                username: "{username}",
                                                firstName: "{first_name}",
                                                lastName: "{last_name}",
                                                avatarUrl: "{avatar_url}",
                                                isBot: {is_bot},
                                                groupIds: {[group.id for group in groups]}}},
                                        topic: {{title: "{title}",
                                                 description: "{description}",
                                                 isPrivate: {is_private},
                                                 groupId: {group_id},
                                                 tags: [{tags}]}}}}) {{
              topic {{
               title
               tags {{
                 name
               }}
              }}
              user {{
                alias
                groups {{
                  name
                }}
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def mark_discussion_as_pending_closed(discussion_id):
        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosed(input: {{id: {discussion_id}}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        return mutation


class UsersMutationGenerator:
    @staticmethod
    def create_user(email, username):
        mutation = f'''
          mutation {{
            createUser(input: {{email: "{email}", username: "{username}"}}) {{
              user {{
                alias
              }}
            }}
          }}
        '''
        return mutation


class MutationGenerator(DialoguesMutationGenerator,
                        GroupsMutationGenerator,
                        SlackIntegrationMutationGenerator,
                        TopicsMutationGenerator,
                        UsersMutationGenerator):
    pass
