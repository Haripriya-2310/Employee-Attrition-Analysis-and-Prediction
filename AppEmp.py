import streamlit as st   
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import pickle

with open("pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f) 
with open("label_encoders.pkl", "rb") as f: 
    saved_encoders = pickle.load(f)


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

    df = pd.read_csv(r'C:\Users\harip\Downloads\GUVI DS\cleaned_data.csv')

    st.title("Employee Metric 📊")
    st.markdown("**Quick overview of workforce size, attrition trends.**")

    col1, col2 = st.columns(2)
    col1.metric("👥 Total Employees", len(df))
    col2.metric("🔻 Attrition Rate", f"{round(df['Attrition'].mean()*100, 2)}%")

elif menu == "Employee Overview🧑‍💼":
    st.header("Employee Overview🧑")
    
    df = pd.read_csv(r'C:/Users/harip/Downloads/GUVI DS/cleaned_emp_data.csv')
    st.write(df.head())

 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### High-Risk Employees ⚠️")
        high_risk = df[df['Attrition'] > 0.7][['Age', 'TotalWorkingYears', 'Attrition']]
        st.dataframe(high_risk, use_container_width=True)

        # Plotting
        fig, ax = plt.subplots()
        sns.scatterplot(data=high_risk,x="Age",y="Attrition",hue="TotalWorkingYears",ax=ax)
        ax.set_title("Age vs Attrition (High-Risk Employees)")
        st.pyplot(fig)

    with col2:
        st.markdown("### High Job Satisfaction 👍")
        high_satisfaction = df[df['JobSatisfaction'] >= 4][['JobLevel', 'JobSatisfaction', 'Attrition']]
        st.dataframe(high_satisfaction, use_container_width=True)

        # Plotting
        fig, ax = plt.subplots()
        sns.barplot(data=high_satisfaction,x="JobLevel", y="JobSatisfaction", hue="Attrition",ax=ax, palette='muted')
        ax.set_title("Job Level vs Job Satisfaction (High Satisfaction Group)")
        st.pyplot(fig)

    with col3:
        st.markdown("### High Performance Score ⭐")
        high_perf = df[df['PerformanceRating'] >= 4][['JobRole','PerformanceRating','MonthlyIncome','YearsAtCompany']]
        st.dataframe(high_perf, use_container_width=True)

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
            age = st.number_input("Age", min_value=18, max_value=60, step=1)
            job_satisfaction = st.number_input("Job Satisfaction (1–4)", min_value=1, max_value=4, step=1)
            monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=50000, step=500)
            years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, step=1)
            environment_sat = st.number_input("Environment Satisfaction (1–4)", min_value=1, max_value=4, step=1)
            job_involvement = st.number_input("Job Involvement (1–4)", min_value=1, max_value=4, step=1)
            total_years = st.number_input("Total Working Years", min_value=0, max_value=40, step=1)
            years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=20, step=1)

        with col2:
            years_with_curr_manager = st.number_input("Years with Current Manager", min_value=0, max_value=20, step=1)
            performance_boost = st.number_input("Performance Boost", min_value=0, max_value=10, step=1)
            stability = st.number_input("Stability Score", min_value=0, max_value=10, step=1)
            engagement = st.number_input("Engagement Score", min_value=0, max_value=10, step=1)
            distance_from_home = st.number_input("Distance From Home", min_value=0, max_value=50, step=1)
            job_level = st.number_input("Job Level", min_value=1, max_value=5, step=1)
            stock_option_level = st.number_input("Stock Option Level", min_value=0, max_value=3, step=1)
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            marital_map = {"Single": 0, "Married": 1, "Divorced": 2}
    
        with col3:
            overtime = st.selectbox("OverTime", ["Yes", "No"])
            overtime_enc = 1 if overtime == "Yes" else 0
            gender = st.selectbox("Gender", ["Male", "Female"])
            gender_enc = 1 if gender == "Male" else 0

            # columns were Label Encoded during training
            business_travel = st.selectbox("Business Travel", saved_encoders["BusinessTravel"].classes_)
            department = st.selectbox("Department", saved_encoders["Department"].classes_)
            education = st.selectbox("Education Field", saved_encoders["EducationField"].classes_)
            jobrole = st.selectbox("Job Role", saved_encoders["JobRole"].classes_)
            tenure = st.selectbox("Tenure Category", saved_encoders["TenureCategory"].classes_)

            submitted = st.form_submit_button("Predict Attrition")

    if submitted:
        department_enc = saved_encoders["Department"].transform([department])[0]
        marital_map = {"Single": 0, "Married": 1, "Divorced": 2}
        marital_enc = marital_map[marital_status]
        overtime_enc = 1 if overtime == "Yes" else 0
        travel_enc = saved_encoders["BusinessTravel"].transform([business_travel])[0]
        education_enc = saved_encoders["EducationField"].transform([education])[0]
        gender_enc = 1 if gender == "Male" else 0
        jobrole_enc = saved_encoders["JobRole"].transform([jobrole])[0]
        tenure_enc = saved_encoders["TenureCategory"].transform([tenure])[0]


        input_df = pd.DataFrame([{
            "Age": age,
            "JobSatisfaction": job_satisfaction,
            "MonthlyIncome": monthly_income,
            "YearsAtCompany": years_at_company,
            "EnvironmentSatisfaction": environment_sat,
            "JobInvolvement": job_involvement,
            "TotalWorkingYears": total_years,
            "YearsInCurrentRole": years_in_current_role,
            "YearsWithCurrManager": years_with_curr_manager,
            "PerformanceBoost": performance_boost,
            "StabilityScore": stability,
            "EngagementScore": engagement,
            "DistanceFromHome": distance_from_home,
            "JobLevel": job_level,
            "StockOptionLevel": stock_option_level,
            "MaritalStatus": marital_enc,
            "OverTime": overtime_enc,
            "Gender": gender_enc,
            "BusinessTravel": travel_enc,
            "Department": department_enc,
            "EducationField": education_enc,
            "JobRole": jobrole_enc,
            "TenureCategory": tenure_enc
        }])
        
        # Predict
        prediction = pipeline.predict(input_df)
        prob = pipeline.predict_proba(input_df)[0][1]
        if prediction == 1:
            st.error(f"🔴 The employee is **likely to leave**({prob:.2f}%)")
        else:
            st.success(f"🟢 The employee is **likely to stay**({100 - prob:.2f}%)")