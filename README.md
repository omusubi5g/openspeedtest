# はじめに
https://github.com/openspeedtest/Speed-Test
をWindowsPCのwsl2上Ubuntuで動かしつつ、各測定のログを記録するサーバーをPythonで実行しています。

# 使い方
1. wsl2のUbuntu 24.04 でsetup.shを実行すると、OpenSpeedTestがインストールされ、立ち上がります [http://自身のIPアドレス]
1. /var/www/speedtest/index.htmlを変更します [http://自身のIPアドレス:5000/に結果をPOSTするように変更する]

1. logger.pyを実行します（必要なライブラリは適宜pipでインストールしてください）
1. [http://自身のIPアドレス] でOpenspeedTestを実行するたび、[http://自身のIPアドレス:5000]にログが記録されていきます
1. LAN内からアクセスするには下記を参考に、wsl2のUbuntuあてに80番ポートをポートフォワーディングしておきます
https://qiita.com/kentomo1002/items/82234030e712c44c2e40

![image](https://github.com/user-attachments/assets/50fdb2e7-bdb7-4b85-95b8-ee80a03f7352)
![image](https://github.com/user-attachments/assets/56c6e0a7-653b-48bc-b930-d5cb2c3c4df2)
