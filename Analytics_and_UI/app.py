from flask import Flask, render_template, url_for, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scenario1')
def scenario1():
    #UFO Tweet references vs BTC
    return render_template('scenario1.html')

@app.route('/scenario2')
def scenario2():
    #Births and Deaths map vs UFO Tweet References
    title = "Births & Deaths vs UFO References"
    description = "Exploring the relationship between birth and death rates and UFO sightings."
    return render_template('scenario2.html', title=title, description=description)

@app.route('/scenario3')
def scenario3():
    #Mastoodon Toots Dynamic Harvestor
    return render_template('scenario3.html')

@app.route('/scenario4')
def scenario4():
    #Statewise Milk Production vs UFO Tweet References
    return render_template('scenario4.html')

@app.route('/scenario5')
def scenario5():
    #Mcdonalds Locations vs UFO References Sentiment
    return render_template('scenario5.html')

@app.route('/general')
def general():
    #The heatmap for tweets with Location information
    return render_template('general.html')

@app.route('/get_stats')
def get_stats():
    #Dynamic program for Toot Harvestor
    with open('static/stats.txt', 'r') as f:
        stats = f.read().splitlines()

    total_docs = int(stats[0])
    ratio_hits = float(stats[1])

    return jsonify(total_docs=total_docs, ratio_hits=ratio_hits)

@app.route('/stats')
def stats():
    #Checking stats in depth
    return render_template('stats.html')

if __name__ == "__main__":
    app.run(debug=True)
