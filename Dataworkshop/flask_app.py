# import necessary libraries
from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import io, base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chart.html')

@app.route('/bar-chart', methods=['POST'])
def bar_chart():
    books_raw = request.form.get('books', '').strip()
    owned_raw = request.form.get('owned', '').strip()

    if not books_raw:
        books_raw = 'Fiction, Fantasy, Horror'
    if not owned_raw:
        owned_raw = '20, 55, 7'

    # list comprehension
    # syntax - newlist = [expression for item in iterable]
    books = [b.strip() for b in books_raw.split(',')]
    owned = [int(o.strip()) for o in owned_raw.split(',')]
    
    fig = go.Figure(data=[go.Bar(x=books, y=owned)])
    fig.update_layout(
        title={
            'text': 'Book Owned per Genre',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Book Genre',
        yaxis_title='Number of Books Owned'
    )
    plotly_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('chart.html', title='Bar Chart', plotly_chart=plotly_chart)

@app.route('/pie-chart', methods=['POST'])
def pie_chart():
    pets_raw = request.form.get('pets', '').strip()
    value_raw = request.form.get('value', '').strip()

    if not pets_raw:
        pets_raw = 'Cat, Dog, Horse'
    if not value_raw:
        value_raw = '7, 3, 2'
    
    pets = [p.strip() for p in pets_raw.split(',')]
    value = [v.strip() for v in value_raw.split(',')]

    fig, ax = plt.subplots()
    ax.pie(value, labels=pets, autopct='%1.1f', startangle=90)
    ax.axis('equal')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    matplotlib_chart = f'<img src="data:image/png;base64, {base64.b64encode(img_bytes.getvalue()).decode()}" />'

    return render_template('chart.html', title='Pie Chart', matplotlib_chart=matplotlib_chart)

if __name__ == '__main__':
    app.run(debug=True, port=3001)