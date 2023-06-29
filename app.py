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
            pass
        elif 'Update' in request.form:
            print ("policy update")
            pass
        elif 'Approve' in request.form:
            output= request.form.get('outputfinal')
            #print ("policy approve = ",output)
            return render_template('index.html', finalpolicy=output)
        else:
            #print ("clear page")
            return render_template('index.html')
            

        print ("us=", user_input)
        #print ("us1=",user_input_next)
        #print ("us2=",user_input_his)
        
        if user_input_next != None : 
            #add chat history 
            prompt = ast.literal_eval(user_input_his)  
            #request updates to policy suggestion
            prompt.append({"role": "user", "content": user_input_next})
        else:
            #First Prompt Creation
            userprompt = generate_first_prompt(user_input)
            prompt.append({"role": "user", "content": userprompt})
            
        user_input_his = prompt
        #print ("prompt=", prompt)
        output = prompt
       # response = openai.Completion.create(
       #     model="text-davinci-003",
       #     prompt=generate_prompt1(user_input),
       #     temperature=0.6,
       # )
       # output = url_for("index", result=response.choices[0].text)
       #json string data

        response = openai.ChatCompletion.create(
        #    model="text-davinci-003",
        #    model="text-ada-001",
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.6,
        )

        if 'choices' in response:
            if len(response['choices']) > 0:
                output = response.choices[0]["message"]["content"]
                print("ChatGPT output=", output)
            else:
                print("response len 0")
        else:
            print("Opps sorry, you beat the AI this time")

        #output = '{"Action" : "Allow", "method" : "included", "users" : "Marketing Department", "Label" : "Location"}'
        #policy_json_object = json.loads(output)
        
        #policystr = genpolicyfromjson(output)
        #convert string to  object
        input=listToString(prompt)
        print (user_input)
        return render_template('index.html', output=output, policy_json_hidden=output, input=user_input, input_his=user_input_his)
    return render_template('index.html')


def genpolicyfromjson(output):
    
    strpolicy = "" 
    policy_json_object = json.loads(output)

    if policy_json_object["method"] == "included":
        if policy_json_object["Action"] == "Allow":
            strpolicy = "Allow "   
        elif policy_json_object["Action"] == "Deny":
            strpolicy = "Deny "
        else:
            print ("Invalid Action")
            return ""
        strpolicy = strpolicy + policy_json_object["users"] + " access to " + policy_json_object["Label"] + " data."
        strpolicy = strpolicy +"\n\nJSON:\n" +   output
        return strpolicy
    elif policy_json_object["method"] == "excluded": 
        if policy_json_object["Action"] == "Allow":
            strpolicy = "Allow "    
        elif policy_json_object["Action"] == "Deny":
            strpolicy = "Deny "
        else:
            print ("Invalid Action")
            return ""
        strpolicy = strpolicy + policy_json_object["users"] + " access to all data except " + policy_json_object["Label"] + " data."           
        strpolicy = strpolicy +"\n\nJSON:\n" +   output
        return strpolicy    
    else:
        print ("Invalid Method")
        return ""   
    



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


def generate_first_prompt(usernlpolicy):
    str1 = ""
    return f"""Create JSON from the text

Text 1: Only users that are FTE_Full_Time should be able to access Confidential Data 
JSON 1: {{\"Action\" :  \"Allow\", \"method\" : \"included\", \"users\" : \"FTE_Full_Time\", \"Label\" : \"Confidential\"\}} 
## 
Text 2: Users that are in Finance must be able to access Credit_Card Data 
JSON 2: {{\"Action\" : \"Allow\", \"method\" : \"included", \"users\": \"FTE_Full_Time\", \"Label\" : \"Confidential\"}} 
## 
Text 2: Users that are Full_time_employees must be able to access Credit_Card Data 
JSON 2: {{\"Action\" : \"Allow\", \"method\": \"included\", \"users\": \"Full_time_employee\", \"Label\" : \"Confidential\"}}
## 
Text 3: Everyone except Roshni must be denied access confidential data
JSON 3: {{\"Action\" : \"Deny\", \"method\" : \"excluded\", \"users\": \"Roshni\", \"Label\" : \"Confidential\"}}
## 
Text 3: Everyone except Roshni must be able to access confidential data
JSON 3: {{\"Action\" : \"Allow\", \"method\" : \"excluded\", \"users\": \"Roshni\", \"Label\" : \"Confidential\"}}
## 
Text 4: Contractors must not be able to access confidential data
JSON 4: {{\"Action\" : \"Deny\", \"method\" : \"included\", \"users\": \"Contractors\", \"Label\" : \"Confidential\"}}
## 
Text 5: Contractors must be denied access to confidential data
JSON 5: {{\"Action\" : \"Deny\", \"method\" : \"included\", \"users\": \"Contractors\", \"Label\" : \"Confidential\"}}
##
Test 6: {usernlpolicy}
JASON 6: 

## 
If the sentence includes \“able to access data\”, or \“granted access\” or \“allowed to see or process\” or something similar then Action is \“Allow\”. If the sentence includes \“not allowed to\” or \“denied\” or \“not granted\” then action is \“Deny\”. If the sentence includes \“No other user except\” or \“everyone except\” or something similar, then method is excluded. If sentence specifies All users or everyone or something similar, then method is included. Also, \“everyone\” or \“everyone except\" are not users. Users are names, users working in a department or company or organization. For the results provide only JSON data and no explanation 
"""


#def generate_prompt1(animal):
#    return f"""Suggest three names for an animal that is a superhero.
#Animal: Cat
#Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
#Animal: Dog
#Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
#Animal: {}
#Names:""".format(
#        animal.capitalize()
#    )


if __name__ == '__main__':
    app.run()



# Print response iteratively
#response = requests.get('<URL>')
#data = response.json()

#for key, value in data.items():
#    print(f'{key}: {value}')
