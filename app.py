import os
import app
import openai
import cosmoscmds
import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        output = user_input.upper()

       # response = openai.Completion.create(
       #     model="text-davinci-003",
       #     prompt=generate_prompt1(user_input),
       #     temperature=0.6,
       # )
       # output = url_for("index", result=response.choices[0].text)
       #json string data
        policy_string = '{"Action": "Deny", "operation": "Read", "classification": "Confidential", "user":"roshni@microsoft.com"}'

        #convert string to  object
        json_object = json.loads(policy_string)

        #check new data type
        print(type(json_object))

        return render_template('index.html', output=output, input=user_input, policy_object=json_object)
    return render_template('index.html')



def generate_prompt1(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


if __name__ == '__main__':
    app.run()



# Print response iteratively
#response = requests.get('<URL>')
#data = response.json()

#for key, value in data.items():
#    print(f'{key}: {value}')
