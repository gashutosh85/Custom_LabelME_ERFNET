#!/usr/bin/perl

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use JSON qw (encode_json);

use vars qw($LM_HOME);

my $query = new CGI;

my $query = new CGI;
my $mode = $query->param("mode");
my $username = $query->param("username");
my $collection = $query->param("collection");
my $folder = $query->param("folder") || "original_folder";
my $image = $query->param("image") || "img1.png";



##replace weights with pretrained weights

my $script = system('cp', '-r', '/var/www/html/work/work/erfnet_pytorch/save/erfnet_training3/.','/var/www/html/work/work/erfnet_pytorch/save/erfnet_training4/');

##write 150 as no. to epoch.txt
my $file = "/var/www/html/LabelMe/annotationTools/perl/epoch.txt";
open (CODE, '>'.$file) || die "error";
print CODE '150';
close(CODE);

my $redirect_url  = "http://localhost/LabelMe/tool.html?collection=LabelMe&mode=f&folder=original_images"."&image=$image";

print "Content-type: application/json\n\n";
my $response->{'redirect_url'} = $redirect_url;
$response->{'curr_dir'} = $script;
my $json_response = JSON::to_json($response);
print $json_response;
