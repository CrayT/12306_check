### 12306 查询车次及票价信息
- 终端运行方法：
```bash
python3 tickets.py 起始站 终点站 YYYY-MM-DD
```
- 示例：
![image](https://s2.ax1x.com/2019/01/04/FTcMMn.png)

> 注意：12306接口经常变化，使用时可能会报错。

> 2019-01-18，今天更新图形界面时，发现票价接口的返回信息关键字已经变了、、、无语、、只好在图形界面中取消展示价格信息，只显示余票信息，终端显示的没有改，有需要的自己改吧、

- GUI界面使用:
![image](https://s2.ax1x.com/2019/01/18/k9kGeH.png)
> 1，用户名及密码配置在config.conf中，打开界面即出现验证码图片，点击 `刷新验证码` 按钮可刷新验证码。

> 2，`刷新验证码` 按钮下面为需要选择的验证码，8个小图显示在右方，将选择的验证码小图序号填写在右方 `验证码` 文本框内，中间用英文逗号隔开，如 `1,3,4` ，然后点击 ` 登陆` 按钮即可登陆，提示 `用户，**，登陆成功!` 即表示已成功登陆。

> 3，出发、到达填写城市中文名，日期通过calendar选择，出发时间手动填写，如15表示下午三点，可筛选出此时间之后的列车信息。