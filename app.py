# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:28:40 2024

@author: Inbat
"""
import dash
import dash_html_components as html
from dash import dcc as dcc
import dash_bootstrap_components as dbc
import webbrowser
import pandas as pd
import pickle
from dash.dependencies import Input, Output, State

#declaring global variables
project_name=None
app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


#defining my fuction

def check_data(age, cholestrol, ap_hi, ap_lo, bmi, gluc):
    file = open("rf.pkl", "rb")
    model_from_pickel = pickle.load(file)

    with open('min_max_scaler.pkl', 'rb') as file:
        loaded_scaler = pickle.load(file)

    scaled_data = loaded_scaler.transform([[age, cholestrol, ap_hi, ap_lo, bmi, gluc]])
    print("data ",scaled_data)
    print("predict ",model_from_pickel.predict(scaled_data))
    return model_from_pickel.predict(scaled_data)


def UI_main():
    
    
    main_ui = dbc.Container(html.Div(
        [
            dbc.Alert(children="Heart Disease Checker", id="Main_head", color="success", style={'fontSize': '24px', 'padding': '10px',
                                                    'width': '100%', 'text-align': 'center','fontFamily': 'Arial, sans-serif',
                                                    'border': '1px solid #ced4da', 'border-radius': '0.25rem'}),

            dbc.Label("AGE",style={'fontSize': '18px','fontWeight': 'bold',
                                                    'width': '100%', 'color': 'black','fontFamily': 'Arial, sans-serif'}),
            dbc.Input(id="age_input", placeholder="Age of the patient", type="number",style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Label("CHOLESTEROL [ 1: normal, 2: above normal, 3: well above normal ]",style={'fontSize': '18px','fontFamily': 'Arial, sans-serif',
                                'fontWeight': 'bold','width': '100%', 'color': 'black'}),
            dbc.Input(id="cholestrol_input", placeholder="Cholesterol of the patient", type="number", max=3, min=1,style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Label("SYSTOLIC BP",style={'fontSize': '18px',
                                'fontWeight': 'bold','width': '100%', 'color': 'black','fontFamily': 'Arial, sans-serif'}),
            dbc.Input(id="ap_hi_input", placeholder="AP_HI of the patient", type="number", min=100,style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Label("DIASTOLIC BP",style={'fontSize': '18px', 
                                'fontWeight': 'bold','width': '100%', 'color': 'black','fontFamily': 'Arial, sans-serif'}),
            dbc.Input(id="ap_low_input", placeholder="AP_LOW of the patient", type="number", min=60,style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Label("BMI",style={'fontSize': '18px',
                                'fontWeight': 'bold','width': '100%', 'color': 'black','fontFamily': 'Arial, sans-serif'}),
            dbc.Input(id="BMI_input", placeholder="BMI of the patient", type="number",style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Label("GLUCOSE [1: normal, 2: above normal, 3: well above normal]",style={'fontSize': '18px',
                                'fontWeight': 'bold','width': '100%', 'color': 'black','fontFamily': 'Arial, sans-serif'}),
            dbc.Input(id="Gluc_input", placeholder="Glucose of the patient", type="number", max=3, min=1,style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),

            dbc.Button("Submit", id="button_one", color='secondary', className="mt-3", style={'width': '100%', 'fontSize': '20px','fontFamily': 'Arial, sans-serif'}),

            html.Div(id="result",className="mt-3"),
        ],
        className="p-5", style={'marginTop': '20px', 'marginBottom': '22px'}  # Added marginBottom for spacing at the bottom
    ))


    return main_ui

def auto_openbrowser():
    webbrowser.open_new("http://127.0.0.1:8050/")

@app.callback(
    Output( 'result', 'children' ),
    Output('result','style'),
    
    [
    Input( 'button_one','n_clicks'),
    Input('age_input','value'),
    Input('cholestrol_input','value'),
    Input('ap_hi_input','value'),
    Input('ap_low_input','value'),
    Input('BMI_input','value'),
    Input('Gluc_input','value')
    ]
    
    )
def review_update(n_clicks,value_one,value_two,value_three,value_four,value_five,value_six):
    
    print("Data Type = ", type(n_clicks))
    print("Value = ", str(n_clicks))
    n_clicks_previous=0
    print("n_clicks:",n_clicks)
    print("n_clicks_previous:",n_clicks_previous)
    if n_clicks > n_clicks_previous:
        n_clicks_previous=n_clicks
        print("n_clicks_previous:",n_clicks_previous)
        response = check_data(value_one,value_two,value_three,value_four,value_five,value_six)
        print(response)
        if (response[0] == 0):
            return 'The patient not affected by Heart disease',{'fontSize': '24px', 'background-color': 'green', 'padding': '10px',
                                                    'width': '100%', 'color': 'black', 'text-align': 'center',
                                                    'border': '1px solid #ced4da', 'border-radius': '0.25rem'}
        
        else:
            return'The patient affected by Heart disease',{'fontSize': '24px', 'background-color': 'red', 'padding': '10px',
                                                    'width': '100%', 'color': 'black', 'text-align': 'center',
                                                    'border': '1px solid #ced4da', 'border-radius': '0.25rem'}
    else:
        return ""

 
#main fuction to control flow

def main():
    print("Start of project")
   
    global project_name,review,app
    
    project_name="Heart disease Prediction"
    app.title=project_name
    app.layout=UI_main()
    app.run_server()
    auto_openbrowser()
    print("End of project")
    
    project_name=None
    review=None
    app=None
    scrappedReviews=None
    
#calling the main function
if __name__=='__main__':
    main()
