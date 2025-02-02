# _*_coding:utf-8_*_
__author__ = 'mcy'
__date__ = '2019-04-29 15:06'

'''
netlaprls
'''

import numpy as np
from sklearn.metrics import precision_recall_curve, roc_curve, accuracy_score, precision_score
from sklearn.metrics import auc

'''
Default parameters in [1]:
    gamma_d1 = gamma_p1 = 1
    gamma_d2 = gamma_p2 = 0.01
    beta_d = beta_p = 0.3
Default parameters in this implementation:
    gamma_d = 0.01, gamma_d=gamma_d2/gamma_d1
    gamma_t = 0.01, gamma_t=gamma_p2/gamma_p1
    beta_d = 0.3
    beta_t = 0.
'''


class NetLapRLS:
    def __init__(self, gamma_d=10.0, gamma_t=10.0, beta_d=1e-5, beta_t=1e-5):
        self.gamma_d = float(gamma_d)
        self.gamma_t = float(gamma_t)
        self.beta_d = float(beta_d)
        self.beta_t = float(beta_t)

    def fix_model(self, W, intMat, drugMat, targetMat, seed=None):
        R = W*intMat
        m, n = R.shape
        # 修正similarity matrix --> symmetric matrix
        drugMat = (drugMat + drugMat.T)/2.
        targetMat = (targetMat + targetMat.T)/2.

        # 药物相似度矩阵
        Wd = (drugMat+self.gamma_d*np.dot(R, R.T)) / (1.0+self.gamma_d)
        Wt = (targetMat+self.gamma_t*np.dot(R.T, R)) / (1.0+self.gamma_t)
        # 去除主对角线上自身的评分e
        Wd = Wd-np.diag(np.diag(Wd))
        Wt = Wt-np.diag(np.diag(Wt))
        # D是一个wd的按照列相加 得到的为列表 长度为drug 开根号 的对角矩阵  D=Dd^(-1/2)
        ## Dd节点的度矩阵
        Wd_srow = np.sum(Wd, axis=1, dtype=np.float64)
        D = np.diag(1.0/np.sqrt(Wd_srow))
        Ld = np.eye(m) - np.dot(np.dot(D, Wd), D)  # Ld = Indxnd - DwdD

        Wt_srow = np.sum(Wt, axis=1, dtype=np.float64)
        # print np.where(Wt_srow == 0)  # 检查np.sum(Wt,axis=1))是否有0
        D = np.diag(1.0/np.sqrt(Wt_srow))
        Lt = np.eye(n) - np.dot(np.dot(D, Wt), D)

        # np.linalg为行业标准级fortran库  inv求矩阵的逆  X = (wd + beta_d*wd)^(-1)
        X = np.linalg.inv(Wd+self.beta_d*np.dot(Ld, Wd))
        Fd = np.dot(np.dot(Wd, X), R)
        X = np.linalg.inv(Wt+self.beta_t*np.dot(Lt, Wt))
        Ft = np.dot(np.dot(Wt, X), R.T)
        self.predictR = 0.5*(Fd+Ft.T)

    def predict_scores(self, test_data, N):
        inx = np.array(test_data)
        # TODO 输出预测值之前正则化
        return self.predictR[inx[:, 0], inx[:, 1]]

    # test_data 预测样本的下标 test_label 原样本下标对应的值
    '''
      precision_recall_curve  Returns
    -------
    precision : array, shape = [n_thresholds + 1]
        Precision values such that element i is the precision of
        predictions with score >= thresholds[i] and the last element is 1.

    recall : array, shape = [n_thresholds + 1]
        Decreasing recall values such that element i is the recall of
        predictions with score >= thresholds[i] and the last element is 0.

    thresholds : array, shape = [n_thresholds <= len(np.unique(probas_pred))]
        Increasing thresholds on the decision function used to compute
        precision and recall.

    '''
    def evaluation(self, test_data, test_label):  # 这里的test_data 为下标
        scores = self.predictR[test_data[:, 0], test_data[:, 1]]
        # test_label的值为原始intMat中对应下标的值 scores是将原始intMat中对应test_data的下标置为0后经过fix后 对应下标位置的得分
        prec, rec, thr = precision_recall_curve(test_label, scores)
        # print 'precision & recall thresholds is '
        # print thr
        aupr_val = auc(rec, prec)
        fpr, tpr, thr = roc_curve(test_label, scores)
        # print 'fpr & tpr thresholds is '
        # print thr
        auc_val = auc(fpr, tpr)
        return aupr_val, auc_val, scores, test_label  # scores = test_data

    def accuracy_md(self, test_data, test_label):
        scores = self.predictR[test_data[:, 0], test_data[:, 1]]
        return accuracy_score(test_label, scores.round(), normalize=True)

    def __str__(self):
        return "Model: NetLapRLS, gamma_d:%s, gamma_t:%s, beta_d:%s, beta_t:%s" \
               % (self.gamma_d, self.gamma_t, self.beta_d, self.beta_t)