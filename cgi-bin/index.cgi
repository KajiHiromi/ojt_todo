#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;

# 1. http method を調べる

# 2. db server からデータを取得する
use DBI;


print "Content-type: text/html\n";
print "\n";



my $user = 'todouser';
my $passwd = 'kaji';

print "<html>\n";
print "<head>\n";

print "<title>Todo</title>\n";
print "</head>\n";
print "<body>\n";

print "<h1>TODO一覧</h1>\n";


# タグ検索フォーム
    print '<form action="select.cgi" method="post">'."\n";
    print 'カテゴリー検索:<input type="text" name="tag"><br>'."\n";

# print '<input type="submit" name="tag_select_form" value="タグ検索">'."\n";
    print '<input type="submit">'."\n";
    print '</form>';
#}



my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
my $tasksQuery = $db->prepare("SELECT * FROM task WHERE user_id = ? AND status = ?;");
    
$tasksQuery->execute(1,"未完了");

my $tasks_num = $tasksQuery->rows;

for (my $i=0; $i < $tasks_num; $i++) {
  my $task = $tasksQuery->fetchrow_hashref;
#   print $task->{id}."\n";
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
    #print $task->{id};
    print '<form action="update.cgi" method="post">'."\n";
    print "<input type=\"hidden\" name=\"id\" value=\"$task->{id}\">","\n";
    #print '<input type="hidden" name="id" value="'.$task->{id}.'">',"\n";
    #print '<input type="hidden" name="status" value="完了}">',"\n";
    print '<input type="submit" name="status" value="完了">'."\n";
    print '</form>';  
    print "</div>\n";
 }
print '<a href="http://192.168.75.128/cgi-bin/todo/create.cgi">TODO登録ページへ</a>';
print "</body>\n";
print "</html>\n";

$tasksQuery->finish;
$db->disconnect;


