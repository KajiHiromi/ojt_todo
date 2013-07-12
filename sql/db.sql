-- 文字コードを設定し、todoデータベース作成
-- DROP DATABASE IF EXIST todo;
-- CREATE DATABASE todo CHARACTER SET utf8;


-- ユーザーテーブル作成

DROP TABLE IF EXISTS user;

CREATE TABLE user (
id INT(50) NOT NULL AUTO_INCREMENT,
name VARCHAR(100) UNIQUE,
password VARCHAR(100) NOT NULL,
PRIMARY KEY (id)
);


-- タスクテーブル作成

DROP TABLE IF EXISTS task;

CREATE TABLE task(
  id INT(50) NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  limit_time datetime NOT NULL,
-- repeat INT(10) NOT NULL,
-- remainder datetime NOT NULL,
  memo TEXT(1000) DEFAULT "",
  user_id INT(50) NOT NULL,
  status VARCHAR(12) DEFAULT "未完了",
  PRIMARY KEY (id)
);


-- タグテーブル作成
DROP TABLE IF EXISTS tag;

CREATE TABLE tag(
  id INT(50) NOT NULL AUTO_INCREMENT,
  tag VARCHAR(50) UNIQUE,
  PRIMARY KEY (id)
);


-- タスクタグテーブル作成(taskとtagをつなげる)

DROP TABLE IF EXISTS tasktag;

CREATE TABLE tasktag(
  task_id INT(50) NOT NULL,
  tag_id INT(50) NOT NULL
);

-- ユーザーにすべての権限（ＤＢを扱う）をつける
-- GRANT ALL PRIVILEGES ON todo.* TO todouser@localhost IDENTIFIED BY 'kaji';
