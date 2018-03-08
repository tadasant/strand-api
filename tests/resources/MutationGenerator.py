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


class StrandsMutationGenerator:
    @staticmethod
    def create_strand(title, body, timestamp, original_poster_id, owner_id, tags=''):
        mutation = f'''
          mutation {{
            createStrand(input: {{title: "{title}",
                                  body: "{body}",
                                  timestamp: "{timestamp}",
                                  originalPosterId: {original_poster_id},
                                  ownerId: {owner_id},
                                  tags: [{','.join([f'{{name: "{tag}"}}' for tag in tags]) if tags else ''}]}}) {{
              strand {{
                title
                body
                timestamp
                originalPoster {{
                  email
                }}
                owner {{
                  name
                }}
                tags {{
                  name
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


class MutationGenerator(GroupsMutationGenerator, StrandsMutationGenerator, UsersMutationGenerator):
    pass
