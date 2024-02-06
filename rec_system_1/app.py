from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
from search import hybrid_search

# Initialize the Flask application
app = Flask(__name__)

# Preload your dataset and indices
df = pd.read_csv('data_with_embeddings.csv')  # Adjust path as needed
distances = np.load('distances.npy')
indices = np.load('indices.npy')

# Route for handling the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        # Call your search function with the query
        results = hybrid_search(df, query, distances, indices)
        
        # Process results for display
        if not results.empty:
            results_formatted = "<br>".join([f"{row['book_title']}: <a href='{row['Image_URL']}'>{row['Image_URL']}</a>" for index, row in results.iterrows()])
        else:
            results_formatted = "No results found."
        
        return render_template_string("""
                                        <h1>Book Search</h1>
                                        <form method="post">
                                            Query: <input type="text" name="query"><br>
                                            <input type="submit" value="Search">
                                        </form>
                                        <div>{{ results_formatted|safe }}</div>
                                      """, results_formatted=results_formatted)
    else:
        # Display the form
        return render_template_string("""
                                        <h1>Book Search</h1>
                                        <form method="post">
                                            Query: <input type="text" name="query"><br>
                                            <input type="submit" value="Search">
                                        </form>
                                      """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
