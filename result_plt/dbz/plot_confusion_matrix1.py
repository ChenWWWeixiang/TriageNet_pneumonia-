import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

data=np.load('/mnt/data9/Lipreading-DenseNet3D-master/re/pure_forest.npy')
y_pred=np.array(data[:,1:-1],np.float)
y_pred=np.argmax(y_pred,1)
y_true = np.array(data[:,-1],np.uint8)
sns.set()
#plt.figure()
f,ax=plt.subplots()
import csv
with open("go5.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(y_pred)
    writer.writerow(y_true)

C2= confusion_matrix(y_true, y_pred,labels=range(5),normalize='true')
print(C2) #
sns.heatmap(C2,annot=True,cmap='Blues',fmt=".2f")
maintype=['virus','fungus','bacteria','chlamydia','mycoplasma']
ax.set_title('Confusion Matrix')
ax.set_xlabel('Prediction')
ax.set_ylabel('Ground Truth')
for tick in ax.get_xticklabels():
    tick.set_rotation(60)
for tick in ax.get_yticklabels():
    tick.set_rotation(0)


plt.xticks(np.arange(5),maintype)
plt.yticks(np.arange(5),maintype)
plt.tight_layout()
plt.savefig('/mnt/data9/Lipreading-DenseNet3D-master/result_plt/dbz/cm_5.jpg')
plt.show()
