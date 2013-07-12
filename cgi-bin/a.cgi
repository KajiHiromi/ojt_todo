#!/usr/bin/env perl
use strict;
use warnings;

my $ref_x =[1,2,3];

my @x = map {$_ * 2} @$ref_x;

print $ref_x->[0];

my @new_x = @$ref_x;

print $new_x[0];
