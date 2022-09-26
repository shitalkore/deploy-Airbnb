import streamlit as st

from pipeline import * 
def load_city():  
    with st.form("my_form"):
       # Every form must have a submit button.
       cities=['amsterdam', 'antwerp', 'asheville', 'athens', 'austin', 'bangkok',
              'barcelona', 'barossa-valley', 'barwon-south-west-vic', 'beijing',
              'belize', 'bergamo', 'berlin', 'bologna', 'bordeaux', 'boston',
              'bristol', 'broward-county', 'brussels', 'buenos-aires', 
              'cambridge', 'cape-town', 'chicago', 'clark-county-nv', 'columbus',
              'copenhagen', 'crete', 'dallas', 'denver', 'dublin', 'edinburgh',
              'euskadi', 'florence', 'fort-worth', 'geneva', 'ghent', 'girona']
       
       city=st.selectbox('Select City :',cities)
       submitted = st.form_submit_button("Submit")
       if submitted:
           from bs4 import BeautifulSoup
           import requests
           
           ##DataInterfaces
           url = "http://insideairbnb.com/get-the-data/"
           req = requests.get(url)
           soup = BeautifulSoup(req.text, "html.parser")
           links_scraped = []
           for link in soup.find_all('a'):
               if link.get('href') is not None:
                   links_scraped.append(link.get('href'))
           links_scraped = [x for x in links_scraped if 'csv' in x]
           city_name=city
           city = City(city_name, links_scraped)
           etl = ETL(city)
           etl.extract()
           etl.transform()
           etl.load()
           etl.export_data_interface(tofile=True)
           
           
           
           # #modelling
           import pickle
           data_interface_file=open(f'DataInterface_{city_name}.obj','rb')
           data_interface=pickle.load(data_interface_file)
           model_1=Model(data_interface,target='revenue')
           model_1.train()
           model_1.save_metrics()
           print(model_1.save())
           model_2=Model(data_interface,target='booking_rate')
           model_2.train()
           model_2.save_metrics()
           print(model_2.save())
           data_interface_file.close()
    
    
    
           #insights
           import pickle
           data_interface_file=open(f'DataInterface_{city_name}.obj','rb')
           data_interface=pickle.load(data_interface_file)
           insights=create_insights(data_interface)
           insight_engine=InsightEngine(data_interface,insights) 
           insight_engine.load_model()
           insight_engine.export()
           data_interface_file.close()
           
