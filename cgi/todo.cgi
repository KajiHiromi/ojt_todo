#!/usr/bin/env perl

use strict;
use warnings;
# エラーをブラウザに表示
use CGI::Carp qw(fatalsToBrowser);
# DBIモジュール
use DBI;


# ユーザー名とパスワード
$user = 'todouser';
$pass = 'kaji';

# DBへ接続
$db = DBI->connect('dbi:mysql:todo','$user','$pass');

# 命令
# 追加
$sth = $db->prepare(
# "INSERT INTO task (task_name,limit_time,memo,user_id) VALUES ()");
#取り出す
$sth = $db->prepare("SELECT id,task_name,limit_time,memo,user_id FROM task");


# 実行
$sth->execute;
while(@rows = $sth->fetchrow_array){
	$login_id = $rows[1];
	$login_pw = $rows[2];
}                                                                                                                
$db->disconnect();

