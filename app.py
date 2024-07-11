from flask import Flask, request, jsonify, render_template
import random
import requests

app = Flask(__name__)

# Replace 'YOUR_GOOGLE_API_KEY' with your actual Google API Key
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'

# Sample date ideas based on different criteria
date_ideas = {
    "default": [
        "Go for a walk",
        "Have a picnic",
        "Watch a movie at home",
        "Attend a local farmers' market",
        "Have a themed dinner night (e.g., Italian, Mexican)",
        "Visit an art gallery or museum",
        "Go stargazing",
        "Take a dance class together"
    ],
    "married_with_kids": [
        "Family movie night",
        "Visit a zoo",
        "Cook together with kids",
        "Backyard camping with a bonfire and s'mores",
        "Family talent show night",
        "DIY arts and crafts session",
        "Visit an amusement park",
        "Plan a scavenger hunt"
    ],
    "married_no_kids": [
        "Romantic dinner",
        "Spa day",
        "Weekend getaway",
        "Wine tasting tour",
        "Hot air balloon ride",
        "Take a pottery or painting class",
        "Visit a botanical garden",
        "Book a couples' massage"
    ],
    "living_together_with_kids": [
        "Board game night",
        "Family bike ride",
        "Visit a museum",
        "Family baking day with themed treats",
        "Explore a nearby nature reserve",
        "Attend a family-friendly concert or theater show",
        "Have a science experiment day",
        "Go fruit picking at a local farm"
    ],
    "living_together_no_kids": [
        "Hiking",
        "Beach day",
        "Concert night",
        "Go on a road trip to a nearby town",
        "Take a sailing or boat trip",
        "Visit an escape room",
        "Attend a wine and paint night",
        "Plan a surprise date where each partner takes turns planning"
    ],
    "dating": [
        "Go-kart racing",
        "Ice skating",
        "Attend a cooking class",
        "Visit a trampoline park",
        "Take a day trip to explore a new city",
        "Attend a comedy show",
        "Try an escape room challenge",
        "Go horseback riding"
    ]
}


def get_place_recommendations(location, keyword):
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}+in+{location}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    places = response.json()['results'][:5]
    recommendations = []
    for place in places:
        recommendations.append({
            'name': place['name'],
            'address': place['formatted_address'],
            'map_url': f"https://www.google.com/maps/search/?api=1&query={place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
        })
    return recommendations

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
    location = data['location']
    
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
    
    recommendations = get_place_recommendations(location, idea)

    return jsonify({"idea": idea, "recommendations": recommendations})

@app.route('/quick_idea', methods=['GET'])
def quick_idea():
    idea = random.choice(date_ideas["default"])
    return jsonify({"idea": idea})

if __name__ == '__main__':
    app.run(debug=True)
