#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;

use Task;

#sub update {
#  my ($self, %content) = @_;
#}

my $body = "";
my $task = Task::findById(6);

#print Dumper $task;
$task->updateStatus('未完了');
#$task->update(status => 1, limit_time => "aaaa");


