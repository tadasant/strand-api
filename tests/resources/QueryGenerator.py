class TeamsQueryGenerator:
    @staticmethod
    def get_team(team_name):
        query = f'''
          query {{
            team(name: "{team_name}") {{
              id
            }}
          }}
        '''
        return query

    @staticmethod
    def get_teams():
        query = '''
          query {
            teams {
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
              saver {{
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
    def get_strands(query=''):
        query = f'''
          query {{
            strands(query: "{query}") {{
              title
              body
              saver {{
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
    def get_user(user_id=None, email=None):
        query = f'''
          query {{
            user({'id: %s' % user_id if user_id else 'email: "%s"' % email}) {{
              id
              email
            }}
          }}
        '''
        return query

    @staticmethod
    def get_users():
        query = '''
          query {
            users {
              id
              email
            }
          }
        '''
        return query


class QueryGenerator(TeamsQueryGenerator,
                     StrandsQueryGenerator,
                     UsersQueryGenerator):
    pass
