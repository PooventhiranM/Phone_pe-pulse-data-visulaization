import streamlit as st
import PIL 
from PIL import Image
import pandas as pd
import mysql.connector as mysql
import plotly.express as px

#with st.headbar:
# SELECT = option_menu(
#     menu_title = None,
#     options = ["About","Home","Top Charts","Explore Data","Contact"],
#     icons =["exclamation-circle","house","bar-chart","toggles","at"],
#     default_index=2,
#     orientation="horizontal",
#     styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
#         "icon": {"color": "black", "font-size": "20px"},
            
#         "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#         "nav-link-selected": {"background-color": "#6F36AD"}})

#Setting page configuration
icon = Image.open("C:/Users/poove/Downloads/phonepe-logo-icon.png")
st.set_page_config(page_title="Phonepe_pulse_data_visualisation | by Pooventhiran",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About':"# This app is created by pooven!..."}
                  )

st.header("Phonepe_pulse Data visualisation Project")
st.write("-------------")
tab1,tab2,tab3,tab4,tab5=st.tabs(["🏡Home","📊Top Charts","📈Explore Data","📝About","📞Contact"])

# CONNECTING WITH MYSQL DATABASE
mydb=mysql.connect(host="localhost",
                   user="root",
                   password="Pooventhiran2",
                   port="3306")
mycursor=mydb.cursor(buffered=True)

mycursor.execute("CREATE DATABASE if not exists phonepe_data")
mycursor.execute("USE phonepe_data")

# Webpage creation
#----------------Home----------------------#

with tab1:
    col1,col2, = st.columns(2)
    col1.image(Image.open("C:/Users/poove/Downloads/about_phonepe2.png"),width = 409)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:/Users/poove/Downloads/upi.mp4")

#----------------TOP CHARTS----------------------#

with tab2:
    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.8],gap="medium")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
        
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍")
            
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
            
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from Arg_transactions where Year = {Year} and Quarter = {Quarter} group by State order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',names='State',
                            title='Top 10',color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
                
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select District , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total from Map_transactions where Year = {Year} and Quarter = {Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',names='District',title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
                                
    # Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3 = st.columns([2,2,2],gap="medium")
            
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select Brands, sum(Users_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from Arg_users where Year = {Year} and Quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,title='Top 10',x="Total_Users",y="Brand",
                            orientation='h',color='Avg_Percentage',color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
        
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select District, sum(Registered_Users) as Total_Users, sum(App_Open_count) as Total_Appopens from Map_users where Year = {Year} and Quarter = {Quarter} group by District order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,title='Top 10',x="Total_Users",y="District",
                        orientation='h',color='Total_Users',color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
                
                
        with col3:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select State, sum(Registered_users) as Total_Users, sum(App_Open_count) as Total_Appopens from Map_users where Year = {Year} and Quarter = {Quarter} group by State order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',names='State',title='Top 10',color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Appopens'],labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

#----------------EXPLORE DATA----------------------# 

with tab3:
    # MENU 3 - EXPLORE DATA
    Type1 = st.selectbox("**Type**", ("Transactions ", "Users "))
    Year1 = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter1 = st.slider("**Quarter**", min_value=1, max_value=4)
    col1,col2 = st.columns(2)
        
    # EXPLORE DATA - TRANSACTIONS
    if Type1 == "Transactions ":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select State, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Map_transactions where Year = {Year1} and Quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:/Users/poove/Downloads/Statenames.csv")
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select State, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Map_transactions where Year = {Year1} and Quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:/Users/poove/Downloads/Statenames.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
                
    # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Arg_transactions where year= {Year1} and Quarter = {Quarter1} group by Transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
    # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,Year,Quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Map_transactions where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
    #EXPLORE DATA - USERS      
    if Type1 == "Users ":
        
        # Overall State Data - TOTAL USERS - INDIA MAP
        with col1:
            st.markdown("## :violet[Overall State Data - User App opening frequency]")
            mycursor.execute(f"select State, sum(Registered_users) as Total_Users, sum(App_open_count) as Total_Appopens from Map_users where Year = {Year1} and Quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            df2 = pd.read_csv("C:/Users/poove/Downloads/Statenames.csv")
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Users',
                        color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig,use_container_width=True)

        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        with col2:
            if Year1 == 2018:
                st.markdown("#### Sorry No Data to Display for 2018")
            elif Year1 == 2019 and Quarter1==1:
                st.markdown("#### Sorry No Data to Display for 2019 qtr 1")
            else:
                st.markdown("## :violet[Overall State Data - User App opening frequency]")
                mycursor.execute(f"select State, sum(Registered_users) as Total_Users, sum(App_open_count) as Total_Appopens from Map_users where Year = {Year1} and Quarter = {Quarter1} group by State order by State")
                df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                df2 = pd.read_csv("C:/Users/poove/Downloads/Statenames.csv")
                df1.Total_Appopens = df1.Total_Appopens.astype(float)
                df1.State = df2
                
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='sunset')

                fig.update_geos(fitbounds="locations", visible=True)
                st.plotly_chart(fig,use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,Year,Quarter,District,sum(Registered_users) as Total_Users, sum(App_open_count) as Total_Appopens from Map_users where Year = {Year1} and Quarter = {Quarter1} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','Year', 'Quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
    
#----------------About-----------------------#

with tab4:
    col1,col2 = st.columns(2)
    with col1:
        st.video("C:/Users/poove/Downloads/pulse-video (1).mp4")
    with col2:
        st.image(Image.open("C:/Users/poove/Downloads/about_phonepe2.png"),width = 409)
    st.write("----------------")
    st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    st.title("THE BEAT OF PHONEPE")
    st.write("---------------------")
    st.subheader("Phonepe became a leading digital payments company")
    st.write("")
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("C:/Users/poove/Downloads/phonepe_image.png"),width = 340)
        with open("C:/Users/poove/Downloads/about_phonepe1.png","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(Image.open("C:/Users/poove/Downloads/about_phonepe1.png"),width = 600)

#----------------------Contact---------------#

with tab5:
    Name = (f'{"Name :"}  {"Poovethiran M"}')
    mail = (f'{"Mail :"}  {"Pooventhiranmurukesan@gmail.com"}')
    social_media = {
        "GITHUB": "https://github.com/PooventhiranM/Phone_pe-pulse-data-visulaization.git",
        "LINKEDIN": "https://www.linkedin.com/in/pooventhiranmurukesan/"}
    
    col1, col2, col3 = st.columns(3)
    col3.image(Image.open("C:/Users/poove/OneDrive/Desktop/My documents/Pooven.jpg"), width=300)

    with col1:
        st.title('Phonepe Pulse data visualisation')
        st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        st.subheader(Name)
        st.subheader("An Aspiring DATA-SCIENTIST..!")
        st.subheader(mail)     
    st.write("#")
    with col3:
        st.write("#")
        st.write("#")
        st.write("#")
        st.write("#")
        for index, (platform, link) in enumerate(social_media.items()):
            st.write(f"[{platform}]({link})")