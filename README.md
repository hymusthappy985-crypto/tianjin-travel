# 天津旅游规划：Python + Streamlit

## 1. 安装 Python
建议 Python 3.10 或更高版本。

## 2. 安装依赖

在项目目录打开终端：

```bash
pip install -r requirements.txt
```

## 3. 运行

```bash
streamlit run app.py
```

运行后终端会出现一个本地地址，一般类似：

http://localhost:8501

复制到浏览器打开即可。

## 4. 项目结构

```text
tianjin_travel_streamlit/
├── app.py
├── requirements.txt
└── README.md
```

## 5. 当前功能

- 1～7天旅游天数
- 旅行人数
- 能否接受勾芡
- 清淡 / 微辣 / 中辣 / 辣
- 鲁菜、川菜、粤菜、苏菜、闽菜、浙菜、湘菜、徽菜、津菜
- 慢节奏 / 快节奏
- 经济型 / 舒适型 / 品质型 / 高端型住宿
- 只玩市区 / 可去郊区 / 希望包含郊区
- 自动生成每日行程
- 自动匹配餐厅
- 自动推荐住宿
- 自动估算预算

## 注意

景点、餐厅、酒店目前是课程项目演示数据，不是实时数据。
