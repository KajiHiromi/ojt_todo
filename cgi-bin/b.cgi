
#!/usr/bin/env perl
package Task;

use strict;
use warnings;
use Data::Dumper;
use DBI;

my %db = (
database => 'todo',
user => 'todouser',
pass => 'kaji',
host => 'localhost',
port => 3306,
);

sub findByTag {
my ($select_tag) = @_;
my $db = DBI->connect("DBI:mysql:$db{database}", $db{user}, $db{pass}) or return -1;
my $find_query = $db->prepare("SELECT * FROM tag WHERE tag = ?");
$find_query->execute($select_tag) or return -1;

my $tag = $find_query->fetchrow_hashref;
if($tag){
# tasktagの取得
my $tasktag_query = $db->prepare("SELECT * FROM tasktag WHERE tag_id = ?");
$tasktag_query->execute($tag->{id}) or return -1;

# taskの初期化
# my @tasks;
# taskを取得するクエリの準備
my $task_query = $db->prepare("SELECT * FROM task WHERE id = ?");
# while(my $tasktag = $tasktag_query->fetchrow_hashref){

$task_query->execute(my $tasktag->{task_id}) or return -1;
my $task = $task_query->fetchrow_hashref;
#if($task){
#push @tasks, $task->{task};
#}
print $task->{task};
#}

# return new Task("id=$task->{id}&user_id=$task->{user_id}&name=$task->{name}&limit_time=$task->{limit_time}&memo=$task->{memo}&".(join "&", map{ "tag=$_"; } @tags));
return new Task("tag=$tag&id=$task->{id}&user_id=$task->{user_id}&name=$task->{name}&limit_time=$task->{limit_time}&memo=$task->{memo}&");
}else{
return undef;
}
}
