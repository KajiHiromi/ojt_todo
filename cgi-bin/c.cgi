#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;

use DBI;

my $user = 'todouser';
my $passwd = 'kaji';

my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
my $tagQuery = $db->prepare("SELECT * FROM tag WHERE tag = ?;");
   
my $body= "kensaku=ビジネス";

my $task = split(/&/, $body);
print "$task\n";

   my ($key, $value) = split(/=/,$task);
  print "キー$key => $value\n";

 my $task2{$key} = $value;
 print "これが\%task2\n";

 
$tagQuery->execute($body->{kensaku});
print "けんさくは\%task2->{kensaku}\n";

#for (my $i=0; $i < $tasks_num; $i++) {
  my $tag = $tagQuery->fetchrow_hashref;
  print $tag->{id}."\n";
 
  my $tasktagsQuery = $db->prepare("SELECT * FROM tasktag WHERE tag_id=?");
   $tasktagsQuery->execute($tag->{id});
   #print $task->{id};
   my $tasktags_num = $tasktagsQuery->rows;
    
     for (my $i=0; $i < $tasktags_num; $i++){
       my $tasktag = $tasktagsQuery->fetchrow_hashref;

        print Dumper $tasktag;

       my $taskQuery = $db->prepare("SELECT * FROM task WHERE id=? AND status=?");
       $taskQuery->execute($tasktag->{task_id},"未完了");

       my $tasks_num = $taskQuery->rows;

        for (my $i=0; $i < $tasks_num; $i++){
       my $task = $taskQuery->fetchrow_hashref;
          # print Dumper $tag;
 
        }
   
     }
#}
