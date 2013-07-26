#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use Task;


sub checkUser {
 # cookieをチェックして、データベースを引いて、セッションIDと照らし合わせて、ユーザを特定して、そのユーザを返す
 return {
   user_id => 1,
   name => "kaji",
 }
}  
my $user = &checkUser();

#送信されたデータを受け取る
my $method = $ENV{'REQUEST_METHOD'};
$method = $method || "GET";
# print "method = $method\n";
if ($method eq 'POST') {
  read(STDIN, my $alldata, $ENV{'CONTENT_LENGTH'});
  
  $alldata =~tr/+//;
  $alldata=~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;
  
  my $task = new Task("$alldata", $user->{user_id});
  #print Dumper $task;
  my $result = $task->insert();
  
  print "Status: 302 Moved\n"; 
  print "Location: index.cgi\n\n"; 
  
  print "Content-type: text/html\n\n";
  
 

} else {
  my $alldata = $ENV{'QUERY_STRING'} || "";

  print "Content-type: text/html\n\n";

  print "<html>\n";
  print "<head>\n";

  print "<title>Todo</title>\n";
  print "</head>\n";
  print "<body>\n";
  print '<h1>TODO登録</h1>';
  print '<form action="create.cgi" method="post">'."\n";
  print 'TODO: <input type="text" name="name"><br>'."\n";
  print 'カテゴリー:<input type ="checkbox" name="tag" value="ビジネス">ビジネス'."\n";
  print '<input type ="checkbox" param name="tag" value="プライベート">プライベート<br>'."\n";
  print '期限:<input type="datetime" param name= "limit_time"><br>'."\n";
  print 'メモ: <textarea rows="7" cols="50" param name="memo"></textarea><br>'."\n";
  print '<input type="submit">'."\n";
  print '</form>'."\n";

}

print "</body>\n";
print "</html>\n";


