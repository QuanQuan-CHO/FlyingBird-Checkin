✈FlyingBird机场自动签到领流量，配合GitHub Actions使用

# 使用
1. 点击Settings->Secrets->Actions->New repository secret，依次配置`EMAIL`、`PASSWD`
    - EMAIL 是suying666的账号
    - PASSWD 是suying666的密码

2. 先在Actions页面将GitHub Action启用，再选择对应的workflow，将scheduled workflow启用
   ![enable-schedule-workflow](https://user-images.githubusercontent.com/90035785/224888848-be15ba52-1892-4a2b-9cef-b321b9a25165.jpg)

3. 北京时间的每天23:50（UTC：15:50，会有[延迟](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)），GitHub Actions会自动签到领取流量，并记录今日使用流量和剩余流量

4. Enjoy it!!!
