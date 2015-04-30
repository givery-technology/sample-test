# Sample Test for new Code-Check

code-checkとは[Givery](https://github.com/givery-technology)が開発中のWebアプリケーションです。このサービスでは、ユーザーは様々な種類のコーディングテストを作成したり、回答をすることが出来ます。
このテストは、そのサービスに向けてのプロトタイプのテストです。

## 目的

- Giveryの求職者の開発スキルを測定する
- Giveryがどのような開発体制で開発をしているのかの理解を促す([api-first-spec](https://github.com/shunjikonishi/api-first-spec)など)
- code-checkのサービス開発・機能改善の参考にする

## 問題

- Webアプリケーションフレームワーク等を活用してREST APIを作成してください。
- APIのスペックは[spec](spec)からご覧いただけます.
  - これらのスペックは [api-first-spec](https://github.com/shunjikonishi/api-first-spec)を使って作成されており、いくつかのAPIテストがあります。
- 上記で定義されているAPIの全てのテストを通過するWebアプリケーションを作成してください。

## 回答方法
このテストには
- Webアプリケーションフレームワーク
- MySQLデータベース
- GitHubアカウント(リポジトリをフォークするため)

の利用が必要です。

まずはじめに、あなたのGithubアカウントでこのリポジトリをフォークし、その後フォークしたリポジトリを用いてWebアプリケーションを作成してください。

データベースの構造とサンプルデータは [sql/create.sql](sql/create.sql)に記載しています。  
MySQLサーバをたてて、スクリプトを実行してください。

もし、自動で開発環境を構築したい場合、弊社が提供している [test env builder](https://github.com/code-check/env-builder)をご活用いただくことも可能です。

上記利用の場合は、以下のコマンドより実行してください。

``` bash
git clone git@github.com:code-check/env-builder.git test-env
cd test-env
cp Vagrantfile.sample Vagrantfile
cp hosts.sample hosts
vagrant up
ansible-playbook all.yml
vagrant ssh
git clone git@github.com:[YOUR GITHUB ACCOUNT]/sample-test.git
mysql -uvagrant -pvagrant -Dvagrant < sample-test/sql/create.sql

cd sample-test
```

## api-first-spec testの実行方法

api-first-specは[Mocha](http://mochajs.org/)を利用しています。
テストの実行は以下のコマンドより実行できます。

``` bash
cd sample-test
npm install
mocha spec/*
```

単体テストも以下のコマンドより実行可能です。

``` bash
mocha spec/users_login.js
```

アプリケーションのデフォルトの設定は [spec/config/config.json](spec/config/config.json).  
に記載されています。

## 問題
このアプリケーションは、シンプルなイベント予約システムです。

- 以下2通りのユーザーがあります。
  - student
  - company
- 全てのユーザーはイベントリストを閲覧することが出来ます。
(ログインしていないユーザーも含む)
- studentが予約していないイベントを予約することが出来ます。
- companyは、彼らの作成したイベントを閲覧することが出来ます。

### Q1. login APIを作成してください
- email と password をもちいてログイン出来るようにしてください。
- login token と user data を返すようにしてください。
  - group_id = 1 は student userを表します。
  - group_id = 2 は company userを表します。

### Q2. student向けの event_list API を作成してください
- ログインは必須ではありません
- "from" パラメータは必須です。
  - これは開催日が「いつから」のイベントを取得するかというものです。
- "offset" と "limit" のパラメータは任意です。

### Q3. reserve と unreserve API を作成してください
- ログインは必須です。
- 予約できるユーザーはstudentでないといけません。

### Q4. company向けの event_list API を作成してください。
- ログインは必須です。
- ユーザーはcompanyでなければいけません。
- イベント情報にはイベントエントリー者の合計が含まれます。

### Q5. リファクタリングをしてください
もし、あなたがこのアプリケーションのプロジェクトマネージャーだとして、このアプリケーションを改善するとしたら、何をしますか？
あなたの意見を answer.md に記載してください。

## 提出方法
- [issue](https://github.com/code-check/sample-test/issues)に以下の方法で提出してください。
  - "implemented"というタイトルを付けてください。
  - コメント欄にあなたの回答リポジトリのURLを記載してください。

## サポート
もし質問がある場合はこのリポジトリの [issue](https://github.com/code-check/sample-test/issues)までお問い合わせください。

このテストは新しいWebサービスのための実験的なテストでもありますので、もしフィードバックがあれば、是非アドバイス等いただければ幸いです。
