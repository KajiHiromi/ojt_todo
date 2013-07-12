#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use Task;

sub paresBody {
    my ($body) = @_;
    my %body = map{ split(/\=/, $_); } split(/&/, $body);
    return %body;
}


#送信されたデータを受け取る
my $method = $ENV{'REQUEST_METHOD'};
$method = $method || "GET";
 
#print "method = $method\n";

if ($method eq 'POST') {
  read STDIN, my $alldata, $ENV{'CONTENT_LENGTH'};
  #warn $alldata;
  $alldata =~tr/+//;
  $alldata =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;


  my %vals = &paresBody($alldata);
  my $dbtask = \%vals;
  #warn Dumper $dbtask;
  my $task = Task::findById($dbtask->{id});
  #warn Dumper $task;
  $task->updateStatus($dbtask->{status});
  
  print "Status: 302 Moved\n";
  print "Location: index.cgi\n\n";

  print "Content-type: text/html\n\n";


} else {
   my $alldata = $ENV{'QUERY_STRING'} || "";
}
