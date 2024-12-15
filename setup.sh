#!/bin/bash

# エラーが発生した場合にスクリプトを停止
set -e

# スーパーユーザー権限の確認
if [ "$EUID" -ne 0 ]; then 
    echo "このスクリプトはroot権限で実行する必要があります"
    echo "sudo ./install-openspeedtest.sh を実行してください"
    exit 1
fi

# システムのアップデート
echo "システムをアップデートしています..."
apt update && apt upgrade -y

# 必要なパッケージのインストール
echo "必要なパッケージをインストールしています..."
apt install -y git nginx

# OpenSpeedTestのダウンロードとセットアップ
echo "OpenSpeedTestをダウンロードしています..."
cd /var/www
git clone https://github.com/openspeedtest/Speed-Test.git
mv Speed-Test openspeedtest
chown -R www-data:www-data /var/www/openspeedtest

# Nginxの設定
echo "Nginxの設定を行っています..."
cat > /etc/nginx/sites-available/openspeedtest << 'EOF'
server {
    listen 80;
    server_name localhost;

    root /var/www/openspeedtest;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF

# デフォルトのNginx設定を無効化し、新しい設定を有効化
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/openspeedtest /etc/nginx/sites-enabled/

# Nginxの設定テストと再起動
nginx -t
systemctl restart nginx

echo "インストールが完了しました！"
echo "ブラウザで http://localhost にアクセスしてOpenSpeedTestを使用できます"
