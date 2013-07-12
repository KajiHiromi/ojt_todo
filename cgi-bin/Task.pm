#!/usr/bin/env perl
package Task;

use strict;
use warnings;
use Data::Dumper;
use DBI;

my %db = (
  database => 'todo',
  user     => 'todouser',
  pass     => 'kaji',
  host     => 'localhost',
  port     => 3306,
);

sub findById {
  my ($id) = @_;
  
  my $db = DBI->connect("DBI:mysql:$db{database}", $db{user}, $db{pass}) or return -1;
  
  my $find_query = $db->prepare("SELECT * FROM task WHERE id = ?");
  $find_query->execute($id) or return -1;

  my $task = $find_query->fetchrow_hashref;
  if($task){
    # tasktagの取得
    my $tasktag_query = $db->prepare("SELECT * FROM tasktag WHERE task_id = ?");
    $tasktag_query->execute($task->{id}) or return -1;

    # tagsの初期化
    my @tags;
    # tagを取得するクエリの準備
    my $tag_query = $db->prepare("SELECT * FROM tag WHERE id = ?");
    while(my $tasktag = $tasktag_query->fetchrow_hashref){
      $tag_query->execute($tasktag->{tag_id}) or return -1;
      my $tag = $tag_query->fetchrow_hashref;
      if($tag){
        push @tags, $tag->{tag};
      }
    }
   
    return new Task("id=$task->{id}&user_id=$task->{user_id}&name=$task->{name}&limit_time=$task->{limit_time}&memo=$task->{memo}&".(join "&", map{ "tag=$_"; } @tags));
  }else{
    return undef;
  }
}




sub new {
  my ($self, $body, $user_id) = @_;
  
  my $this = bless {
    id => undef,
    user_id => $user_id,
    name => "",
    tag  => [],
    limit_time => "",
    memo => "",
    status =>"未完了",
  }, $self;

  $this->parseBody($body);

  $this;
};

sub parseBody {
  my ($self, $body) = @_;
  my @params = split(/&/, $body);

  foreach my $param (@params){
    my ($key, $value) = split(/=/, $param);
      if ($key eq "tag"){
        push @{$self->{tag}},$value;
      }else{
        $self->{$key} = $value;
      }
  }
}

sub insert {
    my ($self) = @_;
    my $db = DBI->connect("DBI:mysql:$db{database}", $db{user}, $db{pass}) or return -1;

    # 1. user の確認
    my $user_find_query = $db->prepare("SELECT * FROM user WHERE id = ?;");
    my $user_data=$self->{user_id};
    $user_find_query->execute($user_data) || die $user_find_query->errstr;
    my $find_user = $user_find_query->fetchrow_hashref;
    warn Dumper $find_user;  
    if($find_user->{id}){
    }else{
      my $user_insert_query = $db->prepare("INSERT INTO user(name) VALUES (?) ;");
      my $user_data = "ななしのごんべ";

      $user_insert_query->execute($user_data) || die $user_insert_query->errstr;

      my $last_insert_user_id = $db->last_insert_id($db{database},$db{database},'user','id'); 

      $find_user = {
        id => $last_insert_user_id,
      };
    }
  
    # # 3. task の追加
    my $task_insert_query = $db->prepare("INSERT INTO task(name,limit_time,memo,user_id) VALUES ( ?, ?, ?, ?)");
    my @task_data = ($self->{name}, $self->{limit_time}, $self->{memo}, $find_user->{id});
    print $self->{name};
    my $task_last_id;   
    $task_last_id = $task_insert_query->execute(@task_data) || die $task_insert_query->errstr;
    # taskのidをとってくる
    $task_last_id = $db->last_insert_id($db{database},$db{database},'task','id');

    # 2. tag の確認
    foreach my $tag (@{$self->{tag}}){
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
        $tag_last_id = $db->last_insert_id($db{database},$db{database},'tag','id');     
        my $tasktag_insert_query = $db->prepare("INSERT INTO tasktag(task_id,tag_id) VALUES (?,?) ;");
        my @tasktag_data = ($task_last_id,$tag_last_id);
        $tasktag_insert_query->execute(@tasktag_data) || die $tasktag_insert_query->errstr;
      }  
   }
#   $db->disconnect();
   return 1;
}


sub updateStatus {
   my ($self, $value) = @_;
   my $sql = "UPDATE task SET status = ? WHERE id = ?;";
   my $db = DBI->connect("DBI:mysql:$db{database}", $db{user}, $db{pass}) or return -1;
   my $task_update_query = $db->prepare($sql);
   $task_update_query->execute($value, $self->{id}) || die $task_update_query->errstr;

}



1;
