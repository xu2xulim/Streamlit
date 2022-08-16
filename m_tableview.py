import streamlit as st

def get_param(param_name):
    query_params = st.experimental_get_query_params()
    try:
        return query_params[param_name][0]
    except:
        st.write('Parameters is missing')
        return False

def get_params(params_names_list):
    query_params = st.experimental_get_query_params()
    responses = []
    for parameter in params_names_list:
        try:
            responses.append(query_params[parameter][0])
        except Exception as e:
            responses.append(None)
    return responses

x = st.number_input('X Parameter',value = float(get_param('x')))

y = st.number_input('Y Parameter',value = float(get_param('y')))

st.write(x+y)
