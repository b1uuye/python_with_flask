# import necessary libraries
from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
import io, base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('myChart.html')

# creating the route for the line graph
@app.route('/line-graph', methods=['POST'])
def line_graph():
    age_raw = request.form.get('age', '').strip()
    wealth_raw = request.form.get('wealth', '').strip()

    # creating normal data that will be outputted if nothing is completed
    if not age_raw:
        age_raw = '16,23,36,43,51,56'
    if not wealth_raw:
        wealth_raw = '0, 500, 2300, 10000, 42000, 90000'

    # splitting each of the inputs so that they can be classed as their own input 
    try:
        age = [int(a.strip()) for a in age_raw.split(',') if a.strip()]
        wealth = [int(w.strip()) for w in wealth_raw.split(',') if w.strip()]
    except ValueError:
        return render_template(
            'myChart.html',
            title='Line Graph',
            error="Error: Please enter only numbers separated by commas."
        )

    # if condition to check that the amount of inputs in age is the same as inputs in wealth so that the graph is outputted well
    if len(age) != len(wealth):
        return render_template(
            'myChart.html',
            title='Line Graph',
            error="Error: Age and wealth lists must have the same length."
        )
    
    df = pd.DataFrame({'age': age, 'wealth': wealth})
    fig = px.line(df, x='age', y='wealth', markers=True, title="Wealth Over Age")
    fig.show()

    plotly_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('myChart.html', title='Line Graph', plotly_chart=plotly_chart)

# creating the route for the table to show countries
@app.route('/table', methods=['POST'])
def table():
    country_raw = request.form.get('country', '').strip()
    year_raw = request.form.get('year', '').strip()
    population_raw = request.form.get('population', '').strip()

        # creating normal data that will be outputted if nothing is completed
    if not country_raw:
        country_raw = 'Jamaica, England, Spain'
    if not year_raw:
        year_raw = '200, 55, 1100'
    if not population_raw:
        population_raw = '20000, 550000, 11023230'

        # splitting each of the inputs so that they can be classed as their own input 
    try:
        countries = [c.strip() for c in country_raw.split(',') if c.strip()]
        years = [int(y.strip()) for y in year_raw.split(',') if y.strip()]
        populations = [int(p.strip()) for p in population_raw.split(',') if p.strip()]
    except ValueError:
        return render_template(
            'myChart.html',
            title='Table',
            error="Error: Please enter valid numbers for Year and Population."
        )

        # if condition to check that the amount of inputs in country, age and population is the same as inputs in wealth so that the table is outputted well
    if not (len(countries) == len(years) == len(populations)):
        return render_template(
            'myChart.html',
            title='Table',
            error="Error: Country, Year, and Population lists must have the same length."
        )

    # Build the matrix for Plotly table
    data_matrix = [["Country", "Year", "Population"]]
    for c, y, p in zip(countries, years, populations):
        data_matrix.append([c, y, p])

    fig = ff.create_table(data_matrix)
    table_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('myChart.html', title='Table', table_chart=table_chart)




if __name__ == '__main__':
    app.run(debug=True, port=3001)