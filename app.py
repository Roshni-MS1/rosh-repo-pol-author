import os
import app
import openai
import cosmoscmds
import json
import ast
from flask import Flask, redirect, render_template, request, url_for
from purreaddocs import readopenaikey

app = Flask(__name__)
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = readopenaikey()


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt = []
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        user_input_next = request.form.get( 'user_input_next')
        user_input_his = request.form.get( 'user_input_his')
        print (request.form.get('submit'))
        
        if 'policyinput' in request.form:
            print ("policy create")
        elif 'Update' in request.form:
            print ("policy update")
            pass
        elif 'Approve' in request.form:
            output= request.form.get('outputfinal')
            print ("policy approve = ",output)
            return render_template('index.html', finalpolicy=output)
        else:
            print ("clear page")
            return render_template('index.html')
            

        print ("us=", user_input)
        print ("us1=",user_input_next)
        print ("us1=",user_input_his)
        
        if user_input_next != None : 
            prompt = ast.literal_eval(user_input_his)  
            prompt.append({"role": "user", "content": user_input_next})
        else:
            prompt.append({"role": "user", "content": user_input})
            
        user_input_his = prompt
        print ("prompt=", prompt)

       # response = openai.Completion.create(
       #     model="text-davinci-003",
       #     prompt=generate_prompt1(user_input),
       #     temperature=0.6,
       # )
       # output = url_for("index", result=response.choices[0].text)
       #json string data

        response = openai.ChatCompletion.create(
        #    model="text-davinci-003",
            model="text-ada-001",
            messages=prompt,
            temperature=0.6,
        )
        print(['choices'][0]['message']['content'])
        policy_string = '{"Action": "Deny", "operation": "Read", "classification": "Confidential", "user":"roshni@microsoft.com"}'

        #convert string to  object
        json_object = json.loads(policy_string)

        #check new data type
        print(prompt)
        input=listToString(prompt)
        output = prompt
        return render_template('index.html', output=output, input=input, input_his=user_input_his, policy_object=json_object)
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


def update_prompt_chat(role, content, prompt):
    prompt.append({"role": role, "content": content})
    return prompt
   
def listToString(list):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in list:
        str1 += ele['content'] + "\n"

    # return string
    return str1


if __name__ == '__main__':
    app.run()



# Print response iteratively
#response = requests.get('<URL>')
#data = response.json()

#for key, value in data.items():
#    print(f'{key}: {value}')
