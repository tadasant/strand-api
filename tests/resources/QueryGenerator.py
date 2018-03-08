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


class UsersQueryGenerator:
    @staticmethod
    def get_user(user_id):
        query = f'''
          query {{
            user(id: {user_id}) {{
              id
            }}
          }}
        '''
        return query

    @staticmethod
    def get_user_authorized(user_id):
        query = f'''
          query {{
            user(id: {user_id}) {{
              email
            }}
          }}
        '''
        return query

    @staticmethod
    def get_users_authorized():
        query = '''
          query {
            users {
              email
            }
          }
        '''
        return query


class QueryGenerator(GroupsQueryGenerator,
                     UsersQueryGenerator):
    pass
