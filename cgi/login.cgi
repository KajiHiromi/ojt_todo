#!/usr/bin/env perl

use strict;
use warnings;

# エラーをブラウザに表示
use CGI::Carp qw(fatalsToBrowser);
# DBIモジュール
use DBI;

# データの取得
if ($ENV{'REQUEST_METHOD'} eq "POST") {
 	# POSTの場合
 	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} else {
 	# GETの場合
 	$buffer = $ENV{'QUERY_STRING'};
}

$lname = param('username');
$lpass = param('password');


# ユーザー名とパスワード
$user = 'todouser';
$pass = 'kaji';

# DBへ接続
$db = DBI->connect('dbi:mysql:todo','$user','$pass');

# 命令
$sth = $db->prepare("select * from USER");

# 実行
$sth->execute;
while(@rows = $sth->fetchrow_array){
        $login_id = $rows[1];
        $login_pw = $rows[2];
        
	# 認証
	if($lname eq $login_id && $lpass eq $login_pw){
                print "Location: ok_login.pl\n\n";
        }else{
                print "Location: login.html\n\n";
        }
}
$db->disconnect();



