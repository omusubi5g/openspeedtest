# 使い方
1. wsl2のUbuntu 24.04 でsetup.shを実行すると、localhostでOpenSpeedTestがインストールされ、立ち上がります
1. /var/www/speedtest/index.htmlを変更します
1. logger.pyを実行します（必要なライブラリは適宜pipでインストールしてください）
1. localhostでOpenspeedTestを実行するたび、localhost:5000にログが記録されていきます
1. LAN内からアクセスするには下記を参考に、wsl2のUbuntuあてに80番ポートをポートフォワーディングしておきます
https://qiita.com/kentomo1002/items/82234030e712c44c2e40

![image](https://github.com/user-attachments/assets/50fdb2e7-bdb7-4b85-95b8-ee80a03f7352)
![image](https://github.com/user-attachments/assets/56c6e0a7-653b-48bc-b930-d5cb2c3c4df2)
