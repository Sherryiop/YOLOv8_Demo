# YOLOv8_Demo
此案例將利用物件檢測模型YOLOv8來辨識蘋果

  
若要了解更多YOLOv8相關資料，請參考: [YOLOv8 Github](https://github.com/ultralytics/ultralytics?tab=readme-ov-file)  |  [YOLOv8 語法](https://docs.ultralytics.com/)
## 下載專案

#### 方法一
若有安裝[Git](https://ithelp.ithome.com.tw/articles/10322227)，在Terminal確認要下載的目的地後，輸入以下指令:
```bash
git clone https://github.com/Sherryiop/YOLOv8_Demo.git --depth 1 
```

#### 方法二
直接點Download.zip下載

## 貼標
### 環境建立
此步驟為建立物件貼標的環境
在Terminal將路徑指定到 YOLOv8_Demo\labellmg後輸入以下指令，安裝所需套件
  
```bash
pip install -r requirement.txt
```
### 確認物件名稱
請至predefined_classes.txt確認物件名稱及數量，文件路徑為labelImg\data\predefined_classes.txt

本次檢測的物件只有一個，所以predefined_classes.txt內容只有一行
```bash
Apple
```
### 貼標程式介面與使用方法
執行 YOLOv8_Demo\labellmg\labelImg.py，其介面與使用方法如下圖
![圖片1](https://github.com/user-attachments/assets/323e808e-fcc2-4179-8ee4-8da12ac2c65a)


## xml檔 -> txt檔
### 環境建立
由於labellmg輸出的程式為xml檔，但YOLO訓練只讀txt檔，需要進行檔案轉錄

路徑指定到YOLOv8_Demo\XmlToTxt後，安裝轉錄檔案所需要的環境，指令如下
```bash
pip install -r requirements.txt
```
原始來源:[XmlToTxt Github](https://github.com/isabek/XmlToTxt/tree/master)

### 轉錄檔案
把要轉錄的xml檔案放置XmlToTxt\xml，如果沒有該資料夾，需要自己建立  

確認XmlToTxt\classes.txt 檔案內容跟YOLOv8_Demo\labelImg\data\predefined_classes.txt 一樣後，在Terminal指定到XmlToTxt後輸入以下指令，以轉錄程式
```bash
python xmltotxt.py -xml xml -out out
```
轉錄後的txt檔會在XmlToTxt\out

## YOLO模型訓練
### 環境建立
$${\color{red}若未安裝cuda，請先安裝後，再安裝YOLOv8。}$$  
**環境要求:Python>=3.8**

請確認python>=3.8後，安裝YOLOv8套件
```bash
pip install ultralytics
```


### 配置yaml檔(訓練檔)
yaml檔為YOLO的訓練檔案，其格式如下

```bash
path:  path\to\Datasets\Example               # dataset root dir 
train:  path\to\Datasets\Example\images\train # training set root dir
val: path\to\Datasets\Example\images\val      # val set root dir
test: # test images (optional)

nc : 1 # the number of class

# Classes
names:
  0 : Apple
```
因為此案例只有檢測一種物件，故nc為1
names下方填寫物件名稱，需與檔案labelImg\data\predefined_classes.txt內容順序一致

### 模型訓練
**預訓練模型下載**:[YOLOv8n.pt](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt)

**Dataset 格式**  

資料格式必須遵守以下結構
  ```
Example
  ├── images
  │   ├── train
  │   └── val
  ├── labels
  │   ├── train
  │   └── val
  ```
**訓練指令**  

確認資料夾格式正確後，輸入訓練指令，需改寫yaml路徑；路徑盡量不要包含中文，以避免報錯
```bash
yolo detect train data=yaml路徑 model=yolov8n.pt epochs=250 imgsz=640 patience=50 device=0 batch=-1
```
此訓練指令適用於較高等級的顯卡或是資料量大的情形。

若顯卡等級較低或資料量較少可以試試看降低batch size或是改用CPU訓練，指令改寫如下:

```bash
yolo detect train data=yaml路徑 model=yolov8n.pt epochs=250 imgsz=640 patience=50 device=cpu batch=4
```

訓練後的模型路徑會顯示於下於紅色框位置
![圖片2](https://github.com/user-attachments/assets/cf95f192-abee-4b8a-ba7a-cb58e53c026c)


## YOLO模型測試
### 修改Apple_detection.py
修改模型、圖片輸入與輸出的路徑

模型要選擇**best.pt**，其路徑為runs\train\weights\best.pt  
```bash
#===========================================================#
# 模型和圖片路徑設定
#===========================================================#
model_path =r'path\to\runs\train\weights\best.pt' # YOLO model path
source =r'path\to\apple.jpg'                      # test picture path
output_path = =r'path\to\output_apple.jpg'        # picture output path
model = YOLO(model_path)
#===========================================================#
```
路徑修改後，即可執行


