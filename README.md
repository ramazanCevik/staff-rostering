# Staff Rostering
Salman et. al. (2014) stated that since call arrival rates change by months, weeks, days and
even in different hours throughout a day, call centers must deal with a dynamic demand pattern
(p.41). Their aim was to produce a mathematical model to produce workable and effective labor
plans than can achieve the management’s objectives and future goals. Call centers are important in
many areas and providing them correctly is crucial for some sectors. In this study, it is stated that
the sectors that have difficulties with call centers and express this, banking and providing global
technical support are examined. There are multi-skill environments with different skill structures
in these two sectors. Staff preference is also important, in addition to these, service level is also
important. To define the service level, the "percentage of calls answered within a specific time
limit, or even 80% of calls in less than 20s, is used as the service level criterion.

## Model
The problem is formulated by the authors as such (refer to the paper for further information):

![image](https://github.com/ramazanCevik/staff-rostering/assets/48220006/cc187094-2f68-43c4-a143-56ad2c613132)

The article performs a very detailed analysis. Some parts of these analysis include the checking
over the collected data and different prior costs. Therefore, there were no need to do the same. To
achieve similar observational data, we studied to how to generate near-real data. The other major
challenge was the difference of our scale from the article. We did not have the same computer
environment to run the model with same scale of article. So, we lowered the number of agents,
available seat capacity and planning horizon. It will not create a problem if our implementation is
used for the staff rostering problem because we built the model such that the solver modules’ input
depends on all the parameters. In other words, in theory, our implementation can directly solve the
article’s problem and even larger scale, assuming the input is given with the JSON format specified.<br>
• Number of agents: We used 8 agents. Also, we run an instance with 20 agents. Since it takes too
much time, we continued with 8.<br>
• Seat Capacity: We used 5 seat capacity. Also, we run an instance with 15 seat capacity.<br>
• Planning Horizon: We used two-week planning horizon because of the reasons specified earlier.<br>
• Geographical Regions: We used 3 geographical locations.<br>
• Time Intervals: We used 24-time interval for a given day.<br>
• Costs: We generated costs using Uniform distributions whose parameters can be found in the data
generation code, we mostly set lower and upper bound limits of uniform distribution as given
intervals of the article.<br>
• Assignments, Binary parameters: We generated binary variables using Bernoulli distribution.<br>
• Set of skills: We used three different skills.<br>
• Set of vehicles: We used two vehicles.<br>
• Other parameters (β, θ, …): We used reasonable numbers which estimated from the article.<br>
• Shifts: We used the same shift structure with the article to achieve consistency.<br>
Because it is a showcase, we limited our number of decision variables with low numbers which
can be easily increased with a real-world data without changing our model implementation module.<br>

## Analysis

With changing the underage cost, we created a table for performance analysis. We used UV%,
OS%, UR% and DL% for our performance analysis and we calculated the objective value as
represented in total cost.<br>

![image](https://github.com/ramazanCevik/staff-rostering/assets/48220006/62e4917e-857e-4285-b914-fb2d09e3ec28)

Also, we did a performance analysis with considering γ<sub>max</sub> upper bound:<br>

![image](https://github.com/ramazanCevik/staff-rostering/assets/48220006/8b86af35-9d17-4edf-ba05-3e9d44d9745e)

Our 3-step work; model implementation, data generation, and analysis were consistent with the
article. A minor difference was caused by data generation part because it is very hard to find the
appropriate random data that fits with the article’s results. Considering the problem caused by the
data, the interpretation of the analysis part was speculative. So, we decided to focus on implementing
the right model and making it scalable and easy to run with different instances. Also, analysis part
is included in the codes and the application gives analyses as outputs.

## References
Örmeci, E. & Salman, F. & Yücel, Eda. (2014). Staff rostering in call centers providing employee transportation. Omega. 43. 41–53. 10.1016/j.omega.2013.06.003. 
