import redis

history_context = ''

r = redis.Redis(host="localhost", port="6380", db=0)
for i in range(1, 11):
        try:
            history_context += (
                f"user: {r.hget(f'chat_history:461329361:{i}', 'user').decode()} \n"
                f"assistant: {r.hget(f'chat_history:461329361:{i}', 'assistant').decode()} \n"
            )
        except AttributeError:
            break

print(history_context)