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
    def create_user_and_message(email, username, first_name, last_name, groups, text, discussion_id, time):
        mutation = f'''
          mutation {{
            createUserAndMessage(input: {{user: {{email: "{email}",
                                                  username: "{username}",
                                                  firstName: "{first_name}",
                                                  lastName: "{last_name}",
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
                id
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
    def create_user_and_reply(email, username, first_name, last_name, groups, text, message_id, time):
        mutation = f'''
          mutation {{
            createUserAndReply(input: {{user: {{email: "{email}",
                                                username: "{username}",
                                                firstName: "{first_name}",
                                                lastName: "{last_name}",
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
                id
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
    def create_user_and_topic(email, username, first_name, last_name, groups,
                              title, description, is_private, group_id, tags=''):
        tags = ','.join([f'{{name: "{tag.name}"}}' for tag in tags]) if tags else tags
        mutation = f'''
          mutation {{
            createUserAndTopic(input: {{user: {{email: "{email}",
                                                username: "{username}",
                                                firstName: "{first_name}",
                                                lastName: "{last_name}",
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
                id
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
                id
              }}
            }}
          }}
        '''
        return mutation


class MutationGenerator(DialoguesMutationGenerator,
                        GroupsMutationGenerator,
                        TopicsMutationGenerator,
                        UsersMutationGenerator):
    pass
