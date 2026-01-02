import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import pickle


with open("preprocess_att.pkl", "rb") as f:
    preprocess = pickle.load(f)
with open("rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

# Page Configuration
st.set_page_config(page_title="Employee Attrition Analysis and Prediction", layout="wide")

#Background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.clearpeaks.com/wp-content/uploads/2019/05/Advanced-analytics-Employee-Attrition-1200-630.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.title("Employee Attrition Prediction Dashboard")

# Sidebar Menu
menu = st.sidebar.selectbox("Explore🔍", ["Home🏛️","Employee Overview🧑‍💼","Employee Attrition Prediction📉"])

if menu == "Home🏛️":
    st.markdown("**Analyze attrition trends, identify at-risk employees, and drive retention strategies.**")
    
    st.markdown("""
    <h2 style='font-weight: 900'>
    Welcome
    </h2>""", unsafe_allow_html=True)

    
    st.markdown(""" 
    <div class="home-card">
        <p><b>This dashboard helps HR teams:</b></p>
            <ul>
                <li><b>🔎 Identify at-risk employees</b></li>
                <li><b>📈 Predict attrition</b></li>
                <li><b>📊 Analyze workforce patterns</b></li>
            </ul>
    </div>""", unsafe_allow_html=True)

    df = pd.read_csv(r'C:/Users/harip/Downloads/GUVI DS/cleaned_empl_data.csv')

    st.title("Employee Metric 📊")
    st.markdown("**Quick overview of workforce size, attrition trends.**")

    col1, col2 = st.columns(2)
    col1.metric("👥 Total Employees", len(df))
    col2.metric("🔻 Attrition Rate", f"{round(df['Attrition'].mean()*100, 2)}%")

elif menu == "Employee Overview🧑‍💼":
    st.header("Employee Overview🧑")
    
    df = pd.read_csv(r'C:/Users/harip/Downloads/GUVI DS/cleaned_empl_data.csv')
    st.write(df.head())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### High-Risk Employees ⚠️")
        high_risk = df[df['Attrition'] > 0.7][['Age', 'TotalWorkingYears', 'Attrition']]

        # Plotting
        fig, ax = plt.subplots()
        sns.scatterplot(data=high_risk,x="Age",y="Attrition",hue="TotalWorkingYears",ax=ax)
        ax.set_title("Age vs Attrition (High-Risk Employees)")
        st.pyplot(fig)

    with col2:
        st.markdown("###  High Job Satisfaction😊")

        high_satisfaction = df[df['JobSatisfaction'] == 4]

        fig, ax = plt.subplots()
        sns.countplot(
            data=high_satisfaction,
            x="JobLevel",
            hue="Attrition",
            ax=ax
        )

        ax.set_title("Attrition Count by Job Level (High Job Satisfaction)")
        ax.set_xlabel("Job Level")
        ax.set_ylabel("Employee Count")

        st.pyplot(fig)

    with col3:
        st.markdown("### High Performance Score ⭐")
        high_perf = df[df['PerformanceRating'] >= 4][['JobRole','PerformanceRating','MonthlyIncome','YearsAtCompany']]

        # Plotting
        fig, ax = plt.subplots()
        sns.scatterplot(data=high_perf,x="YearsAtCompany",y="MonthlyIncome",hue="PerformanceRating",ax=ax, palette='Set1')         
        ax.set_title("Years at Company vs Monthly Income (High Performers)")
        st.pyplot(fig)


# Attrition Prediction 

if menu == "Employee Attrition Prediction📉":
    st.header("Employee Attrition Prediction")

    with st.form("attrition_form"): 
        col1, col2, col3 = st.columns(3)

        with col1:
            Age = st.number_input("Age", 18, 60, 30)
            Gender = st.selectbox("Gender", ["Male", "Female"])
            MaritalStatus = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])

            Education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
            EducationField = st.selectbox(
                "Education Field",
                ["Life Sciences", "Medical", "Marketing",
                "Technical Degree", "Human Resources", "Other"])
            Department = st.selectbox(
                "Department",
                ["Sales", "Research & Development", "Human Resources"])
            JobRole = st.selectbox(
                "Job Role",
                ["Sales Executive", "Research Scientist", "Laboratory Technician",
                "Manufacturing Director", "Healthcare Representative",
                "Manager", "Sales Representative", "Research Director",
                "Human Resources"])
            JobLevel = st.selectbox("Job Level", [1, 2, 3, 4, 5])

        with col2:
            
            BusinessTravel = st.selectbox(
                "Business Travel",
                ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
            OverTime = st.selectbox("Over Time", ["Yes", "No"])
            StockOptionLevel = st.selectbox("Stock Option Level", [0, 1, 2, 3])
            JobInvolvement = st.selectbox("Job Involvement", [1, 2, 3, 4])
            DistanceFromHome = st.number_input("Distance From Home", 1, 100, 10)
            MonthlyIncome = st.number_input("Monthly Income", 1000, 50000, 5000)
            PercentSalaryHike = st.slider("Percent Salary Hike", 10, 25, 15)

        with col3:

            TotalWorkingYears = st.number_input("Total Working Years", 0, 40, 8)
            NumCompaniesWorked = st.number_input("Companies Worked", 0, 10, 2)
            YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", 0, 20, 1)
            TrainingTimesLastYear = st.selectbox("Training Times Last Year", [0,1,2,3,4,5,6])
            EngagementScore = st.number_input(
                "Engagement Score",
                min_value=1.0,
                max_value=4.0,
                value=2.75,
                step=0.25
            )
            StabilityScore = st.number_input(
                "Stability Score",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1
            )
            JobInvolvement = st.selectbox(
                "Job Involvement",
                [1, 2, 3, 4],
                key="job_involvement")
            PerformanceRating = st.selectbox("Performance Rating", [3, 4])
            submit = st.form_submit_button("🔍 Predict Attrition")

    if submit:

        input_df = pd.DataFrame([{
                'Age': Age,
                'Gender': Gender,
                'MaritalStatus': MaritalStatus,
                'Education': Education,
                'EducationField': EducationField,
                'Department': Department,
                'JobRole': JobRole,
                'JobLevel': JobLevel,
                'BusinessTravel': BusinessTravel,
                'DistanceFromHome': DistanceFromHome,
                'OverTime': OverTime,
                'MonthlyIncome': MonthlyIncome,
                'PercentSalaryHike': PercentSalaryHike,          
                'StockOptionLevel': StockOptionLevel,
                'TotalWorkingYears': TotalWorkingYears,
                'NumCompaniesWorked': NumCompaniesWorked,
                'YearsSinceLastPromotion': YearsSinceLastPromotion,
                'TrainingTimesLastYear': TrainingTimesLastYear,
                'EngagementScore' : EngagementScore,
                'StabilityScore': StabilityScore,
                'JobInvolvement': JobInvolvement,               
                'PerformanceRating': PerformanceRating,
                
    }])

        # Encode input
        input_enc = preprocess.transform(input_df)  

        # Predict probability for class 1
        prob = rf_model.predict_proba(input_enc)[0][1]

        # Apply threshold
        threshold = 0.39
        prediction = 1 if prob > threshold else 0

        # Display result
        if prediction == 1:
            st.error(f"🔴 The employee is **likely to leave** ({prob*100:.2f}%)")
        else:
            st.success(f"🟢 The employee is **likely to stay** ({(1-prob)*100:.2f}%)")