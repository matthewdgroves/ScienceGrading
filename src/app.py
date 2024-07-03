import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dash_table
import base64
import io
import dash_bootstrap_components as dbc
from numpy import interp

# from dash_bootstrap_templates import load_figure_template
# load_figure_template('COSMO')

#would be nice to get the more sophisticated Download instead of export, to give the exported file a date on it
#would be nice to get emailed copies every time someone runs it

# Initialize the Dash app
app = dash.Dash(__name__, prevent_initial_callbacks='initial_duplicate',external_stylesheets=[dbc.themes.COSMO])
server = app.server

row1 = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.H1("Science department grade calculator"),
                html.H5("First, upload your formative file and confirm that its contents look right. You should see a table with students, some student info, and all of your formative assignments and grades if you scroll to the right. "),
                html.H5("Second, upload your summative file and confirm that its contents look right. It will appear below the first table, so you may have to scroll down. You should see a table with students, some student info, and all of your Learning Targets, with numbers between 0 and 4 for all of the values."),
                html.H5("If your files look wrong, you can always refresh the page to try again"),
                html.H5("If all the data looks good, click the 'Run the grades' button at the very bottom"),
            ],
                style = {'margin-left':'5px', 'margin-top':'7px', 'margin-right':'5px'}
            )
        ])
    ]
)

row2 = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id='formative-data',
                    children=html.Div(['Formative: Drag and Drop or ', html.A('Select')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False),
            ]),
            dbc.Col([
                dcc.Upload(
                    id='summative-data',
                        children=html.Div(['Summative ("Outcomes"): Drag and Drop or ', html.A('Select ')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False),
            ])
        ])
    ]
)

row3 = html.Div([
    dbc.Row([
        dbc.Col([html.Div(id='output-data-upload1')]),
        dbc.Col([html.Div(id='output-data-upload2')]),
    ]),
    dbc.Row([
        dbc.Col([html.Button('Run the grades calculation', id='merge-data-btn', n_clicks=0, style={'margin': '10px'})])
    ])
])

row4 = html.Div([
    dbc.Row([
        dbc.Col([html.Div(id='output-data-upload3')])
    ]),
        # dbc.Row([
        # dbc.Col([html.Div([
        #     html.Button("Download CSV", id="btn_csv"),
        #     dcc.Download(id="download-dataframe-csv"),
        # ])])
   # ])
])

app.layout = dbc.Container(children=[
    row1,
    html.Br(),
    row2,
    html.Br(),
    row3,
    html.Br(),
    row4
])

# Function to parse contents of uploaded CSV file
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    # Decode the base64 encoded string
    decoded = base64.b64decode(content_string)

    # Read the decoded bytes into a pandas DataFrame
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    return df

# LT letter grade conversions
def percentGradeH(LT_grade):
    #A
    if 3.95 <= LT_grade < 4:
        pctGrade = interp(LT_grade, [3.95, 4.0], [99,100])
        return([pctGrade, "H A"])
    if 3.9 <= LT_grade < 3.95:
        pctGrade = interp(LT_grade, [3.9,3.95], [99,99])
        return([pctGrade, "H A"])
    if 3.85 <= LT_grade < 3.9:
        pctGrade = interp(LT_grade, [3.85,3.9], [98,99])
        return([pctGrade, "H A"])
    if 3.8 <= LT_grade < 3.85:
        pctGrade = interp(LT_grade, [3.8,3.85], [97,98])
        return([pctGrade, "H A"])
    if 3.75 <= LT_grade < 3.8:
        pctGrade = interp(LT_grade, [3.75,3.8], [96,97])
        return([pctGrade, "H A"])
    if 3.70 <= LT_grade < 3.75:
        pctGrade = interp(LT_grade, [3.70,3.75], [95,96])
        return([pctGrade, "H A"])
    if 3.65 <= LT_grade < 3.7:
        pctGrade = interp(LT_grade, [3.65,3.7], [94,95])
        return([pctGrade, "H A"])        
    if 3.60 <= LT_grade < 3.65:
        pctGrade = interp(LT_grade, [3.60,3.65], [93,94])
        return([pctGrade, "H A"])
    
    #A-
    if 3.5 <= LT_grade < 3.6:
        pctGrade = interp(LT_grade, [3.5,3.6], [92,93])
        return([pctGrade, "H A-"])
    if 3.4 <= LT_grade < 3.5:
        pctGrade = interp(LT_grade, [3.4,3.5], [92,92])
        return([pctGrade, "H A-"])
    if 3.35 <= LT_grade < 3.4:
        pctGrade = interp(LT_grade, [3.35,3.4], [91,92])
        return([pctGrade, "H A-"])
    if 3.3 <= LT_grade < 3.35:
        pctGrade = interp(LT_grade, [3.3,3.35], [90,91])
        return([pctGrade, "H A-"])
    
    #B+
    if 3.2 <= LT_grade < 3.3:
        pctGrade = interp(LT_grade, [3.2, 3.3], [89,90])
        return([pctGrade, "H B+"])
    if 3.1 <= LT_grade < 3.2:
        pctGrade = interp(LT_grade, [3.1, 3.2], [88,89])
        return([pctGrade, "H B+"])
    if 3.0 <= LT_grade < 3.1:
        pctGrade = interp(LT_grade, [3.0, 3.1], [87,88])
        return([pctGrade, "H B+"])
    
    #B
    if 2.9 <= LT_grade < 3.0:
        pctGrade = interp(LT_grade, [2.9,3.0], [86,87])
        return([pctGrade, "H B"])
    if 2.8 <= LT_grade < 2.9:
        pctGrade = interp(LT_grade, [2.8,2.9], [85,86])
        return([pctGrade, "H B"])
    if 2.7 <= LT_grade < 2.8:
        pctGrade = interp(LT_grade, [2.7,2.8], [83,85])
        return([pctGrade, "H B"]) 

    #B-
    if 2.6 <= LT_grade < 2.7:
        pctGrade = interp(LT_grade, [2.6,2.7], [82,83])
        return([pctGrade, "H B-"])
    if 2.5 <= LT_grade < 2.6:
        pctGrade = interp(LT_grade, [2.5,2.6], [81,82])
        return([pctGrade, "H B-"])
    if 2.4 <= LT_grade < 2.5:
        pctGrade = interp(LT_grade, [2.4,2.5], [80,81])
        return([pctGrade, "H B-"])

    #C+
    if 2.3 <= LT_grade < 2.4:
        pctGrade = interp(LT_grade, [2.3,2.4], [79,80])
        return([pctGrade, "H C+"])
    if 2.2 <= LT_grade < 2.3:
        pctGrade = interp(LT_grade, [2.2,2.3], [78,79])
        return([pctGrade, "H C+"])
    if 2.1 <= LT_grade < 2.2:
        pctGrade = interp(LT_grade, [2.1,2.2], [77,78])
        return([pctGrade, "H C+"])

    #C
    if 2.0 <= LT_grade < 2.1:
        pctGrade = interp(LT_grade, [2.0,2.1], [76,77])
        return([pctGrade, "H C"])
    if 1.9 <= LT_grade < 2.0:
        pctGrade = interp(LT_grade, [1.9,2.0], [75,76])
        return([pctGrade, "H C"])
    if 1.8 <= LT_grade < 1.9:
        pctGrade = interp(LT_grade, [1.8,1.9], [73,75])
        return([pctGrade, "H C"])
    
    #C-
    if 1.74 <= LT_grade < 1.8:
        pctGrade = interp(LT_grade, [1.74,1.8], [76,77])
        return([pctGrade, "C-"])
    if 1.67 <= LT_grade < 1.74:
        pctGrade = interp(LT_grade, [1.67,1.74], [75,76])
        return([pctGrade, "C-"])
    if 1.6 <= LT_grade < 1.67:
        pctGrade = interp(LT_grade, [1.6,1.67], [70,71])
        return([pctGrade, "C-"])
    
    #D+
    if 1.54 <= LT_grade < 1.6:
        pctGrade = interp(LT_grade, [1.54,1.6], [69,70])
        return([pctGrade, "D+"])
    if 1.47 <= LT_grade < 1.54:
        pctGrade = interp(LT_grade, [1.47,1.54], [68,69])
        return([pctGrade, "D+"])
    if 1.4 <= LT_grade < 1.47:
        pctGrade = interp(LT_grade, [1.4,1.47], [67,68])
        return([pctGrade, "D+"])
    
    #D
    if 1.34 <= LT_grade < 1.4:
        pctGrade = interp(LT_grade, [1.34,1.4], [66,67])
        return([pctGrade, "D"])
    if 1.27 <= LT_grade < 1.34:
        pctGrade = interp(LT_grade, [1.27,1.34], [65,66])
        return([pctGrade, "D"])
    if 1.2 <= LT_grade < 1.27:
        pctGrade = interp(LT_grade, [1.2,1.27], [63,65])
        return([pctGrade, "D"])

    #D-
    if 1.14 <= LT_grade < 1.2:
        pctGrade = interp(LT_grade, [1.14,1.2], [62,63])
        return([pctGrade, "D-"])
    if 1.07 <= LT_grade < 1.14:
        pctGrade = interp(LT_grade, [1.07,1.14], [61,62])
        return([pctGrade, "D-"])
    if 1.0 <= LT_grade < 1.07:
        pctGrade = interp(LT_grade, [1.0,1.07], [60,61])
        return([pctGrade, "D-"])
    
    if 0.0 <= LT_grade < 1.0:
        pctGrade = interp(LT_grade, [0, 1.0], [50,60])
        return([pctGrade, "F"])
    
def percentGradeAdv(LT_grade):
    #A
    if 3.85 <= LT_grade < 4:
        pctGrade = interp(LT_grade, [3.85, 4.0], [99,100])
        return([pctGrade, "Adv A"])
    if 3.75 <= LT_grade < 3.85:
        pctGrade = interp(LT_grade, [3.75, 3.85], [99,99])
        return([pctGrade, "Adv A"])
    if 3.60 <= LT_grade < 3.75:
        pctGrade = interp(LT_grade, [3.60, 3.75], [98,99])
        return([pctGrade, "Adv A"])    
    if 3.50 <= LT_grade < 3.60:
        pctGrade = interp(LT_grade, [3.50, 3.60], [97,98])
        return([pctGrade, "Adv A"])    
    if 3.35 <= LT_grade < 3.50:
        pctGrade = interp(LT_grade, [3.35, 3.50], [96,97])
        return([pctGrade, "Adv A"])
    if 3.25 <= LT_grade < 3.35:
        pctGrade = interp(LT_grade, [3.25, 3.35], [95,96])
        return([pctGrade, "Adv A"])
    if 3.10 <= LT_grade < 3.25:
        pctGrade = interp(LT_grade, [3.10, 3.25], [94,95])
        return([pctGrade, "Adv A"])
    if 3.0 <= LT_grade < 3.10:
        pctGrade = interp(LT_grade, [3.0, 3.10], [93,94])
        return([pctGrade, "Adv A"])
    
    #A-
    if 2.95 <= LT_grade < 3.0:
        pctGrade = interp(LT_grade, [2.95, 3.0], [92,93])
        return([pctGrade, "Adv A-"])
    if 2.90 <= LT_grade < 2.95:
        pctGrade = interp(LT_grade, [2.90, 2.95], [92,92])
        return([pctGrade, "Adv A-"])
    if 2.85 <= LT_grade < 2.90:
        pctGrade = interp(LT_grade, [2.85, 2.90], [91,92])
        return([pctGrade, "Adv A-"])   
    if 2.80 <= LT_grade < 2.85:
        pctGrade = interp(LT_grade, [2.80, 2.85], [90,91])
        return([pctGrade, "Adv A-"])    

    #B+
    if 2.74 <= LT_grade < 2.80:
        pctGrade = interp(LT_grade, [2.74, 2.80], [89,90])
        return([pctGrade, "Adv B+"])   
    if 2.67 <= LT_grade < 2.74:
        pctGrade = interp(LT_grade, [2.67, 2.74], [88,89])
        return([pctGrade, "Adv B+"])
    if 2.60 <= LT_grade < 2.67:
        pctGrade = interp(LT_grade, [2.60, 2.67], [87,88])
        return([pctGrade, "Adv B+"])

    #B
    if 2.54 <= LT_grade < 2.60:
        pctGrade = interp(LT_grade, [2.54, 2.60], [86,87])
        return([pctGrade, "Adv B"])
    if 2.47 <= LT_grade < 2.54:
        pctGrade = interp(LT_grade, [2.47, 2.54], [85,86])
        return([pctGrade, "Adv B"])
    if 2.40 <= LT_grade < 2.47:
        pctGrade = interp(LT_grade, [2.40, 2.47], [83,85])
        return([pctGrade, "Adv B"]) 
    
    #B-
    if 2.34 <= LT_grade < 2.40:
        pctGrade = interp(LT_grade, [2.34, 2.4], [82,83])
        return([pctGrade, "Adv B-"])
    if 2.27 <= LT_grade < 2.34:
        pctGrade = interp(LT_grade, [2.27, 2.34], [81,82])
        return([pctGrade, "Adv B-"])
    if 2.20 <= LT_grade < 2.27:
        pctGrade = interp(LT_grade, [2.20, 2.27], [80,81])
        return([pctGrade, "Adv B-"])
    
    #C+
    if 2.14 <= LT_grade < 2.20:
        pctGrade = interp(LT_grade, [2.14, 2.20], [79,80])
        return([pctGrade, "Adv C+"])
    if 2.07 <= LT_grade < 2.14:
        pctGrade = interp(LT_grade, [2.07, 2.14], [78,79])
        return([pctGrade, "Adv C+"])
    if 2.0 <= LT_grade < 2.07:
        pctGrade = interp(LT_grade, [2.0, 2.07], [77,78])
        return([pctGrade, "Adv C+"])
    
    #C
    if 1.94 <= LT_grade < 2.0:
        pctGrade = interp(LT_grade, [1.94, 2.0], [76,77])
        return([pctGrade, "Adv C"])
    if 1.87 <= LT_grade < 1.94:
        pctGrade = interp(LT_grade, [1.87, 1.94], [75,76])
        return([pctGrade, "Adv C"])
    if 1.8 <= LT_grade < 1.87:
        pctGrade = interp(LT_grade, [1.80, 1.87], [73,75])
        return([pctGrade, "Adv C"])
    

    #C-
    if 1.74 <= LT_grade < 1.8:
        pctGrade = interp(LT_grade, [1.74,1.8], [72,73])
        return([pctGrade, "C-"])
    if 1.67 <= LT_grade < 1.74:
        pctGrade = interp(LT_grade, [1.67,1.74], [71,72])
        return([pctGrade, "C-"])
    if 1.6 <= LT_grade < 1.67:
        pctGrade = interp(LT_grade, [1.6,1.67], [70,71])
        return([pctGrade, "C-"])
    
    #D+
    if 1.54 <= LT_grade < 1.6:
        pctGrade = interp(LT_grade, [1.54,1.6], [69,70])
        return([pctGrade, "D+"])
    if 1.47 <= LT_grade < 1.54:
        pctGrade = interp(LT_grade, [1.47,1.54], [68,69])
        return([pctGrade, "D+"])
    if 1.4 <= LT_grade < 1.47:
        pctGrade = interp(LT_grade, [1.4,1.47], [67,68])
        return([pctGrade, "D+"])
    
    #D
    if 1.34 <= LT_grade < 1.4:
        pctGrade = interp(LT_grade, [1.34,1.4], [66,67])
        return([pctGrade, "D"])
    if 1.27 <= LT_grade < 1.34:
        pctGrade = interp(LT_grade, [1.27,1.34], [65,66])
        return([pctGrade, "D"])
    if 1.2 <= LT_grade < 1.27:
        pctGrade = interp(LT_grade, [1.2,1.27], [63,65])
        return([pctGrade, "D"])

    #D-
    if 1.14 <= LT_grade < 1.2:
        pctGrade = interp(LT_grade, [1.14,1.2], [62,63])
        return([pctGrade, "D-"])
    if 1.07 <= LT_grade < 1.14:
        pctGrade = interp(LT_grade, [1.07,1.14], [61,62])
        return([pctGrade, "D-"])
    if 1.0 <= LT_grade < 1.07:
        pctGrade = interp(LT_grade, [1.0,1.07], [60,61])
        return([pctGrade, "D-"])
    
    if 0.0 <= LT_grade < 1.0:
        pctGrade = interp(LT_grade, [0, 1.0], [50,60])
        return([pctGrade, "F"])

# Callback to upload formative file
@app.callback(Output('output-data-upload1', 'children'),
              [Input('formative-data', 'contents'),
               Input('formative-data', 'filename')])
def upload_file_1(contents, filename):
    if contents is None:
        raise PreventUpdate

    df1 = parse_contents(contents, filename)
    return html.Div([
        html.H2(f'Successfully uploaded {filename}.'),
        html.H4('Please confirm that this data looks right before uploading the Summative file'),
        dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in df1.columns],
            data=df1.to_dict('records'),
            fill_width=False
        )
    ])

# Callback to upload summative file
@app.callback(Output('output-data-upload2', 'children'),
              [Input('summative-data', 'contents'),
               Input('summative-data', 'filename')])
def upload_file_2(contents, filename):
    if contents is None:
        raise PreventUpdate

    df2 = parse_contents(contents, filename)
    return html.Div([
        html.H2(f'Successfully uploaded: {filename}.'),
        html.H4('Please confirm that this data looks right before clicking the "Run grades" button below'),
        dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in df2.columns],
            data=df2.to_dict('records'),
            fill_width=False
        )
    ])

# Callback to clean and display data
@app.callback(
        Output('output-data-upload1', 'children', allow_duplicate=True),
        Output('output-data-upload2', 'children', allow_duplicate=True),
        Output('output-data-upload3', 'children'),
              [Input('merge-data-btn', 'n_clicks')],
              [dash.dependencies.State('formative-data', 'contents'),
               dash.dependencies.State('formative-data', 'filename'),
               dash.dependencies.State('summative-data', 'contents'),
               dash.dependencies.State('summative-data', 'filename')])
def merge_and_display(n_clicks, formative_contents, formative_filename, summative_contents, summative_filename):
    if n_clicks == 0:
        raise PreventUpdate

    if formative_contents is None or summative_contents is None:
        raise PreventUpdate

    # import formative data, keep only the one relevant column, name, and ID 
    f_df = parse_contents(formative_contents, formative_filename)
    f_df['Formative Pct Grade'] = list(f_df['Formative Assignments Current Score'])
    f_df = f_df[["Student", "ID", 'Formative Pct Grade']]


    s_df = parse_contents(summative_contents, summative_filename)
    #s_df['LT Average'] = s_df.mean(numeric_only=True, axis=1)
    droppedColumnsLT = [i for i in s_df if "mastery points" in i]
    # droppedColumnsLT.append("Student ID") #keep this column for merging later
    droppedColumnsLT.append("Student SIS ID")
    s_df = s_df.drop(droppedColumnsLT, axis=1)
    s_df = s_df.dropna(how='all', axis=1,)
    s_df["LT Average"] = s_df.loc[:,[c for c in s_df.columns if c!= "Student ID"]].mean(axis=1)
    s_df = s_df[['Student name', 'Student ID', 'LT Average']]

    gradePercentageH = []
    gradeLetterH = []

    gradePercentageAdv = []
    gradeLetterAdv = []

    for num in s_df['LT Average']:

        pct = percentGradeH(num)[0]
        gradePercentageH.append(pct)

        pct = percentGradeAdv(num)[0]
        gradePercentageAdv.append(pct)

        lett = percentGradeH(num)[1]
        gradeLetterH.append(lett)

        lett = percentGradeAdv(num)[1]
        gradeLetterAdv.append(lett)

        #print(num, pct, lett)

    s_df['LT Letter Grade: H'] = gradeLetterH
    s_df['Summative Pct Grade: H'] = gradePercentageH

    s_df['LT Letter Grade: Adv'] = gradeLetterAdv
    s_df['Summative Pct Grade: Adv'] = gradePercentageAdv


    # renaming them to have a common column title
    f_df.rename(columns={"ID":"Student ID"}, inplace=True)

    # Merge dataframes based on a common column, using the ID was easier than trying to re-order the names to match (one was "first last", the other was "last, first")
    merged_df = pd.merge(f_df, s_df, on='Student ID', how='inner')
    merged_df = merged_df[['Student', 'Formative Pct Grade','LT Average', 'LT Letter Grade: H', 'Summative Pct Grade: H', "LT Letter Grade: Adv",'Summative Pct Grade: Adv']]


    formativeNumGrades = list(merged_df["Formative Pct Grade"])
    summativeNumGradesH = merged_df['Summative Pct Grade: H']
    summativeNumGradesAdv = merged_df['Summative Pct Grade: Adv']

    totalModGradeH=[]
    totalModGradeAdv=[]

    for i in range(len(list(summativeNumGradesH))):
        entry = .4*float(formativeNumGrades[i]) + .6*summativeNumGradesH[i]
        totalModGradeH.append(entry)

    for i in range(len(list(summativeNumGradesAdv))):
        entry = .4*float(formativeNumGrades[i]) + .6*summativeNumGradesAdv[i]
        totalModGradeAdv.append(entry)

    merged_df['Total Year Pct Grade: H'] = totalModGradeH
    merged_df['Total Year Pct Grade: Adv'] = totalModGradeAdv
    merged_df = merged_df.round(3)

    # Display the merged dataframe in a Dash DataTable
    return [
        html.Div(),
        html.Div(),
        html.Div([
            html.H2('Results for the year to date:'),
            html.H5("You can sort any of these columns by clicking the small arrows beside each column title. You can also search for a student, but it is case-sensitive. You can also delete any of the columns that aren't helpful to you, like the LT letter grades"),
            dash_table.DataTable(
                columns=[{'name': col, 'id': col, 'deletable': True} for col in merged_df.columns],
                data=merged_df.to_dict('records'),
                fill_width=False,
                sort_action='native',
                filter_action='native',
                export_format='csv'
        )
    ])

    ]
# nice to add: could rename the file with the dates it was made
# # Callback to export the final data
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     State("output-data-upload3", "children"),
#     prevent_initial_call=True,
# )
# def func(n_clicks, f_df):
#     return dcc.send_data_frame(f_df[2].to_csv, "mydf.csv")

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
