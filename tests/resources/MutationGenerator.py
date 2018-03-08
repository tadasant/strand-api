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


class MutationGenerator(GroupsMutationGenerator,
                        UsersMutationGenerator):
    pass
