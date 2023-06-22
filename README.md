# Education systems data analysis for market expansion
## Context

An EdTech start-up, which offers online training content for high school and university-level audiences, wants to expand internationally. The mission here is to determine, using education data from the World Bank (2010), the viability of the expansion project, as well as the countries to be favored.

- What are the countries with a strong potential of customers for our services?
- For each of these countries, what will be the evolution of this customer potential?
- In which countries should the company operate in priority?

Link to raw data : https://datacatalog.worldbank.org/search/dataset/0038480
To understand the data : https://datatopics.worldbank.org/education/

## Indicators
Before you begin, it's important to determine the ideal customer profile for this type of content. I therefore establish that the main target population is young (15 - 24 years old), wishes to continue their education in secondary and tertiary institutions, has access to internet and should experience an increase in the years to come. With these elements, and after a quick analysis of the data structure, I selected 5 relevant indicators to answer the problem :

- A demographic indicator, to know the proportion of young people (18 - 24 years) in a country

<img src="https://github.com/pgrondein/education_system_analysis/assets/113172845/632e02c2-c661-4467-bb48-7ed995add6ee" height="480">

- A demographic growth indicator, to evaluate the evolution of this young population
  
![young_pop_growth](https://github.com/pgrondein/education_system_analysis/assets/113172845/5f0a779c-5bd5-4a20-b9c2-2fa41243315d)
<img src="https://github.com/pgrondein/education_system_analysis/assets/113172845/5f0a779c-5bd5-4a20-b9c2-2fa41243315d" height="560">

- An indicator of internet users rate

![internet_users](https://github.com/pgrondein/education_system_analysis/assets/113172845/43a91e54-fad5-4948-82fd-61458fe9ad87)

- Two indicators for the enrollment rate in secondary and tertiary education

![secondary](https://github.com/pgrondein/education_system_analysis/assets/113172845/f7cb8027-bab5-488a-a214-25bb55dfcea7)

![tertiary](https://github.com/pgrondein/education_system_analysis/assets/113172845/28e785c6-0fb9-47a3-abcd-5b73a61db51b)

I also added a bonus indicator, linked to the income group.

![income](https://github.com/pgrondein/education_system_analysis/assets/113172845/0650f2fc-33ed-4f6d-ad85-19ebe8e19cbb)

## Points
Points are assigned to countries based on the value of indicators.
The points for each indicator are calculated as follow :
$(1 + ind/ind_M)$
with *ind* the value of the indicator and *ind_M* the maximum value of the same indicator.
An overall score is obtained by multiplying all the indicator points, and makes it possible to rank all the countries.

## Conclusion
![final](https://github.com/pgrondein/education_system_analysis/assets/113172845/8bcc46e0-06d4-45e0-9b30-18185f8d0b8f)

- Regions with high customer potential:
    - East Asia and Pacific: South Korea, New Zealand, Australia, Macao
    - Northern Europe: Iceland, Norway, Finland, Sweden
    - USA & Israel
- Evolution: each selected country (with the exception of Iceland) is experiencing positive population growth

![point_distrib](https://github.com/pgrondein/education_system_analysis/assets/113172845/892f8b5e-b580-46e9-9623-d335ac155c21)

If we look at the distribution of points in the final score, we see that the countries present in the top 10 all belong to the same income group (High income), and that the difference is mainly played on the proportion of internet users and secondary and tertiary enrollment rates.

In conclusion, the priority would be USA and Northern Europe.
