#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use DBI;

my $newTag = "tag".int(rand() * 100000);
#my $body2 = "tag=ビジネス";
my $user_id = 1;
my $user_name = 'kaji';
my $database = 'todo';

my $user = 'todouser';
my $passwd = 'kaji';

my %task = (
"task" => "",
"tag" => [],
"limit_time" => "",
"memo" =>"" );

#print "1ばん$body2";

my $method = $ENV{'REQUEST_METHOD'};
$method = $method || "GET";
print "method = $method\n";


if ($method eq 'GET') {
    my $body = $ENV{'QUERY_STRING'};
    print "GETに入った";
 }
  elsif ($method eq 'POST') {
    print "POSTに入った";
    read(STDIN, my $body, $ENV{'CONTENT_LENGTH'});
    $body =~tr/+//;
    $body=~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;
    print "これ$body\n";
    my %body = map{ split(/\=/, $_); } split(/&/, $body);
　　
    #print $body;

#my @params = split(/&/, $body);

#print @params;

#foreach my $param (@params){
  #  my ($key, $value) = split(/=/, $param);
 #   if ($key eq "tag"){
 #       push @{$task{tag}},$value;


#print "なかみは、$param";
#
  #  }else{
 #       $task{$key} = $value;
#    }


#my $body = "tag=プライベート";
my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
my $tagQuery = $db->prepare("SELECT * FROM tag WHERE tag = ?;");


$tagQuery->execute($body->{tag});
#my $tags_num =$tagQuery->rows;

#for (my $i=0; $i < $tags_num; $i++) {
my $tag = $tagQuery->fetchrow_hashref;
print $tag->{id}."\n";
  
my $tasktagsQuery = $db->prepare("SELECT * FROM tasktag WHERE tag_id=?");
$tasktagsQuery->execute($tag->{id}) || die $tasktagsQuery->errstr;
                        #print $task->{id};
my $tasktags_num = $tasktagsQuery->rows;
  
for (my $i=0; $i < $tasktags_num; $i++){
    my $tasktag = $tasktagsQuery->fetchrow_hashref;
  
    print Dumper $tasktag;                   
    my $taskQuery = $db->prepare("SELECT * FROM task WHERE id=? AND status=?");      
    $taskQuery->execute($tasktag->{task_id},"未完了") || die $taskQuery->errstr;
  
    my $task2 = $taskQuery->fetchrow_hashref;
    


}
}
