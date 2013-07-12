#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;

print "Content-Type: text/html\n\n";

my $query = $ENV{QUERY_STRING};
if($query){
  my %query = map {
    split(/\=/, $_);
  } split(/&/, $query);

  print "<h1>$query{name}</h1>\n";
  print "<h1>$query{age}</h1>\n";
  print "<h2>he is $query{gender}</h2>\n";
}else{
  print '<form method="GET">name<input type="text" name="name">'.
        'age<input type="text" name="age">'.
        '<select name="gender"><option value="male">男</option><option value="female">女</option></select></form>';
}
