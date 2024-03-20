import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go


#######################
# Constants
BLUE = '#006BA2'
CYAN = '#3EBCD2'
GREEN = '#379A8B'
YELLOW = '#EBB434'
OLIVE = '#B4BA39'
PURPLE = '#9A607F'
RED = '#DB444B'
GOLD = '#D1B07C'
GREY =  '#758D99'
BLUE_LIGHT = '#98DAFF'
BLUE_DARK = '#00588D'
CYAN_LIGHT = '#6FE4FB'
CYAN_DARK = '#005F73'
GREEN_LIGHT = '#86E5D4'
GREEN_DARK = '#005F52'
YELLOW_LIGHT = '#FFCB4D'
YELLOW_DARK = '#714C00'
OLIVE_LIGHT = '#D7DB5A'
OLIVE_DARK = '#4C5900'
PURPLE_LIGHT = '#FFC2E3'
PURPLE_DARK = '#78405F'
RED_LIGHT = '#FFA39F'
RED_DARK = '#A81829'
GOLDLIGHT = '#F2CF9A'
GOLD_DARK = '#674E1F'




#######################
# Page configuration
st.set_page_config(
    page_title = "Stili alimentari",
    page_icon='🥑',
    layout='wide',
    initial_sidebar_state='expanded'
)

alt.themes.enable('dark')

#######################
# CSS styling



#######################
# Load Data
df = pd.read_csv('data/stili_al.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('🥑 Stili alimentari')

    countries = ['All'] + list(df.country.unique())
    selected_country = st.selectbox('Select a country', countries)

    if selected_country == 'All':
        df_filtered = df
    else:
        df_filtered = df.query('country == @selected_country')

        # region
        regions = ['All'] + list(df_filtered.regio.unique())
        selected_region = st.selectbox('Select a region', regions)
        if selected_region != 'All':
            df_filtered = df_filtered.query('regio == @selected_region')

    # gender
    genders = ['All'] + list(df.s3.unique())
    selected_gender = st.selectbox('Select a gender', genders)
    if selected_gender != 'All':
        df_filtered = df_filtered.query('s3 == @selected_gender')

    # age group
    ages = ['All'] + list(  np.sort(df.eta.unique() ))
    selected_age = st.selectbox('Select an age group', ages)
    if selected_age != 'All':
        df_filtered = df_filtered.query('eta == @selected_age')
    
    # s5
    s5_list = ['All'] + list(df.s5.unique())
    selected_s5 = st.selectbox('Select ...', s5_list)
    if selected_s5 != 'All':
        df_filtered = df_filtered.query('s5 == @selected_s5')
    
    # Metric to plot
    st.markdown("""<br><hr>""", unsafe_allow_html=True) # a gap br and a line (hr)
    metrics = ['stile', 'q4__4', 'q4__5', 'q4__6', 'q4__7', 'q4__8', 'q4__9', 'q4__10',
               'q5__4', 'q5__5', 'q5__6', 'q5__7', 'q5__8', 'q5__9', 'q5__10',
               ]
    selected_metric = st.selectbox('📊 Select a metric', metrics)

    # Color theme
    st.markdown("""<br><hr>""", unsafe_allow_html=True) # a gap br and a line (hr)
    color_theme_list = ['blue', 'cyan', 'green', 'red', 'yellow', 'olive', 'purple', 'gold']
    selected_color_theme = st.selectbox('🎨 Select a color theme', color_theme_list)

    # number of observations
    n = len(df)
    n_sample = len(df_filtered)


#######################
# Grouping function
def group_df(df, metric: str) -> pd.Series:
    # group for a bar chart
    s = (df
            .groupby(metric)
            .count()
        ).country.sort_values()
    return s


#######################
# Plots
def make_donut(input_color):
    if input_color == 'blue':
        chart_color = [BLUE_LIGHT, BLUE_DARK]
    if input_color == 'cyan':
        chart_color = [CYAN_LIGHT, CYAN_DARK]
    if input_color == 'green':
        chart_color = [GREEN_LIGHT, GREEN_DARK]
    if input_color == 'yellow':
        chart_color = [YELLOW_LIGHT, YELLOW_DARK]
    if input_color == 'red':
        chart_color = [RED_LIGHT, RED_DARK]
    if input_color == 'olive':
        chart_color = [OLIVE_LIGHT, OLIVE_DARK]
    if input_color == 'purple':
        chart_color = [PURPLE_LIGHT, PURPLE_DARK]
    if input_color == 'gold':
        chart_color = [GOLDLIGHT, GOLD_DARK]

    # Calculate percentage
    percentage = (n_sample / n) * 100
    remaining_percentage = 100 - percentage

    # Prepare the data for the donut chart
    data = pd.DataFrame({
        'Category': ['Sample', 'Remaining'],
        'Value': [percentage, remaining_percentage]
    })

    # Create a donut chart
    donut_chart = alt.Chart(data).mark_arc(innerRadius=30, radius=50).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal", scale=alt.Scale(domain=['Sample', 'Remaining'], range=chart_color),legend=None),
        tooltip=["Category", "Value"]
    ).properties(width=130, height=130)

    # Create a text mark for displaying the percentage in the center
    text = alt.Chart(pd.DataFrame({"Value": [f"{percentage:.1f}%"]})).mark_text(size=20, baseline='middle').encode(
        text='Value:N'
    )

    # Layer the donut chart and the text mark
    chart = (donut_chart + text)
    
    return chart    

def make_bars_plotly(input_color, s: pd.Series, width=800, height=600):
    color_map = {
        'blue': BLUE,
        'cyan': CYAN,
        'green': GREEN,
        'yellow': YELLOW,
        'red': RED,
        'olive': OLIVE,
        'purple': PURPLE,
        'gold': GOLD
    }
    chart_color = color_map.get(input_color, 'blue')  # Default to blue if color not found

    fig = go.Figure(go.Bar(
        x=s.values,
        y=s.index,
        orientation='h',
        marker=dict(color=chart_color),
    ))

    # Update layout for a cleaner look
    fig.update_layout(
        #title=title,
        xaxis=dict(
            showticklabels=True,
            showgrid=True,
            tickangle=0,
            titlefont=dict(size=12),
            title_standoff=25
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            linecolor='black'
        ),
        plot_bgcolor='white',
        showlegend=False,
        width=width,
        height=height,
    )

    fig.update_yaxes(tickfont=dict(size=12), tickmode='array', tickvals=list(s.index))
    fig.update_xaxes(tickfont=dict(size=12))

    return fig
        
#######################
# Dashboard Main Panel    
col = st.columns((1.5, 4.5, 0.5), gap='medium')

with col[0]:
    st.markdown('#### Observations')
    st.markdown(f'### {n_sample:,}')
    #st.metric(label='', value=f"{n_sample:,}")

    st.markdown('#### % of Total Observations')
    st.altair_chart(make_donut(selected_color_theme))
    

with col[1]:
    st.markdown(f'#### {selected_metric.capitalize()}')
    
    # create a series - value counts for a selected metric
    metric_series = group_df(df_filtered, selected_metric)
    #st.title(selected_metric)
    fig = make_bars_plotly(selected_color_theme, metric_series)
    st.plotly_chart(fig)
    #bar_chart = make_bars(input_color=selected_color_theme, s=metric_series, title=selected_metric)
    #st.pyplot(bar_chart)

#######################
