import streamlit as st
from datetime import date 
import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = '2015-01-01'
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction System")

stocks = ("AAPL","GOOG","MSFT","GME")
selected_stock = st.selectbox("Select dataseet for prediction", stocks)

n_years = st.slider("Years of predition",1,4)
period = n_years * 365

#use function to cache the data downloaded from the api
@st.cache
def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    #set the date as the first column 
    data.reset_index(inplace=True)
    return data

data_lead_state = st.text("Load data...")
data = load_data(selected_stock)
data_lead_state.text("Loading data...done!")

st.subheader("Raw Data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'], name='Stock Open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'], name='Stock Close'))
    #add a range slide to the graph frame 
    fig.layout.update(title_text = 'Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#forecasting
df_train = data[['Date','Close']]
#format the columns to be compatible with prophet 
df_train = df_train.rename(columns={"Date":"ds","Close":"y"})

#declare Prophet model 
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader("Forecast Data")
st.write(forecast.tail())

st.write("Forecast Data Visualization")
fig1 =  plot_plotly(m,forecast)
st.plotly_chart(fig1)

st.write("Forecast Components")
fig2 = m.plot_components(forecast)
st.write(fig2)