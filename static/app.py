from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Sample date ideas based on different criteria
date_ideas = {
    "default": ["Go for a walk", "Have a picnic", "Watch a movie at home"],
    "married_with_kids": ["Family movie night", "Visit a zoo", "Cook together with kids"],
    "married_no_kids": ["Romantic dinner", "Spa day", "Weekend getaway"],
    "living_together_with_kids": ["Board game night", "Family bike ride", "Visit a museum"],
    "living_together_no_kids": ["Hiking", "Beach day", "Concert night"],
    "dating": ["Go-kart racing", "Ice skating", "Attend a cooking class"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_date_idea', methods=['POST'])
def get_date_idea():
    data = request.json
    name1 = data['name1']
    name2 = data['name2']
    duration = data['duration']
    relationship_status = data['relationship_status']
    have_kids = data['have_kids']
    
    if relationship_status == "married":
        if have_kids == "yes":
            idea = random.choice(date_ideas["married_with_kids"])
        else:
            idea = random.choice(date_ideas["married_no_kids"])
    elif relationship_status == "living_together":
        if have_kids == "yes":
            idea = random.choice(date_ideas["living_together_with_kids"])
        else:
            idea = random.choice(date_ideas["living_together_no_kids"])
    else:
        idea = random.choice(date_ideas["dating"])
    
    return jsonify({"idea": idea})

@app.route('/quick_offer', methods=['GET'])
def quick_offer():
    idea = random.choice(date_ideas["default"])
    return jsonify({"idea": idea})

if __name__ == '__main__':
    app.run(debug=True)
