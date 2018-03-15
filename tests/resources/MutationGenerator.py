import json


class TeamsMutationGenerator:
    @staticmethod
    def create_team(team_name):
        mutation = f'''
          mutation {{
            createTeam(input: {{name: "{team_name}"}}) {{
              team {{
                name
              }}
            }}
          }}
        '''
        return mutation

    @staticmethod
    def add_members_to_team(id, member_ids):
        mutation = f'''
          mutation {{
            addMembersToTeam(input: {{id: {id}, memberIds: {[member_id for member_id in member_ids]}}}) {{
              team {{
                name
                members {{
                  email
                }}
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

    @staticmethod
    def create_user_with_teams(email, username, team_ids):
        mutation = f'''
          mutation {{
            createUserWithTeams(input: {{email: "{email}", username: "{username}",
                                         teamIds: {[team_id for team_id in team_ids]}}}) {{
              user {{
                email
                teams {{
                  name
                }}
              }}
            }}
          }}
        '''
        return mutation


class StrandsMutationGenerator:
    @staticmethod
    def create_strand(title, body, timestamp, saver_id, owner_id, tags=''):
        mutation = f'''
          mutation {{
            createStrand(input: {{{'title: "%s",' % title if title else ''}
                                  body: "{body}",
                                  timestamp: "{timestamp}",
                                  saverId: {saver_id},
                                  ownerId: {owner_id},
                                  tags: [{','.join([f'{{name: "{tag}"}}' for tag in tags]) if tags else ''}]}}) {{
              strand {{
                title
                body
                timestamp
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
          }}
        '''
        return mutation

    @staticmethod
    def update_strand(strand_id, title='', tags=''):
        mutation = f'''
          mutation {{
            updateStrand(input: {{id: {strand_id},
                                  {'title: %s,' % json.dumps(title) if title else ''}
                                  tags: [{','.join([f'{{name: "{tag}"}}' for tag in tags]) if tags else ''}]}}) {{
              strand {{
                title
                body
                timestamp
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


class MutationGenerator(TeamsMutationGenerator, StrandsMutationGenerator, UsersMutationGenerator):
    pass
