#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;

use DBI;

my $user = 'todouser';
my $passwd = 'kaji';

my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
my $tasksQuery = $db->prepare("SELECT * FROM task WHERE user_id = ? AND status = ?;");
    
$tasksQuery->execute(1,"未完了");

my $tasks_num = $tasksQuery->rows;


for (my $i=0; $i < $tasks_num; $i++) {
  my $task = $tasksQuery->fetchrow_hashref;
# print $task->{id}."\n";
   my $tasktagsQuery = $db->prepare("SELECT * FROM tasktag WHERE task_id=?");
   $tasktagsQuery->execute($task->{id});
   #print $task->{id};
   my $tasktags_num = $tasktagsQuery->rows;
    
     print "<div>\n";
     print "☆TODO：$task->{name}\n\n<br>";
     print "期限： $task->{limit_time}\n\n<br>";
     print "メモ：$task->{memo}\n\n<br>";


     for (my $i=0; $i < $tasktags_num; $i++){
       my $tasktag = $tasktagsQuery->fetchrow_hashref;
       # print Dumper $tasktag;
       my $tagsQuery = $db->prepare("SELECT * FROM tag WHERE id=?");
       $tagsQuery->execute($tasktag->{tag_id});

       my $tags_num = $tagsQuery->rows;

        for (my $i=0; $i < $tags_num; $i++){
          my $tag = $tagsQuery->fetchrow_hashref;
          # print Dumper $tag;
 
          print "カテゴリー：$tag->{tag}\n\n";
        }
      
     }
}
