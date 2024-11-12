from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Prepare top 50 books data for the main page
    top_books = [{
        'title': row['Book-Title'],
        'author': row['Book-Author'],
        'image_url': row['Image-URL-M'],
        'rating': row['avg_rating'],
        'genre': 'Fiction'  # Example genre, replace if available
    } for _, row in popular_df.iterrows()]

    return render_template('index.html', top_books=top_books)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        try:
            # Find the index of the user input book
            index = np.where(pt.index == user_input)[0][0]
            # Get the top 5 similar books
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)

            return render_template('recommend.html', data=data, error=None)
        except IndexError:
            return render_template('recommend.html', error="Book not found", data=None)
    return render_template('recommend.html', error=None, data=None)


if __name__ == '__main__':
    app.run(debug=True)
