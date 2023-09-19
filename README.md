# 基於ResNet50之課堂學生狀態即時偵測系統
本專案旨在利用ResNet50為架構，訓練出一個能夠於課堂中即時偵測學生狀態之系統

## 如何訓練
請先至`train_model`資料夾中下載`requirement.txt`中所列的相依套件：
```
cd train_model
pip install -r requirement.txt
```
安裝完套件後，可進入`train.ipynb`中進行模型訓練
本專案訓練參數如下：
```
input_size = (224,224)
batch_size = 64
class_mode = 'categorical'
train_data_size = 0.8
base_model = ResNet50
epochs = 50
```
## 訓練成果(BEST)

| train accucary | valid accucary | test accucary |
|:--------------:|:--------------:|:-------------:|
|     1. 000     |      1.000     |     0.9333    |

![image](https://github.com/shiayongshen/Use_ResNet50_to_detect_student_status_in_real_time/blob/main/pic/val_acc.png)

| train loss | valid loss | test loss |
|:----------:|:----------:|:---------:|
|   0.0186   |   0.0919   |  0.1995   |

![image](https://github.com/shiayongshen/Use_ResNet50_to_detect_student_status_in_real_time/blob/main/pic/val_loss.png)


|         | precision | recall | f1-score |
| ------- |:---------:|:------:|:--------:|
| confuse |   1.00    |  1.00  |   1.00   |
| happy   |   0.83    |  1.00  |   0.91   |
| normal  |   1.00    |  0.91  |   0.95   |
| sleepy  |   0.90    |  0.90  |   0.90   |

![image](https://github.com/shiayongshen/Use_ResNet50_to_detect_student_status_in_real_time/blob/main/pic/confusion_matrix.png)

## 如何使用
進入`flask_web`中，並於終端執行：
```
python render.py
```
即可開啟網頁，其網頁分成學生端和教師端，學生端在登入後能夠開啟鏡頭偵測，而教師端則可觀看目前登入學生人數與學生目前狀態。
