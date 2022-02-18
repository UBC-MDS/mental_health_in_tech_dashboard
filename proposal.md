# 1. Motivation and purpose (Jordan)

Our role: Data scientist consultancy firm

Target audience: New graduating student seeking job in tech

- Mental health is important and ....working capability...
- 


https://www.kaggle.com/osmi/mental-health-in-tech-survey



# 2. Description of the data (Hatef)
In this dashboard, we will be visualizing a dataset of approximately 1300 responses from a 2014 survery measuring the attitude towards mental health in tech sector and the number of disorders in the workplace. Each row of the dataset has 27 associate variables such as `gender`, `age', `country`, `state`, `family_history`, treatment`, `no_employees` etc. In this project, we will only focus on a subset of variables for visualization which are `age', `gender', `no_employees`, `country', `state`, `benefits`, and `obs_consequence` as a target variable. `age', `gender` are the employees' specific information. `country`, `state` show where the eomployee lives. `no_employees` shows the size of the company and will be inluded in the dashboard as a slider for the user to change the size of company and correlates that with the mental health disorders. `benefits` feature shows whether the employres provides the mental health benefits for their employees (we use a pie chart to show what percentage of employers provides such a benefit). Our target variable would be `obs_consequence` which only has two values: "yes" and "no". "yes" indicates someone has already heard or observed negative consequences for coworkers with mental health conditions in the workplace, and the response is "no" otherwise. We will visulize the `obs_consequence` using a pie chart and show how the distribution of that varies across different states. 


# 3. Research questions you are exploring (Lisheng)

- How does the frequency of mental health illness and attitudes towards mental health vary by geographic location?
- What are the strongest predictors of mental health illness or certain attitudes towards mental health in the workplace?
