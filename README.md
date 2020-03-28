### 工具
* `python: 3.7`
* `baostock: 0.8.8`
* `pandas: 1.0.3`   
* `numpy: 1.18.0`    

### 运行文件
* `update_base_stocks.py`: 用于筛选出基本股票, 共 744 股
* `filter_stocks.py`: 从基本股票中， 根据`净资产收益率(ROF)`, `滚动市盈率(peTTM)`, `市净率(pbMRQ)` 筛选出值得投资的股票

### 存储文件
* `base_stocks.csv`：存储基本股
* `filter_stocks.csv`: 存储筛选后的股票