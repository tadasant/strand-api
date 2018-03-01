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


class QueryGenerator(DialoguesQueryGenerator):
    pass
