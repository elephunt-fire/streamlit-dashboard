import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
#warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Sample SuperStore EDA")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
try:
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))

    if fl is not None:
        df = pd.read_csv(fl, encoding="ISO-8859-1")
        st.write(fl.name)
        st.write(df)



    col1 , col2 = st.columns(2)
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    startDate = pd.to_datetime(df['Order Date']).min()
    endDate = pd.to_datetime(df['Order Date']).max()
    with col1:
        date1 = pd.to_datetime(st.date_input('Start Date' , startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input('End Date ' , endDate))

    df = df[(df['Order Date']>= date1) & (df['Order Date']<=date2)].copy()

    st.sidebar.header('Choose your filter : ')
    # Region Filter
    region = st.sidebar.multiselect('Pick your Region' , df['Region'].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df['Region'].isin(region)]

    # State Filter
    state = st.sidebar.multiselect('Pick your state' , df2['State'].unique())
    if not state:
        df3=df2.copy()
    else:
        df3 = df2[df2['State'].isin(state)]

    # City Filter
    city  = st.sidebar.multiselect('Pick your city' ,df3['City'].unique())

    # Filtering Based on the region ,state, city

    if not region and not state and not city :
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df['Region'].isin(region)]
    elif not region and not city:
        filtered_df = df[df['State'].isin(state)]

    elif state and city :
        filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]
    elif region and city:
        filtered_df = df3[df['Region'].isin(region) & df['City'].isin(city)]
    elif region and state:
        filtered_df = df3[df['Region'].isin(region) &  df['State'].isin(state)]
    elif city:
        filtered_df = df3[df['City'].isin(city)]
    else:
        filtered_df = df3[df3['Region'].isin(region) & df['State'].isin(state) & df3['City'].isin(city) ]

    # Forming a Bar chart and Pie Chart

    category_df= filtered_df.groupby(by = ['Category'] , as_index= False)['Sales'].sum()
    col1 , col2  = st.columns(2)
    with col1 :
        st.subheader('Category wise Sales')
        fig = px.bar(category_df, x = 'Category' , y = 'Sales'
                     , text = ['${:,.2f}'.format(x) for x in category_df['Sales']])
        st.plotly_chart(fig , use_container_width= True , height = 200)

    with col2 :
        st.subheader('Region wise Sales')
        fig = px.pie(filtered_df , values = 'Sales' , names= 'Region', hole = 0.5)
        fig.update_traces(text = filtered_df['Region'],textposition = 'outside')
        st.plotly_chart(fig , use_container_width=True)

    # To be able to downloading the Bar Chart and Pie Chart
    col1 , col2 = st.columns(2)
    with col1:
        with st.expander('Category ViewDate'):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index= False).encode('utf-8')
            st.download_button('Download Data', data = csv, file_name = 'Category.csv'
                               ,mime = 'text/csv' , help='Click here to download a CSV file')

    with col2:
        with st.expander('Region ViewDate'):
            region = filtered_df.groupby(by ='Region', as_index= False)['Sales'].sum()
            st.write(region.style.background_gradient(cmap='Oranges'))
            csv = region.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='region.csv'
                               , mime='text/csv', help='Click here to download a CSV file')

    # For Time Data Analysis
    filtered_df['month_year']= filtered_df['Order Date'].dt.to_period('M')
    st.subheader(':chart: Time Series Analysis')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y:%b'))['Sales'].sum()).reset_index()
    fig2 = px.line(linechart , x = 'month_year' , y = 'Sales' , labels= {'Sales': 'Amount', 'month_year':'Year:Month'}, height= 500, width = 1000, template='gridon')
    st.plotly_chart(fig2, use_container_width= True)

    with st.expander('View Data of TimeSeries'):
        st.write(linechart.T.style.background_gradient(cmap= 'Blues'))
        csv= linechart.to_csv(index= False ).encode('utf-8')
        st.download_button('Download Data' , data = csv, file_name= 'TiemSeries.csv' , mime= 'text/csv')


    # Create a tree based on Region , Category and Suub-category
    st.subheader('Hierarchical View of Sales using TreeMap')
    fig3 = px.treemap(filtered_df, path =['Region' , 'Category' , 'Sub-Category'] , values = 'Sales' , hover_data= ['Sales'] , color= 'Sub-Category')
    fig3.update_layout(width  = 800 , height = 650)
    st.plotly_chart(fig3 , use_container_width=True)

    # Pie chart Segment wise Sales and Category wise Sales
    chart1, chart2 = st.columns(2)
    with chart1 :
        st.subheader('Segment wise Sales')
        fig = px.pie(filtered_df , values= 'Sales' , names='Segment' , template='plotly_dark')
        fig.update_traces(text = filtered_df['Segment'] , textposition = 'inside')
        st.plotly_chart(fig , use_container_width= True)

    with chart2:
        st.subheader('Category wise Sales')
        fig = px.pie(filtered_df , values= 'Sales' , names= 'Category', template='gridon')
        fig.update_traces(text = filtered_df['Category'],textposition = 'inside' )
        st.plotly_chart(fig,use_container_width=True )

    import plotly.figure_factory as ff
    st.subheader(':point_right: Month wise Sub-Category Sales Summary')
    with st.expander('Summary_Table'):
        df_sample = df[0:5][['Region' , 'State', 'City' , 'Category' , 'Sales' , 'Profit' , 'Quantity']]
        fig = ff.create_table(df_sample, colorscale='Cividis')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('Month wise Sub-Category Table')
        filtered_df['month']  = filtered_df['Order Date'].dt.month_name()
        sub_category_year = pd.pivot_table(data = filtered_df , values='Sales' , index = ['Sub-Category'] , columns='month')

    # Create a scatter plot
    date1 = px.scatter(filtered_df , x = 'Sales' , y = 'Profit' , size = 'Quantity')
    date1['layout'].update(title = 'Relationship between Sales and Profit using Scatter Plot',
                           titlefont = dict(size = 20) , xaxis = dict(title = 'Sales', titlefont = dict(size=19)),
                           yaxis = dict(title = 'Profit' , titlefont= dict(size= 19)))
    st.plotly_chart(date1 , use_container_width=True)

    with st.expander('View Data'):
        st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap = 'Oranges'))

    # Download Original Dataset
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data' , data= csv , file_name='Data.csv' , mime = 'text/csv')

except Exception as e:
    st.error(f"An error occurred: {str(e)}  \n Please upload valid file.")