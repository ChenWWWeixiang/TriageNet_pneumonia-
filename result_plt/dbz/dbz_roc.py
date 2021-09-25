##plot 3cls roc
import seaborn as sns
import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn.metrics as metric
from sklearn.calibration import calibration_curve
from sklearn.preprocessing import label_binarize
import pandas as pd
def get_CI(value,res,xx=False):
    sorted_scores=np.array(value)
    sorted_scores.sort()
    confidence_lower = sorted_scores[int(0.05 * len(sorted_scores))].round(3)
    confidence_upper = sorted_scores[int(0.95 * len(sorted_scores))].round(3)
    if xx:
        res.append(np.mean(value).round(3))
    else:
        v=((confidence_upper-confidence_lower)/2).round(3)
        res.append(str(np.mean(value).round(3)) + '+-' + str(v))
    return res
import argparse
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
import  pandas as pd
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--ress", help="A list of npy files which record the performance.",
                    default=['/mnt/data9/Lipreading-DenseNet3D-master/re/pure_forest.npy',
                    ])
parser.add_argument("-o", "--output_file", help="Output file path", type=str,
                    default='/mnt/data9/Lipreading-DenseNet3D-master/result_plt/dbz/dfn5_new.csv')
args = parser.parse_args()

#res=np.load('ipt_results/results/train.npy')
if isinstance(args.ress,str):
    ress=eval(args.ress)
else:
    ress=args.ress
CLS=['virus','fungus','bacteria','chlamydia','mycoplasma']
plt.figure()
axes = plt.subplot(111)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves of Distinguishing level-I using DFN')

all_record=[]
with open(args.output_file,'w') as f:
    f=csv.writer(f)
    f.writerow(['name', 'AUC','Sensitivity','Specificity'])
    for a_res in ress:
        res = np.load(a_res)
        pre = np.array(res[:, 1:-1], np.float)
        gt = np.array(res[:, -1], np.float)
        #AUC=[]
        #pre=pre/pre.sum(1,keepdims=True)
        ACC=[]
        REC=[]
        SPE=[]
        SAUC=[]
        AUC=[]
        SEN2=[]
        y_one_hot = label_binarize(gt, np.arange(5))
        norm_x=pre
        for i in range(100):
            train_x, test_x, train_y, test_y = train_test_split(pre, y_one_hot, test_size=0.2)
            #train_x=train_x/train_x.max(axis=0)
            auc = metric.roc_auc_score(train_y, train_x, average='micro')
            AUC.append(auc)

            prediction = np.argmax(train_x, 1)
            groundtruth = np.argmax(train_y, 1)
            pre2=np.argsort(-train_x,-1)[:,1]
            ACC.append(np.mean(prediction == groundtruth))
            sen = []
            spe = []
            sauc = []
            sen2=[]
            for cls in range(5):
                sen2.append(np.sum((pre2 == cls) * (groundtruth == cls)) / np.sum(groundtruth == cls)+np.sum((prediction == cls) * (groundtruth == cls)) / np.sum(groundtruth == cls))
                sen.append(np.sum((prediction == cls) * (groundtruth == cls)) / np.sum(groundtruth == cls))
                spe.append(np.sum((prediction != cls) * (groundtruth != cls)) / np.sum(groundtruth != cls))
                sauc.append(metric.roc_auc_score(train_y[:,cls], train_x[:,cls]))
            SAUC.append(sauc)
            REC.append(sen)
            SPE.append(spe)
            SEN2.append(sen2)
        SPE = np.array(SPE)
        REC = np.array(REC)
        SEN2 = np.array(SEN2)
        SAUC = np.array(SAUC)
        for cls in range(5):
            Res=[CLS[cls]]
            Res = get_CI(SAUC[:, cls], Res)
            Res = get_CI(REC[:, cls], Res)
            Res = get_CI(SPE[:, cls], Res)
            Res = get_CI(SEN2[:, cls], Res)
            f.writerow(Res)
        Res=['all']
        Res=get_CI(AUC,Res)
        Res = get_CI(ACC, Res)
        f.writerow(Res)
       # plt.figure(1)
        #fpr,tpr,threshold = metric.roc_curve(y_one_hot, norm_x)
        #fpr, tpr, thresholds = metric.roc_curve(y_one_hot.ravel(), norm_x.ravel())
        #plt.plot(fpr, tpr, label='all, AUC={:.2f}'.format(metric.auc(fpr, tpr)))
        fpr, tpr, thresholds = metric.roc_curve(y_one_hot[:,0], norm_x[:,0])
        all_record.append(fpr)
        all_record.append(tpr)
        #axins.plot(fpr, tpr)
        axes.plot(fpr, tpr, label='Virus, AUC={:.2f}'.format(100*np.mean(SAUC[:, 0])))

        fpr, tpr, thresholds = metric.roc_curve(y_one_hot[:,1], norm_x[:,1])
        #axins.plot(fpr, tpr)
        axes.plot(fpr, tpr, label='Fungus, AUC={:.2f}'.format(100*np.mean(SAUC[:, 1])))
        all_record.append(fpr)
        all_record.append(tpr)
        fpr, tpr, thresholds = metric.roc_curve(y_one_hot[:,2], norm_x[:,2])
        all_record.append(fpr)
        all_record.append(tpr)
        #axins.plot(fpr, tpr)
        axes.plot(fpr, tpr, label='Bacteria, AUC={:.2f}'.format(100*np.mean(SAUC[:, 2])))
        all_record.append(fpr)
        all_record.append(tpr)
        fpr, tpr, thresholds = metric.roc_curve(y_one_hot[:,3], norm_x[:,3])
       # axins.plot(fpr, tpr)
        axes.plot(fpr, tpr, label='Chlamydia, AUC={:.2f}'.format(100*np.mean(SAUC[:, 3])))
        all_record.append(fpr)
        all_record.append(tpr)
        fpr, tpr, thresholds = metric.roc_curve(y_one_hot[:,4], norm_x[:,4])
        #axins.plot(fpr, tpr)
        axes.plot(fpr, tpr, label='Mycoplasma, AUC={:.2f}'.format(100*np.mean(SAUC[:, 4])))


        #plt.figure(3)
        #plt.plot(fps, tps, label='COVID, AUC={:.4f}'.format(metric.auc(fpr, tpr)))
# with open("record_5c.csv","w") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(fps)
#     writer.writerow(tps)
#     for item in all_record:
#         writer.writerow(item)

#plt.figure(1)
#plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

#mark_inset(axes, axins, loc1=2, loc2=4, fc="none", ec="0.5")
#plt.draw()

axes.legend()
plt.tight_layout()


plt.savefig('result_plt/dbz/roc_5c_new.jpg')
