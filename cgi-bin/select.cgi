#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use Task;
use DBI;

my $user = 'todouser';
my $passwd = 'kaji';

#
sub paresBody {
    my ($body) = @_;
    
    my %body = map{ split(/\=/, $_); } split(/&/, $body);

    
    return %body;


}

print "Content-Type: text/html\n\n";
print "<html>\n";
print "<head><title>タグ検索表示</title></head>\n";
print "<body>\n";


            #送信されたデータを受け取る
my $method = $ENV{'REQUEST_METHOD'};
$method = $method || "GET";
             
#print "method = $method\n";

if ($method eq 'POST') {
    read STDIN, my $alldata, $ENV{'CONTENT_LENGTH'};
    warn $alldata;
    $alldata =~tr/+//;
    $alldata =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;

    #print "オールデータは$alldata\n";
   
    
    my %vals = &paresBody($alldata); 
        
    #print %vals;
    print "カテゴリー検索　→　[$vals{'tag'}]\n\n";

    #print '<a href="http://192.168.75.128/cgi-bin/todo/create.cgi">TODO登録ページへ</a>'
    #print '<a href="http://192.168.75.128/cgi-bin/todo/index.cgi">タスク一覧ページへ</a>'    

   
    
 
    my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
  
    my $tagQuery = $db->prepare("SELECT * FROM tag WHERE tag = ?;");

   
     $tagQuery->execute($vals{'tag'});

     my $tag = $tagQuery->fetchrow_hashref;
 

     my $tasktagsQuery = $db->prepare("SELECT * FROM tasktag WHERE tag_id=?");
     $tasktagsQuery->execute($tag->{id}) || die $tasktagsQuery->errstr;
     my $tasktags_num = $tasktagsQuery->rows;

    for (my $i=0; $i < $tasktags_num; $i++){
         my $tasktag = $tasktagsQuery->fetchrow_hashref;

   # print "タスク$tasktag->{task_id}";
    #print Dumper $tasktag;

    my $taskQuery = $db->prepare("SELECT * FROM task WHERE id=? AND status=?");
    $taskQuery->execute($tasktag->{task_id},"未完了") || die $taskQuery->errstr;

    my $task2 = $taskQuery->fetchrow_hashref;

     print "<div>\n";
     print "TODO：$task2->{name}\n\n<br>";
     print "期限： $task2->{limit_time}\n\n<br>";
     print "メモ：$task2->{memo}\n\n<br><br><br>";
     print "</div\n>";


    }  
                       

} else {
    my $alldata = $ENV{'QUERY_STRING'} || "";                                           
}


#foreach my $data (split(/&/, my $alldata)) {
 #my ($key, $value) = split(/=/, $data);

  #$value =~ s/\+/ /g;
  #$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
  #$value =~ s/\t//g;


  #print $dbtask
 #my $in{"$key"} = my $value;
#}

#print "Content-Type: text/html\n\n";
#print "<html>\n";
#print "<head><title>タグ検索表示</title></head>\n";
#print "<body>\n";

#受け取ったデータを表示する
#print my $dbtag->tag;
#
print "</body>\n";
print "</html>\n";
#
exit;



