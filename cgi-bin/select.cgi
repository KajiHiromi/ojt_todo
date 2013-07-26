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


            #送信されたデータを受け取る
my $method = $ENV{'REQUEST_METHOD'};
$method = $method || "GET";
             
print "method = $method\n";

if ($method eq 'POST') {
    read STDIN, my $alldata, $ENV{'CONTENT_LENGTH'};
    #warn $alldata;
    $alldata =~tr/+//;
    $alldata =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;


    my %vals = &paresBody($alldata);
    my $dbtag = \%vals;
 

  #  my $db = DBI->connect('DBI:mysql:todo',$user,$passwd);
  #  my $tagQuery = $db->prepare("SELECT * FROM tag WHERE tag = ?;");


  #  $tagQuery->execute($dbtag->{tag});

  #  my $tag = $tagQuery->fetchrow_hashref;

  #  my $tasktagsQuery = $db->prepare("SELECT * FROM tasktag WHERE tag_id=?");
  #  $tasktagsQuery->execute($tag->{id}) || die $tasktagsQuery->errstr;
  #  my $tasktags_num = $tasktagsQuery->rows;

  #  for (my $i=0; $i < $tasktags_num; $i++){
  #      my $tasktag = $tasktagsQuery->fetchrow_hashref;


    }  
                                   
print "Content-type: text/html\n\n";

} else {
    my $alldata = $ENV{'QUERY_STRING'} || "";                                           
}





