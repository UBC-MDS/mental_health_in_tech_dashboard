# 1. Motivation and purpose (Jordan)

Our role: Data scientist consultancy firm

Target audience: Both tech employers and employees

Even today, both employers and employees are more likely to acknowledge physical health conditions than mental health conditions. While some employers are ahead of the curve in terms of acknowledging the importance of employee mental health, there are many workplaces where employees still do not get the support that they need. For employers, this can lead to high employee turnover as well as lower quality work. For employees, this can lead to further deteriorating mental health. To address these challenges, we propose building a web dashboard that visually illustrates the current state of mental health in tech. Our app will allow employers to explore how different variables relate to the mental health of employees, as well as give employees insight into how their workplace compares to other workplaces in various aspects of mental health.

# 2. Description of the data 
In this dashboard, we will be visualizing a dataset of approximately 1300 responses from a 2014 survery measuring the attitude towards mental health in tech sector and the number of disorders in the workplace. Each row of the dataset has 27 associate variables such as `gender`, `age', `country`, `state`, `family_history`, treatment`, `no_employees` etc. In this project, we will only focus on a subset of variables for visualization which are `age', `gender', `no_employees`, `country', `state`, `benefits`, and `obs_consequence` as a target variable. `age', `gender` are the employees' specific information. `country`, `state` show where the eomployee lives. `no_employees` shows the size of the company and will be inluded in the dashboard as a slider for the user to change the size of company and correlates that with the mental health disorders. `benefits` feature shows whether the employres provides the mental health benefits for their employees (we use a pie chart to show what percentage of employers provides such a benefit). Our target variable would be `obs_consequence` which only has two values: "yes" and "no". "yes" indicates someone has already heard or observed negative consequences for coworkers with mental health conditions in the workplace, and the response is "no" otherwise. We will visulize the `obs_consequence` using a pie chart and show how the distribution of that varies across different states. 


https://www.kaggle.com/osmi/mental-health-in-tech-survey

# 3. Research questions you are exploring (Lisheng)

- How does the frequency of mental health illness and attitudes towards mental health vary by geographic location?
- What are the strongest predictors of mental health illness or certain attitudes towards mental health in the workplace?
