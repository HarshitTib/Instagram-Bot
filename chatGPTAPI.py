import openai

api_key = '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'
openai.api_key = api_key

def generate_quote():
    prompt = "You are a bot that generates quotes.\nUser: Generate a random text."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7
    )
    quote = response.choices[0].text.strip().split('\n')[-1]
    return quote

# quote = generate_quote()
# print(quote)
