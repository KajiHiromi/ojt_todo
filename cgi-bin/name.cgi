#!/usr/bin/env perl

use strict;
use warnings;
use DBI;
use Data::Dumper;

print "Content-type: text/html\n\n";

print "kaji";

my $user = 'todouser';
my $password = 'kaji';

my $db = DBI->connect( 'DBI:mysql:todo',$user,$password );

my $sth = $db->prepare( "select * from USER" );

$sth->execute();

while(my @row = $sth->fetchrow_array ){ print "@row\n";}

$db->disconnect;

print "終了"
