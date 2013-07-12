
#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use DBI;

my $newTag = "tag".int(rand() * 100000);
my $body = "task=あいう&tag=$newTag&tag=プライベート&limit_time=&memo=&Submit=>登録";
my $user_id = 1;
my $user_name = 'kaji';
my $database = 'todo';

my %task = (
"task" => "",
"tag" => [],
"limit_time" => "",
"memo" =>"" );
my @params = split(/&/, $body);

foreach my $param (@params){
  my ($key, $value) = split(/=/, $param);
    if ($key eq "tag"){
      push @{$task{tag}},$value;
    }else{
      $task{$key} = $value;
    }
}

sub insertDB {
  my %task = @_;
  my $todouser = 'todouser';
  my $passwd = 'kaji';
  my $db = DBI->connect('DBI:mysql:todo',$todouser,$passwd);

# 1. user の確認
  my $user_find_query = $db->prepare("SELECT * FROM user WHERE id =?;");
  my $user_data=$user_id;
  $user_find_query->execute($user_data) || die $user_find_query->errstr;
  my $find_user = $user_find_query->fetchrow_hashref;
  
    if($find_user->{id} eq $user_id){
    }else{
 # COMMENT 0: prepareで値を渡すときは「placeholder」を使ってください(以降全てのINSERT文で同様)
     my $user_insert_query = $db->prepare("INSERT INTO user(name) VALUES (?) ;");
     my $user_data = $user_name;    

 # COMMENT 1: この方法だと、name = $user_id になってしまいますけど、いいですか？
      $user_insert_query->execute($user_data) || die $user_insert_query->errstr;
 # COMMENT 2: $find_userが無いので、taskに user_id が紐付かず、「誰のTaskなのか」がわからなくなります

     my $last_insert_user_id = $db->last_insert_id($database,$database,'user','id'); 

      $find_user = {
        id => $last_insert_user_id,
      };
    }  
# # 3. task の追加
 # COMMENT 3: COMMENT 2でも書きましたが、 user_id がひも付きません
   my $task_insert_query = $db->prepare("INSERT INTO task(name,limit_time,memo,user_id) VALUES ( ?, ?, ?, ?)");
   my @task_data = ($task{task},$task{limit_time},$task{memo},$find_user->{id});
   my $task_last_id;   
   $task_last_id = $task_insert_query->execute(@task_data) || die $task_insert_query->errstr;
# # taskのidをとってくる
# # COMMENT 4: dbにinsertしたもののIDについては http://blog.livedoor.jp/sasata299/archives/51280681.html を参照してください
# # COMMENT 5: FROM idとありますが、idというテーブルはなかったと思います・・・
   $task_last_id = $db->last_insert_id($database,$database,'task','id');
#
# # 2. tag の確認
   foreach my $tag (@{$task{tag}}){
# # COMMENT 6: このクエリだと、「tag テーブルに格納されているデータをすべて取得」になってしまいます
     my $tag_find_query = $db->prepare("SELECT * FROM tag WHERE tag=?");
     $tag_find_query->execute($tag) || die $tag_find_query->errstr;
     my $find_tag = $tag_find_query->fetchrow_hashref;
     if($find_tag){
       my $tag_last_id = $find_tag->{id};
       my $tasktag_insert_query = $db->prepare("INSERT INTO tasktag(task_id,tag_id) VALUES (?,?);");
       my @tasktag_data = ($task_last_id,$tag_last_id);
       $tasktag_insert_query->execute(@tasktag_data) || die $tasktag_insert_query->errstr;
     }else{
       my $tag_insert_query = $db->prepare("INSERT INTO tag(tag) VALUE (?) ;");
       my $tag_data = $tag;
       my $tag_last_id; 
       $tag_last_id = $tag_insert_query->execute($tag_data) || die $tag_insert_query->errstr;
       $tag_last_id = $db->last_insert_id($database,$database,'tag','id');     
       my $tasktag_insert_query = $db->prepare("INSERT INTO tasktag(task_id,tag_id) VALUES (?,?) ;");
       my @tasktag_data = ($task_last_id,$tag_last_id);
       $tasktag_insert_query->execute(@tasktag_data) || die $tasktag_insert_query->errstr;
     }  
  #$db->disconnect();
   }
 return 1;
 }
 insertDB(%task);

# Daichi Morifuji
#
# # COMMENTって書いてあるところを見てください。
#
# このままだと動かないです・・・
#
# 1. prepareではplaceholder 「?」 を使う
# 2. FROM のあとは対象となるtableが来ます
# 3. SELECT 文では WHERE 節が無いと全部取得になります
# 4. LAST_INSERT_ID() を調べてください{

















