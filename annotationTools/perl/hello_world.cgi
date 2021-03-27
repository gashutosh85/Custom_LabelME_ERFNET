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

# my $curr_dir = $folder.' '.$image;
print $image;
# my $cmd = " /Library/WebServer/Documents/LabelMeAnnotationTool/Images/prediction_overlay.py original_images $image";
my $script = system('/Users/nikhil.p/AshuKaMS/myenv/bin/python', '/Library/WebServer/Documents/LabelMeAnnotationTool/Images/prediction_overlay.py','original_images', $image );
my $redirect_url  = "http://localhost/LabelMeAnnotationTool/tool.html?collection=LabelMe&mode=f&folder=overlayed_images_for_scribbles"."&image=$image";

print "Content-type: application/json\n\n";
my $response->{'redirect_url'} = $redirect_url;
$response->{'curr_dir'} = $script;
my $json_response = JSON::to_json($response);
print $json_response;
