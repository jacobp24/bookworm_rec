from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
from search import hybrid_search  # Make sure this is correctly implemented

# Initialize the Flask application
app = Flask(__name__)

# Preload your dataset and indices
df = pd.read_csv('data_with_embeddings.csv')  # Adjust path as needed
distances = np.load('distances.npy')
indices = np.load('indices.npy')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        # Safely get the minimum rating from the form, default to '1' if not provided
        min_rating = request.form.get('minRating', '1')

        # Call your search function with the query
        results = hybrid_search(df, query, distances, indices)

        # Filter results by rating
        if not results.empty:
            results = results[results['Ratings'] >= int(min_rating)]
            
            cards = "".join([f"<div class='col-lg-3 col-md-4 col-sm-6 mb-4'>" +
                             f"<div class='card' style='width: 100%;'><img src='{row['Image_URL']}' class='card-img-top' alt='{row['book_title']}'>" +
                             f"<div class='card-body'><h5 class='card-title'>{row['book_title']}</h5><p class='card-text'>Rating: {row['Ratings']}</p><a href='{row['Image_URL']}' class='btn btn-primary'>View Image</a></div></div></div>"
                             for index, row in results.iterrows()])
            results_formatted = f"<div class='row'>{cards}</div>"
        else:
            results_formatted = "<p>No results found.</p>"
        
        return render_template_string("""
                                        <!DOCTYPE html>
                                        <html>
                                        <head>
                                            <title>Book Search</title>
                                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                                        </head>
                                        <body>
                                            <div class="container">
                                                <h1>Book Search</h1>
                                                <form method="post" class="mb-3">
                                                    <div class="form-group">
                                                        <label for="query">Query:</label>
                                                        <input type="text" class="form-control" name="query" id="query">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="minRating">Minimum Rating:</label>
                                                        <input type="range" class="form-control-range" name="minRating" id="minRating" min="1" max="10" value="1" oninput="this.nextElementSibling.value = this.value">
                                                        <output>1</output>
                                                    </div>
                                                    <button type="submit" class="btn btn-primary">Search</button>
                                                </form>
                                                <div class="results">{{ results_formatted|safe }}</div>
                                            </div>
                                        </body>
                                        </html>
                                      """, results_formatted=results_formatted)
    else:
        # Display the form with the slider for ratings on initial page load
        return render_template_string("""
                                        <!DOCTYPE html>
                                        <html>
                                        <head>
                                            <title>Book Search</title>
                                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                                        </head>
                                        <body>
                                            <div class="container">
                                                <h1>Book Search</h1>
                                                <form method="post" class="mb-3">
                                                    <div class="form-group">
                                                        <label for="query">Query:</label>
                                                        <input type="text" class="form-control" name="query" id="query">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="minRating">Minimum Rating:</label>
                                                        <input type="range" class="form-control-range" name="minRating" id="minRating" min="1" max="10" value="1" oninput="this.nextElementSibling.value = this.value">
                                                        <output>1</output>
                                                    </div>
                                                    <button type="submit" class="btn btn-primary">Search</button>
                                                </form>
                                            </div>
                                        </body>
                                        </html>
                                      """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)