import numpy as np
import tqdm
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

""" 
    Generating a population of 100,000 elements as a mixture of
    exponential and normal distributions
"""
np.random.seed(9)
exp=np.random.exponential(size=50000,scale=1)
normal=np.random.normal(loc=25,scale=5,size=50000)
population=np.concatenate((exp,normal),axis=0)
plt.hist(exp)
plt.hist(normal)
plt.legend(["Exponential","Normal"])
plt.show()
""" 
    Running the simulations by sampling with different sizes and
    different number of trials.
"""
sample_sizes=[1,100,150,200,250]
trials=[100,500,2000]
data={}
for s in tqdm.tqdm(sample_sizes):
    for t in trials:
        mean=[]
        for k in range(t):
            sample=np.random.choice(population,size=s,replace=True)
            mean.append(np.mean(sample))
        data[str(s)+'_'+str(t)]=mean

""" 
    Plotting the graphs using plotly
"""
plot=[]
steps = []
i=0
f=0
for s in sample_sizes:
    for t in trials:
        if f==0:
            plot.append(go.Histogram(x=data[str(s)+'_'+str(t)],visible=True,name="s="+str(s)+"\n"+"t="+str(t)))
            f=1
        else:
            plot.append(go.Histogram(x=data[str(s)+'_'+str(t)],visible=False,name="s="+str(s)+"\n"+"t="+str(t)))
        step = dict(
        method = 'restyle',  
        args = ['visible', [False] * len(data)],
        label= "s="+str(s)+","+"t="+str(t)
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)
        i=i+1
  
sliders = [dict(
    active = 0,
    pad = {"t": 50},
    steps = steps
)]
layout= go.Layout(height=300,width=300,autosize=True,title="Simulations",xaxis=dict(fixedrange=True),yaxis=dict(fixedrange=True))
layout["sliders"]=sliders

fig = dict(data=plot, layout=layout)

# py.plot(fig, filename='Central Limit Theorem',auto_open=True)