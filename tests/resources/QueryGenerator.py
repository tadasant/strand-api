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


class StrandsQueryGenerator:
    @staticmethod
    def get_strand(strand_id):
        query = f'''
          query {{
            strand(id: {strand_id}) {{
              title
              body
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
        '''
        return query

    @staticmethod
    def get_strands():
        query = '''
          query {
            strands {
              title
              body
              originalPoster {
                email
              }
              owner {
                name
              }
              tags {
                name
              }
            }
          }
        '''
        return query

    @staticmethod
    def get_tag(tag_name):
        query = f'''
          query {{
            tag(name: "{tag_name}") {{
              name
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
                     StrandsQueryGenerator,
                     UsersQueryGenerator):
    pass
