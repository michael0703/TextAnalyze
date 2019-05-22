
# coding: utf-8

# In[1]:


import re
import time
import io
import os
import json
import pandas as pd
from optparse import OptionParser
from pandas import DataFrame, read_csv
import pandas as pd


# In[2]:


df = pd.read_csv('./聯電2010-2011.csv', index_col=0)


# In[3]:


# df.index
df.columns


# In[4]:


from sklearn.decomposition import PCA
pca=PCA(n_components=2)
pca_data = pca.fit_transform(df.T.values)
type(pca_data)
pca_data


# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
x=[i[0] for i in pca_data]
y=[i[1] for i in pca_data]
import matplotlib.pyplot as plt
for i in range(len(pca_data)):
    plt.scatter(pca_data[i][0], pca_data[i][1], label=df.columns[i])
    plt.annotate('{}'.format(df.columns[i].split('.txt')[0]), xy=(pca_data[i][0],pca_data[i][1]))
# plt.legend(loc='upper right')#這個必須有，沒有你試試看
plt.xlim(min(y) - 0.05, max(x) + 0.05)
plt.ylim(min(y)-0.05, max(y) + 0.05)
plt.show()

