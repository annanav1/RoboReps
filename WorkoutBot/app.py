from flask import Flask, render_template, request,jsonify
import openai
#from openai.error import OpenAIError
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

# Setup logger
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route('/',methods=['GET'])
def frontend():
    return render_template('index.html')

@app.route('/workout_plan_frontend', methods=['POST', 'GET'])
def workout_plan__frontend():
    return render_template('workout_plan_frontend.html')

@app.route('/explain_concept_frontend', methods=['POST', 'GET'])
def explain_concept_frontend():
    return render_template('nutrition_advice_frontend.html')

@app.route('/workout_frontend', methods=['POST', 'GET'])
def workout_frontend():
    return render_template('workout_frontend.html')

    

@app.route('/workout_plan_creator',methods=['POST','GET'])
def workout_plan_creator():
    # print(request.form)
    goal = request.form.get('goal')
    age = request.form.get('age')
    days_perWeek = request.form.get('days')
    duration = request.form.get('timeCommit')
    experiene = request.form.get('experience')
    project_type = request.form.get('project_type')
    reference_preference = request.form.get('reference_preference')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on workout plan creator: {time}')
    logger.info(f'Goal: {goal}')
    logger.info(f'Project Type: {project_type}')
    logger.info(f'Reference Preference: {reference_preference}')


    experts = {
        'Full Body': 'Professional Trainer',
        'Upper Body': 'Professional Trainer'
    }

    expert = experts.get(project_type,'Professional Trainer')

    # expert = experts[project_type]
    system_prompt =f'''
    Act as an expert {expert}. You specialize in customized training and create workout plans to help people reach their fitness goals.
    You will be provided with the goal of the trainee, their age, time commitment, experience level, and workout preference.
    You will create a four week workout plan that provides clear instructions of each exercise including a detailed description of each exercises, technique tips, and the amount of reps and sets.
    You will not include any rest days, and you will ensure that the workouts are clear and descriptive.
    Every workout should include a detailed description and links to helpful resource videos. 
    Organize the information with each week bolded, and format with spacing inbetween each workout, and include bulleted list for exercises. 
    Write workout plan organized as a scheduled time line and add a seperate line \n\n---\n\n to seperate weeks.
    Be sure to only include relevant information because time is limited. 
    
    Desired format:
    Week: <Bold>
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-         
    ##
    Week: <Bold>
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
    ##
    Week: <Bold>
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
    ##
    Week: <Bold>
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
        Day: -||-
            Excercise: -||-
                Instructions: -||-
            Excercise: -||-
                Instructions: -||-
    

    '''

    query = f'''
    My goal is {goal}. I am {age} years old and have {experiene} experience.
    I can comitt to this routine for {days_perWeek} day per week for {duration} minitues per session.
    I will be using {reference_preference} during my workout and want to fucus my plan on {project_type}.
    Make a workout a month long workout plan with descriptions of excercises and resources.
    '''

    print(system_prompt, query)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query
                
            }],
            max_tokens=2000,
            temperature=0.1
        )
    except Exception as e:
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":e})
    
    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on workout plan creator: {time}')

    return jsonify({"response":response.choices[0].message.content})
    



@app.route('/explain_concept',methods=['POST','GET'])
def explain_concept():
    macro_goal = request.form.get('concept_name')
    dietary_restrictions = request.form.get('dietary_restrictions')
    meal_type = request.form.get('mealType')
    meal_location = request.form.get('mealLoc')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on explain concept: {time}')
    logger.info(f'Concept Name: {macro_goal}')

    system_prompt ='''
    Act as an expert nutritionist or personal chef. You will be provided a prompt related to healthy food ideas.
    You will provide healthy recipies with detailed instructions and resource links.
    Provide only suggestions that adhear to dietary requriements, and macros goals.
    Provide suggestions based on the type of meal either breakfast,lunch,dinner,snack,or dessert.
    Provide links to the recipies provided and one to two other options.
    '''

    query = f'''Generate a meal focused around {macro_goal}, and the recipe is required to adhear to {dietary_restrictions}.
      I want to enjoy this meal for {meal_type} and I will be {meal_location} it. Provide only suggestions that meet all needs.'''

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query

            }],
            max_tokens=2000,
            temperature=0.1
        )
    except Exception as e:
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":e})
    
    
    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on explain concept: {time}')

    return jsonify({"response":response.choices[0].message.content})






@app.route('/workout',methods=['POST','GET'])
def workout():
    goal = request.form.get('goal')
    project_type = request.form.get('build_project_type')
    time_constraint = request.form.get('timeCommit')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on build project: {time}')
    logger.info(f'Goal: {goal}')
    logger.info(f'Project Type: {project_type}')
    logger.info(f'Time Constraint: {time_constraint}')

      #Define the dictionary
    experts = {
        'Full Body Workouts': 'Professional Trainer',
        'Ab Focus': 'Professional Trainer',
        'Booty Builder': 'Professional Trainer',
        'Upper Body': 'Professional Trainer',
        'Cardio': 'Professional Trainer',
        'HIIT Sessions': 'Professional Trainer',
        'Stretch': 'Yoga Instructure',
        'Pilates':'Pilates Instructure'
        }
   

    expert = experts.get(project_type, 'Professional Trainer')

    system_prompt =f'''
    Act as an expert {expert}. User will provide be provided a targeted goals, duration required, and type of workout they want to complete. 
    Create a complete workout that is focused on the specific targeted goals or area and include a detailed description of each exercises.
    Provide the number of sets and reps for each exercise and links of videos that will be useful resources.
    Provide the useful tips related to the targeted fitness goals.
    '''

    query = f'''
    {goal} is my targeted goals. I have {time_constraint} to workout and want a {project_type} type of workout. 
    Provide tips and resources and detailed instructions.
    '''

    print(system_prompt, query)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            # model= 'gpt-4',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query

            }],
            max_tokens=2000,
            temperature=0.1
        )

    except Exception as e: 
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":str(e)}),500
    

    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on build project : {time}')

    return jsonify({"response":response.choices[0].message.content})



    



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)