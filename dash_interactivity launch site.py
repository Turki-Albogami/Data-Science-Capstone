# spacex_final_complete.py
# الكود النهائي لجميع التاسكات مطابق للصورة

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------
# 1. تحميل البيانات
# -----------------------------------------------------------------
print("جاري تحميل بيانات SpaceX...")
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(url)

# حساب min و max للـ Payload
min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())

# -----------------------------------------------------------------
# 2. إنشاء تطبيق Dash
# -----------------------------------------------------------------
app = Dash(__name__)

# الحصول على قائمة المواقع الفريدة
launch_sites = sorted(spacex_df['Launch Site'].unique().tolist())

# -----------------------------------------------------------------
# 3. تصميم الواجهة (مطابق للصورة)
# -----------------------------------------------------------------
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard"),
    
    html.Br(),
    
    # Dropdown Menu
    html.Div([
        html.Label("Select Launch Site:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
            ] + [
                {'label': site, 'value': site} for site in launch_sites
            ],
            value='ALL',
            placeholder='Select a Launch Site here',
            searchable=True
        )
    ]),
    
    html.Br(),
    html.Hr(),
    html.Br(),
    
    # Range Slider (مطابق للصورة)
    html.Div([
        html.Label("Payload range (Kg):", style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={
                0: '0',
                2500: '2500',
                5000: '5000',
                7500: '7500',
                10000: '10000'
            },
            value=[min_payload, max_payload]
        )
    ]),
    
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    
    # Pie Chart
    html.Div([
        html.H3("Pie Chart: Launch Success Analysis"),
        dcc.Graph(id='success-pie-chart')
    ]),
    
    html.Br(),
    html.Hr(),
    html.Br(),
    
    # Scatter Plot (مطابق للصورة)
    html.Div([
        html.H3("Scatter Plot: Payload vs Launch Outcome"),
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])

# -----------------------------------------------------------------
# 4. Callback للـ Pie Chart
# -----------------------------------------------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        success_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts()
        fig = px.pie(
            values=success_counts.values,
            names=success_counts.index,
            title='Total Success Launches By Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = len(filtered_df[filtered_df['class'] == 1])
        failure_count = len(filtered_df[filtered_df['class'] == 0])
        
        fig = px.pie(
            values=[success_count, failure_count],
            names=['Success', 'Failure'],
            title=f'Total Success Launches for site {entered_site}'
        )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    
    return fig

# -----------------------------------------------------------------
# 5. Callback للـ Scatter Plot (مطابق للصورة)
# -----------------------------------------------------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_chart(entered_site, payload_range):
    # فلترة البيانات حسب payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        # مطابق للصورة: "Correlation between Payload and Success for all Sites"
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites',
            labels={'class': 'Mission Outcome'}
        )
    else:
        fig = px.scatter(
            filtered_df[filtered_df['Launch Site'] == entered_site],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {entered_site}',
            labels={'class': 'Mission Outcome'}
        )
    
    # تنسيق مطابق للصورة
    fig.update_layout(
        title_x=0.5,
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Failure', 'Success'],
            title='Mission Outcome'
        ),
        xaxis=dict(title='Payload Mass (kg)'),
        legend_title_text='Booster Version Category'
    )
    
    # تحسين حجم النقاط
    fig.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    
    return fig

# -----------------------------------------------------------------
# 6. تشغيل التطبيق
# -----------------------------------------------------------------
if __name__ == '__main__':
    print("✅ الكود النهائي جاهز!")
    print("🌐 افتح: http://127.0.0.1:8050")
    print("\n📋 المكونات المطابقة للصورة:")
    print("   1. Range Slider: 0, 2500, 5000, 7500, 10000")
    print("   2. Scatter Plot عنوان: 'Correlation between Payload and Success for all Sites'")
    print("   3. Legend: Booster Version Category مع الألوان")
    app.run(debug=True)