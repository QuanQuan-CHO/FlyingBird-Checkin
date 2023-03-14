# suying666-clock-in

速鹰666自动签到领流量，配合GitHub Actions使用

# 使用
1. 点击Settings->Secrets->Actions->New repository secret，依次配置`EMAIL`、`PASSWD`
    - EMAIL 是suying666的账号
    - PASSWD 是suying666的密码
2. 先在Actions页面将GitHub Action启用，再选择对应的workflow，将scheduled workflow启用
   ![enable-schedule-workflow](https://user-images.githubusercontent.com/90035785/224888848-be15ba52-1892-4a2b-9cef-b321b9a25165.jpg)
3. UTC时间的每天01:00分（北京时间：09:00，并不准时），github actions会自动帮助您签到领取流量
4. enjoy it!!!

# 特性

1. 每次登陆成功后，自动更新hosts.txt，避免因为host被墙，而自动签到失败
2. 完全免费，不需要服务器，与云函数
